"""
Entry point for running the contract analysis workflow from the command line.
"""

from __future__ import annotations

from ai_agents.graph import AgentState, build_parallel_graph
from ai_agents.planner import PlanningModule


def run(query: str):
	planner = PlanningModule()
	plan = planner.generate_plan(query)

	graph = build_parallel_graph(plan)

	# Initialize state
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
	return result


if __name__ == "__main__":
	sample_query = "Analyze the contract for legal, compliance, financial, and operational risks"
	output = run(sample_query)
	print("\n=== Analysis Complete ===")
	for key, value in output.items():
		if value:
			print(f"\n[{key}]\n{value}")
