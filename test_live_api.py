"""
Simple test with actual contract text to verify API is working
"""

from ai_agents import PlanningModule, build_graph, AgentState

CONTRACT = """
SERVICE AGREEMENT

PAYMENT: $50,000 monthly, Net 30. Late fee: 2% per month.
LIABILITY: Capped at $1M except gross negligence.
COMPLIANCE: Must meet GDPR, HIPAA, SOC 2 requirements.
TERMINATION: 60 days notice or $100,000 penalty.
"""

query = f"""
Analyze this contract:

{CONTRACT}

Focus on: liability risks, payment terms, and compliance gaps.
"""

print("\n🤖 Running Multi-Turn Agent Analysis...\n")

planner = PlanningModule()
plan = planner.generate_plan(query)

print(f"📋 Agents: {plan['agents']}")
print(f"💭 Reasoning: {plan['reasoning'][:80]}...\n")

graph = build_graph(plan)
result = graph.invoke(AgentState(query=query))

print("="*80)
print("RESULTS:")
print("="*80)

for agent_type in ['legal', 'compliance', 'finance', 'operations']:
    if result.get(agent_type):
        print(f"\n{agent_type.upper()} AGENT:")
        print(result[agent_type][:300])
        print("...\n")

print("✅ Analysis complete!")
