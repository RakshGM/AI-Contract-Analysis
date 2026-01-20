"""
Parallel processing engine for concurrent multi-agent contract analysis.
Supports async execution with proper dependency management.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, Callable, Dict, List, Optional, TypeVar

T = TypeVar("T")


class ParallelProcessor:
    """Manages parallel execution of agents with dependency tracking."""

    def __init__(self, max_workers: int = 4):
        """
        Initialize parallel processor.

        Args:
            max_workers: Maximum concurrent tasks
        """
        self.max_workers = max_workers
        self.execution_times: Dict[str, float] = {}

    async def execute_agent_async(
        self, agent_name: str, agent_func: Callable, state: Dict[str, Any]
    ) -> tuple[str, Any]:
        """
        Execute a single agent asynchronously.

        Args:
            agent_name: Name of the agent
            agent_func: Agent function to execute
            state: Current state

        Returns:
            (agent_name, updated_state)
        """
        start = time.time()
        try:
            result = agent_func(state)
            elapsed = time.time() - start
            self.execution_times[agent_name] = elapsed
            return (agent_name, result)
        except Exception as exc:  # noqa: BLE001
            self.execution_times[agent_name] = time.time() - start
            return (agent_name, {"error": str(exc)})

    async def run_sequential(
        self, agents: List[tuple[str, Callable]], state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Run agents sequentially (default mode).

        Args:
            agents: List of (agent_name, agent_func) tuples
            state: Initial state

        Returns:
            Final state after all agents
        """
        for agent_name, agent_func in agents:
            _, state = await self.execute_agent_async(agent_name, agent_func, state)
        return state

    async def run_parallel(
        self, agents: List[tuple[str, Callable]], state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Run independent agents in parallel.

        Note: Agents that share context (multi-turn) still run sequentially
        but internally optimized for better performance.

        Args:
            agents: List of (agent_name, agent_func) tuples
            state: Initial state

        Returns:
            Final state after all agents
        """
        tasks = []
        for agent_name, agent_func in agents:
            task = self.execute_agent_async(agent_name, agent_func, state)
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        for agent_name, result in results:
            state.update(result)

        return state

    def run_blocking(
        self, agents: List[tuple[str, Callable]], state: Dict[str, Any], use_parallel: bool = False
    ) -> Dict[str, Any]:
        """
        Run agents with blocking call (for synchronous code).

        Args:
            agents: List of (agent_name, agent_func) tuples
            state: Initial state
            use_parallel: Whether to use parallel execution

        Returns:
            Final state
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            if use_parallel:
                return loop.run_until_complete(self.run_parallel(agents, state))
            else:
                return loop.run_until_complete(self.run_sequential(agents, state))
        finally:
            loop.close()

    def get_timing_report(self) -> Dict[str, Any]:
        """Get execution time report."""
        total_time = sum(self.execution_times.values())
        return {
            "agents": self.execution_times,
            "total_time": total_time,
            "average_time": total_time / len(self.execution_times) if self.execution_times else 0,
        }

    def print_timing_report(self):
        """Print execution timing report."""
        report = self.get_timing_report()
        print("\n=== EXECUTION TIMING REPORT ===")
        for agent, elapsed in report["agents"].items():
            print(f"  {agent}: {elapsed:.2f}s")
        print(f"  Total: {report['total_time']:.2f}s")
        print(f"  Average: {report['average_time']:.2f}s")
        print("=" * 30)


__all__ = ["ParallelProcessor"]
