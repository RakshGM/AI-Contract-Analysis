"""
Concurrent contract processing engine for batch analysis.
Optimized for handling multiple contracts simultaneously.
"""

from __future__ import annotations

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Tuple

from ai_agents.graph import AgentState, build_parallel_graph
from ai_agents.planner import PlanningModule
from document_parser import load_document, split_document
from embed_and_upsert import embed_and_upload


class BatchProcessor:
    """Process multiple contracts concurrently."""

    def __init__(self, max_concurrent: int = 3, use_parallel_agents: bool = True):
        """
        Initialize batch processor.

        Args:
            max_concurrent: Maximum concurrent contract analyses
            use_parallel_agents: Use parallel agent execution
        """
        self.max_concurrent = max_concurrent
        self.use_parallel_agents = use_parallel_agents
        self.results: Dict[str, Dict[str, Any]] = {}
        self.timings: Dict[str, float] = {}
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent)

    def process_contract_sync(self, contract_id: str, contract_path: str, query: str) -> Dict[str, Any]:
        """
        Process single contract (synchronous).

        Args:
            contract_id: Unique identifier
            contract_path: Path to contract file or text
            query: Analysis query

        Returns:
            Analysis results
        """
        start = time.time()

        try:
            # Load and embed
            text = load_document(file_path=contract_path)
            chunks = split_document(text)
            embed_and_upload(chunks, document_id=contract_id)

            # Analyze
            planner = PlanningModule()
            plan = planner.generate_plan(query)
            graph = build_parallel_graph(plan) if self.use_parallel_agents else build_parallel_graph(plan)

            state = AgentState(
                query=query,
                legal=None,
                compliance=None,
                finance=None,
                operations=None,
                legal_clauses=None,
                compliance_risks=None,
                finance_risks=None,
                agent_context=None,
                final_summary=None,
            )

            result = graph.invoke(state)
            elapsed = time.time() - start

            self.timings[contract_id] = elapsed
            self.results[contract_id] = {"status": "success", "result": result, "time": elapsed}

            return {"status": "success", "contract_id": contract_id, "time": elapsed}

        except Exception as exc:  # noqa: BLE001
            elapsed = time.time() - start
            self.timings[contract_id] = elapsed
            self.results[contract_id] = {"status": "error", "error": str(exc), "time": elapsed}

            return {"status": "error", "contract_id": contract_id, "error": str(exc), "time": elapsed}

    def process_contracts_batch(
        self, contracts: List[Tuple[str, str, str]]
    ) -> Dict[str, Any]:
        """
        Process multiple contracts concurrently.

        Args:
            contracts: List of (contract_id, file_path, query) tuples

        Returns:
            Summary of processing
        """
        batch_start = time.time()
        futures = {}

        # Submit all tasks
        for contract_id, file_path, query in contracts:
            future = self.executor.submit(self.process_contract_sync, contract_id, file_path, query)
            futures[future] = contract_id

        # Collect results as they complete
        completed = []
        for future in as_completed(futures):
            contract_id = futures[future]
            try:
                result = future.result()
                completed.append(result)
            except Exception as exc:  # noqa: BLE001
                completed.append({"status": "error", "contract_id": contract_id, "error": str(exc)})

        batch_elapsed = time.time() - batch_start

        return {
            "status": "complete",
            "total_contracts": len(contracts),
            "successful": len([c for c in completed if c["status"] == "success"]),
            "failed": len([c for c in completed if c["status"] == "error"]),
            "batch_time": batch_elapsed,
            "results": completed,
        }

    def get_contract_result(self, contract_id: str) -> Optional[Dict[str, Any]]:
        """Get analysis result for a specific contract."""
        return self.results.get(contract_id)

    def get_timing_summary(self) -> Dict[str, Any]:
        """Get timing summary for all processed contracts."""
        if not self.timings:
            return {}

        times = list(self.timings.values())
        return {
            "total_time": sum(times),
            "average_time": sum(times) / len(times),
            "min_time": min(times),
            "max_time": max(times),
            "contracts_processed": len(times),
        }

    def print_summary(self):
        """Print processing summary."""
        summary = self.get_timing_summary()

        print("\n" + "=" * 60)
        print("BATCH PROCESSING SUMMARY")
        print("=" * 60)

        if not summary:
            print("No contracts processed")
            return

        print(f"Total Contracts: {summary['contracts_processed']}")
        print(f"Total Time: {summary['total_time']:.2f}s")
        print(f"Average Time: {summary['average_time']:.2f}s")
        print(f"Min Time: {summary['min_time']:.2f}s")
        print(f"Max Time: {summary['max_time']:.2f}s")
        print("=" * 60)

    def cleanup(self):
        """Cleanup executor."""
        self.executor.shutdown(wait=True)


class ContractQueue:
    """Queue-based contract processor for larger batches."""

    def __init__(self, max_queue_size: int = 100):
        """Initialize queue."""
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self.results: Dict[str, Any] = {}

    async def add_contract(self, contract_id: str, file_path: str, query: str):
        """Add contract to processing queue."""
        await self.queue.put({"contract_id": contract_id, "file_path": file_path, "query": query})

    async def process_queue(self, num_workers: int = 3) -> Dict[str, Any]:
        """Process queued contracts with specified number of workers."""
        workers = [asyncio.create_task(self._worker(i)) for i in range(num_workers)]

        # Wait for queue to be empty
        await self.queue.join()

        # Cancel workers
        for w in workers:
            w.cancel()

        return {"processed": len(self.results), "results": self.results}

    async def _worker(self, worker_id: int):
        """Worker coroutine."""
        while True:
            try:
                item = self.queue.get_nowait()

                try:
                    processor = BatchProcessor(max_concurrent=1)
                    result = processor.process_contract_sync(
                        item["contract_id"], item["file_path"], item["query"]
                    )

                    self.results[item["contract_id"]] = result
                    processor.cleanup()

                finally:
                    self.queue.task_done()

            except asyncio.QueueEmpty:
                await asyncio.sleep(0.1)


def process_contracts_parallel(
    contracts: List[Tuple[str, str, str]], max_concurrent: int = 3, show_progress: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to process multiple contracts in parallel.

    Args:
        contracts: List of (contract_id, file_path, query) tuples
        max_concurrent: Maximum concurrent analyses
        show_progress: Print progress updates

    Returns:
        Processing results
    """
    processor = BatchProcessor(max_concurrent=max_concurrent)

    try:
        results = processor.process_contracts_batch(contracts)

        if show_progress:
            processor.print_summary()

        return results

    finally:
        processor.cleanup()


__all__ = ["BatchProcessor", "ContractQueue", "process_contracts_parallel"]
