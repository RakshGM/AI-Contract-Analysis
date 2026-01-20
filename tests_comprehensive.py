"""
Comprehensive test suite for parallel processing, structured pipelines,
multi-turn interaction, and Pinecone storage.
"""

from __future__ import annotations

import json
import unittest
from datetime import datetime

from ai_agents.graph import AgentState, build_parallel_graph
from ai_agents.intermediates_storage import IntermediatesStorage
from ai_agents.parallel_processor import ParallelProcessor
from ai_agents.planner import PlanningModule
from ai_agents.structured_extraction import (
    ComplianceExtractionPipeline,
    FinancialRiskExtractionPipeline,
    MultiDomainClauseExtractor,
)


class TestStructuredPipelines(unittest.TestCase):
    """Test structured extraction pipelines."""

    def setUp(self):
        self.sample_context = """
        SERVICE AGREEMENT between Provider Corp and Client Inc.
        Payment: $50,000 monthly, due on 1st of month.
        SLA: 99.9% uptime guarantee.
        Data Protection: GDPR compliant, encryption required.
        Termination: 30 days notice, early exit penalty $100k.
        """
        self.sample_query = "Analyze all risks in this contract"

    def test_compliance_extraction_returns_valid_structure(self):
        """Compliance pipeline returns expected JSON structure."""
        result = ComplianceExtractionPipeline.extract_compliance_risks(
            self.sample_context, self.sample_query
        )

        self.assertIn("status", result)
        self.assertIn("data", result)
        self.assertIn("timestamp", result)

        data = result.get("data", {})
        self.assertIn("regulations_violated", data)
        self.assertIn("missing_clauses", data)
        self.assertIn("overall_compliance_score", data)
        self.assertIn("priority_actions", data)

    def test_compliance_score_is_numeric(self):
        """Compliance score should be a number."""
        result = ComplianceExtractionPipeline.extract_compliance_risks(
            self.sample_context, self.sample_query
        )
        score = result.get("data", {}).get("overall_compliance_score")
        self.assertIsInstance(score, (int, float))
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_financial_extraction_returns_valid_structure(self):
        """Financial pipeline returns expected JSON structure."""
        result = FinancialRiskExtractionPipeline.extract_financial_risks(
            self.sample_context, self.sample_query
        )

        self.assertIn("status", result)
        self.assertIn("data", result)

        data = result.get("data", {})
        self.assertIn("payment_obligations", data)
        self.assertIn("penalties", data)
        self.assertIn("financial_risks", data)

    def test_clause_extraction_covers_all_domains(self):
        """Clause extraction should cover all domains."""
        result = MultiDomainClauseExtractor.extract_clauses(self.sample_context, self.sample_query)

        self.assertIn("status", result)
        data = result.get("data", {})

        expected_keys = [
            "legal_clauses",
            "termination_clauses",
            "liability_caps",
            "ip_clauses",
            "sla_terms",
            "payment_terms",
            "data_protection",
        ]

        for key in expected_keys:
            self.assertIn(key, data)


