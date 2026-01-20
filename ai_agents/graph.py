"""
LangGraph state management and graph builder for multi-agent orchestration
"""

from typing import TypedDict, Optional, Dict, Any, List
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    """
    Shared state across all agents
    
    Attributes:
        query: Original user query
        legal: Legal agent analysis results
        compliance: Compliance agent analysis results
        finance: Finance agent analysis results
        operations: Operations agent analysis results
        legal_clauses: Structured legal clauses (from structured extraction)
        compliance_risks: Structured compliance risks (from structured extraction)
        finance_risks: Structured financial risks (from structured extraction)
        agent_context: Accumulated context from previous agents (for multi-turn)
        final_summary: Combined summary of all analyses
    """
    query: str
    legal: Optional[str]
    compliance: Optional[str]
    finance: Optional[str]
    operations: Optional[str]
    legal_clauses: Optional[Dict[str, Any]]
    compliance_risks: Optional[Dict[str, Any]]
    finance_risks: Optional[Dict[str, Any]]
    agent_context: Optional[str]
    final_summary: Optional[str]


def build_graph(plan: Dict[str, Any]) -> StateGraph:
    """
    Build LangGraph execution graph based on planner output (sequential)
    
    Args:
        plan: Plan dictionary from PlanningModule with 'agents' and 'execution_order'
        
    Returns:
        Compiled StateGraph
    """
    from ai_agents.agents.legal_agent import legal_agent
    from ai_agents.agents.compliance_agent import compliance_agent
    from ai_agents.agents.finance_agent import finance_agent
    from ai_agents.agents.operations_agent import operations_agent
    
    # Create graph
    workflow = StateGraph(AgentState)
    
    # Agent mapping
    agent_map = {
        "LegalAgent": legal_agent,
        "ComplianceAgent": compliance_agent,
        "FinanceAgent": finance_agent,
        "OperationsAgent": operations_agent
    }
    
    execution_order = plan.get("execution_order", [])
    
    if not execution_order:
        raise ValueError("Execution order is empty in plan")
    
    # Add nodes for each agent in execution order
    for agent_name in execution_order:
        if agent_name in agent_map:
            workflow.add_node(agent_name, agent_map[agent_name])
    
    # Set entry point
    workflow.set_entry_point(execution_order[0])
    
    # Add edges in sequence
    for i in range(len(execution_order) - 1):
        workflow.add_edge(execution_order[i], execution_order[i + 1])
    
    # Last agent connects to END
    workflow.add_edge(execution_order[-1], END)
    
    # Compile graph
    return workflow.compile()


def build_parallel_graph(plan: Dict[str, Any]) -> StateGraph:
    """
    Build LangGraph with TRUE parallel execution for all agents
    
    All agents run concurrently for maximum speed.
    
    Args:
        plan: Plan dictionary from PlanningModule
        
    Returns:
        Compiled StateGraph with parallel execution capability
    """
    from ai_agents.agents.legal_agent import legal_agent
    from ai_agents.agents.compliance_agent import compliance_agent
    from ai_agents.agents.finance_agent import finance_agent
    from ai_agents.agents.operations_agent import operations_agent
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    def parallel_agent_executor(state: AgentState) -> AgentState:
        """Execute all agents in parallel using thread pool"""
        # Agent mapping
        agent_map = {
            "LegalAgent": legal_agent,
            "ComplianceAgent": compliance_agent,
            "FinanceAgent": finance_agent,
            "OperationsAgent": operations_agent
        }
        
        execution_order = plan.get("execution_order", [])
        
        # Run all agents in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {}
            for agent_name in execution_order:
                if agent_name in agent_map:
                    # Each agent gets a copy of state to work with
                    future = executor.submit(agent_map[agent_name], dict(state))
                    futures[future] = agent_name
            
            # Collect results as they complete
            for future in as_completed(futures):
                agent_name = futures[future]
                try:
                    result_state = future.result()
                    # Merge results back into main state
                    for key in ["legal", "compliance", "finance", "operations", 
                               "legal_clauses", "compliance_risks", "finance_risks"]:
                        if key in result_state and result_state[key]:
                            state[key] = result_state[key]
                except Exception as exc:
                    print(f"Agent {agent_name} generated an exception: {exc}")
        
        return state
    
    # Create simple graph with single parallel executor node
    workflow = StateGraph(AgentState)
    workflow.add_node("parallel_executor", parallel_agent_executor)
    workflow.set_entry_point("parallel_executor")
    workflow.add_edge("parallel_executor", END)
    
    return workflow.compile()


def create_agent_summary(state: AgentState) -> str:
    """
    Create a combined summary from all agent results
    
    Args:
        state: AgentState with all agent results
        
    Returns:
        Combined summary string
    """
    summary_parts = []
    
    summary_parts.append("=" * 60)
    summary_parts.append("CONTRACT ANALYSIS SUMMARY")
    summary_parts.append("=" * 60)
    summary_parts.append(f"\nQuery: {state['query']}\n")
    
    if state.get("legal"):
        summary_parts.append("\n--- LEGAL ANALYSIS ---")
        summary_parts.append(state["legal"])
    
    if state.get("compliance"):
        summary_parts.append("\n--- COMPLIANCE ANALYSIS ---")
        summary_parts.append(state["compliance"])
    
    if state.get("finance"):
        summary_parts.append("\n--- FINANCIAL ANALYSIS ---")
        summary_parts.append(state["finance"])
    
    if state.get("operations"):
        summary_parts.append("\n--- OPERATIONAL ANALYSIS ---")
        summary_parts.append(state["operations"])
    
    # Add structured results if available
    if state.get("compliance_risks"):
        summary_parts.append("\n--- STRUCTURED COMPLIANCE RISKS ---")
        summary_parts.append(str(state["compliance_risks"]))
    
    if state.get("finance_risks"):
        summary_parts.append("\n--- STRUCTURED FINANCIAL RISKS ---")
        summary_parts.append(str(state["finance_risks"]))
    
    summary_parts.append("\n" + "=" * 60)
    
    return "\n".join(summary_parts)


# Example usage
if __name__ == "__main__":
    # Example plan
    example_plan = {
        "agents": ["LegalAgent", "ComplianceAgent", "FinanceAgent"],
        "execution_order": ["LegalAgent", "ComplianceAgent", "FinanceAgent"],
        "reasoning": "Query requires legal, compliance, and financial analysis"
    }
    
    print("Building graph from plan...")
    print(f"Agents: {example_plan['agents']}")
    print(f"Execution order: {example_plan['execution_order']}")
    
    try:
        graph = build_graph(example_plan)
        print("\n✓ Graph built successfully (sequential)")
        
        parallel_graph = build_parallel_graph(example_plan)
        print("✓ Parallel graph built successfully")
        
        # Example state
        example_state = AgentState(
            query="Analyze contract risks",
            legal="Legal analysis here...",
            compliance="Compliance analysis here...",
            finance="Financial analysis here...",
            operations=None,
            legal_clauses=None,
            compliance_risks=None,
            finance_risks=None,
            agent_context=None,
            final_summary=None
        )
        
        summary = create_agent_summary(example_state)
        print("\n" + summary)
        
    except ImportError as e:
        print(f"\n⚠ Note: Agent modules not yet created")
        print(f"   Error: {str(e)}")
        print("   This is expected if you're building the system incrementally")
