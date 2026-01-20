"""
Lightweight tests for planner, graph execution, and structured pipelines.
These tests avoid external service calls by relying on fallbacks when API
keys are not configured.
"""

import unittest

from ai_agents.graph import AgentState, build_parallel_graph
from ai_agents.planner import PlanningModule
from ai_agents.structured_extraction import (
	ComplianceExtractionPipeline,
	FinancialRiskExtractionPipeline,
	MultiDomainClauseExtractor,
)


class PlannerTests(unittest.TestCase):
	def test_planner_fallback(self):
		planner = PlanningModule()
		plan = planner.generate_plan("Check payment terms and GDPR")
		self.assertIn("agents", plan)
		self.assertGreater(len(plan["agents"]), 0)


class GraphExecutionTests(unittest.TestCase):
	def test_graph_runs_with_fallbacks(self):
		query = "Analyze contract for risks"
		planner = PlanningModule()
		plan = planner.generate_plan(query)
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
		# Ensure at least one agent wrote something
		self.assertTrue(
			any(result.get(key) for key in ["legal", "compliance", "finance", "operations"])
		)


class StructuredExtractionTests(unittest.TestCase):
	def test_compliance_extraction_fallback(self):
		res = ComplianceExtractionPipeline.extract_compliance_risks("", "")
		self.assertEqual(res.get("status"), "success")

	def test_finance_extraction_fallback(self):
		res = FinancialRiskExtractionPipeline.extract_financial_risks("", "")
		self.assertEqual(res.get("status"), "success")

	def test_clause_extraction_fallback(self):
		res = MultiDomainClauseExtractor.extract_clauses("", "")
		self.assertEqual(res.get("status"), "success")


if __name__ == "__main__":
	unittest.main()