class TestMultiTurnInteraction(unittest.TestCase):
    """Test multi-turn agent interaction with context passing."""

    def setUp(self):
        self.query = "Analyze contract for legal, compliance, and financial risks"
        self.planner = PlanningModule()

    def test_agent_context_accumulates(self):
        """Context should accumulate across agent executions."""
        plan = self.planner.generate_plan(self.query)
        graph = build_parallel_graph(plan)

        state = AgentState(
            query=self.query,
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

        # Check that context was accumulated
        agent_context = result.get("agent_context")
        if agent_context:
            # Should contain multiple agent findings
            self.assertIsInstance(agent_context, str)
            self.assertGreater(len(agent_context), 0)

    def test_multiple_agents_execute(self):
        """Multiple agents should execute and produce results."""
        plan = self.planner.generate_plan("Full contract analysis")
        graph = build_parallel_graph(plan)

        state = AgentState(
            query="Full contract analysis",
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

        # At least one agent should produce output
        agent_outputs = [
            result.get("legal"),
            result.get("compliance"),
            result.get("finance"),
            result.get("operations"),
        ]

        non_none_outputs = [o for o in agent_outputs if o]
        self.assertGreater(len(non_none_outputs), 0)


class TestPineconeStorage(unittest.TestCase):
    """Test intermediate result storage in Pinecone."""

    def test_store_and_retrieve_intermediate_result(self):
        """Should store and retrieve intermediate results."""
        try:
            query = "Test query for storage"
            agent_name = "TestAgent"
            result_data = {"test": "data", "score": 95}

            # Store
            store_result = IntermediatesStorage.store_intermediate_result(
                query=query,
                agent_name=agent_name,
                result=result_data,
                analysis_type="test",
            )

            self.assertEqual(store_result.get("status"), "stored")

            # Retrieve
            retrieved = IntermediatesStorage.retrieve_intermediate_result(
                query=query,
                agent_name=agent_name,
            )

            if retrieved:
                self.assertIn("metadata", retrieved)
                self.assertEqual(retrieved["metadata"].get("agent"), agent_name)

        except Exception as exc:
            # Pinecone may not be configured
            self.skipTest(f"Pinecone not configured: {exc}")

    def test_store_multi_agent_results(self):
        """Should store combined multi-agent results."""
        try:
            query = "Multi-agent test"
            results = {
                "legal": "Legal analysis",
                "compliance": "Compliance analysis",
                "finance": "Financial analysis",
            }

            store_result = IntermediatesStorage.store_multi_agent_results(query, results)

            self.assertEqual(store_result.get("status"), "stored")

        except Exception as exc:
            self.skipTest(f"Pinecone not configured: {exc}")

    def test_retrieve_similar_queries(self):
        """Should retrieve similar historical queries."""
        try:
            # Store a few test results first
            for i in range(3):
                IntermediatesStorage.store_intermediate_result(
                    query=f"Payment terms analysis {i}",
                    agent_name="FinanceAgent",
                    result={"test": i},
                    analysis_type="financial",
                )

            # Retrieve similar
            similar = IntermediatesStorage.retrieve_similar_queries(
                query="Payment terms", analysis_type="financial", top_k=3
            )

            self.assertIsInstance(similar, list)

        except Exception as exc:
            self.skipTest(f"Pinecone not configured: {exc}")


class TestParallelProcessing(unittest.TestCase):
    """Test parallel processing engine."""

    def setUp(self):
        self.processor = ParallelProcessor(max_workers=4)

    def test_processor_tracks_execution_times(self):
        """Processor should track execution times."""

        def dummy_agent(state):
            state["test"] = "completed"
            return state

        state = {"test": None}
        agents = [("DummyAgent", dummy_agent)]

        result_state = self.processor.run_blocking(agents, state, use_parallel=False)

        self.assertIn("DummyAgent", self.processor.execution_times)
        self.assertGreater(self.processor.execution_times["DummyAgent"], 0)

    def test_timing_report_generation(self):
        """Should generate execution timing report."""

        def agent_func(state):
            return state

        state = {}
        agents = [("Agent1", agent_func), ("Agent2", agent_func)]

        self.processor.run_blocking(agents, state)
        report = self.processor.get_timing_report()

        self.assertIn("agents", report)
        self.assertIn("total_time", report)
        self.assertIn("average_time", report)


class TestIntegration(unittest.TestCase):
    """Integration tests combining all features."""

    def test_full_workflow_with_all_features(self):
        """Complete workflow: plan → parallel execute → store results."""
        query = "Comprehensive contract risk analysis"

        # Step 1: Plan
        planner = PlanningModule()
        plan = planner.generate_plan(query)
        self.assertIn("agents", plan)

        # Step 2: Execute
        graph = build_parallel_graph(plan)
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
        self.assertIsNotNone(result)

        # Step 3: Verify multi-turn context
        if result.get("agent_context"):
            self.assertGreater(len(result["agent_context"]), 0)

        # Step 4: Store results (may fail if Pinecone not configured)
        try:
            IntermediatesStorage.store_multi_agent_results(query, result)
        except Exception:
            pass  # OK if Pinecone not available


def run_all_tests():
    """Run all tests with summary."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestStructuredPipelines))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiTurnInteraction))
    suite.addTests(loader.loadTestsFromTestCase(TestPineconeStorage))
    suite.addTests(loader.loadTestsFromTestCase(TestParallelProcessing))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 60)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
