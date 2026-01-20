"""
Test Operations Agent - SLA Analysis & Delivery Feasibility
"""

from ai_agents import PlanningModule, build_graph, AgentState

CONTRACT = """
SERVICE AGREEMENT - DELIVERY & OPERATIONS

PROJECT TIMELINE:
- Phase 1 (Requirements): 2 weeks
- Phase 2 (Development): 8 weeks  
- Phase 3 (Testing): 4 weeks
- Phase 4 (Deployment): 2 weeks
- Total project duration: 16 weeks from contract signing

SERVICE LEVEL AGREEMENT (SLA):
- System Uptime: 99.9% monthly (maximum 43 minutes downtime per month)
- Response Time: Critical issues < 1 hour, High issues < 4 hours, Medium < 24 hours
- Resolution Time: Critical < 4 hours, High < 24 hours, Medium < 72 hours
- Performance: Page load time < 2 seconds, API response < 500ms

PENALTIES FOR SLA VIOLATIONS:
- Uptime below 99.9%: $5,000 credit per 0.1% below target
- Missed critical response time: $2,000 per incident
- Missed critical resolution time: $10,000 per incident
- Performance degradation: $1,000 per day until resolved

OPERATIONAL REQUIREMENTS:
- 24/7 monitoring and support
- Weekly status reports
- Monthly business reviews
- Quarterly security audits
- Annual disaster recovery testing

RESOURCE COMMITMENTS:
- Dedicated project manager
- Minimum 3 senior developers
- DevOps engineer available 24/7
- Customer support team (5 agents minimum)

DELIVERY MILESTONES:
- Week 2: Requirements approval (payment: $50,000)
- Week 10: Development complete (payment: $100,000)
- Week 14: Testing complete (payment: $75,000)
- Week 16: Production deployment (payment: $75,000)
- Total contract value: $300,000
"""

query = f"""
Analyze the operational feasibility and SLA commitments in this contract:

{CONTRACT}

Focus on:
1. Are the timelines realistic?
2. Are the SLA targets achievable?
3. What are the operational risks?
4. What is the penalty exposure for SLA violations?
5. Are the resource commitments adequate?
"""

print("\n" + "="*80)
print("🔧 OPERATIONS AGENT - SLA & DELIVERY ANALYSIS")
print("="*80 + "\n")

print("📋 Query: Analyze operational feasibility, SLAs, and delivery timelines\n")

planner = PlanningModule()
plan = planner.generate_plan(query)

print(f"🤖 Selected Agents: {', '.join(plan['agents'])}")
print(f"💭 Reasoning: {plan['reasoning'][:100]}...\n")

print("⚙️  Building execution graph and running agents...\n")

graph = build_graph(plan)
result = graph.invoke(AgentState(query=query))

print("="*80)
print("📊 OPERATIONS AGENT ANALYSIS:")
print("="*80 + "\n")

if result.get("operations"):
    print(result["operations"])
else:
    print("⚠️  Operations agent was not selected by the planner.")
    print("\nIncluded agents:")
    for agent_type in ['legal', 'compliance', 'finance']:
        if result.get(agent_type):
            print(f"\n{agent_type.upper()} AGENT:")
            print(result[agent_type][:250])
            print("...\n")

print("\n" + "="*80)
print("✅ Operations analysis complete!")
print("="*80)
