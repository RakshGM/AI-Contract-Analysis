"""
Planning module for dynamic agent selection
"""

import os
import json
from typing import Dict, Any, List
from dotenv import load_dotenv
from ai_agents.prompt_templates import PromptTemplates

try:
    from groq import Groq
except ImportError:
    Groq = None

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class PlanningModule:
    """
    Intelligent planning module that determines which agents should analyze a query
    """
    
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        """
        Initialize planning module
        
        Args:
            model_name: Groq model to use for planning
        """
        self.model_name = model_name
        if not GROQ_API_KEY or Groq is None:
            print("⚠ Warning: GROQ_API_KEY not found. Planner will use fallback keyword matching.")
    
    def generate_plan(self, query: str) -> Dict[str, Any]:
        """
        Generate execution plan for the query
        
        Args:
            query: User query
            
        Returns:
            Plan dictionary with agents, execution_order, and reasoning
        """
        if not GROQ_API_KEY or Groq is None:
            print("Using fallback planning (no GROQ_API_KEY)")
            return self.fallback_plan(query)
        
        try:
            # Get planning prompt
            prompt = PromptTemplates.get_planner_prompt(query)
            
            # Call Groq
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=512
            )
            
            # Parse JSON response
            response_text = response.choices[0].message.content.strip()
            
            # Clean response (remove markdown code blocks if present)
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            
            plan = json.loads(response_text)
            
            # Validate plan structure
            if not all(key in plan for key in ["agents", "execution_order"]):
                print("⚠ Invalid plan structure, using fallback")
                return self.fallback_plan(query)
            
            return plan
        
        except json.JSONDecodeError as e:
            print(f"⚠ JSON parsing failed: {str(e)}")
            print("Using fallback planning")
            return self.fallback_plan(query)
        
        except Exception as e:
            print(f"⚠ Error generating plan: {str(e)}")
            print("Using fallback planning")
            return self.fallback_plan(query)
    
    def fallback_plan(self, query: str) -> Dict[str, Any]:
        """
        Fallback keyword-based planning when LLM is unavailable
        
        Args:
            query: User query
            
        Returns:
            Plan dictionary
        """
        query_lower = query.lower()
        
        # Keywords for each agent
        keywords = {
            "LegalAgent": ["legal", "liability", "indemnity", "termination", "jurisdiction", 
                          "contract", "enforce", "clause", "breach"],
            "ComplianceAgent": ["compliance", "regulatory", "gdpr", "iso", "audit", 
                               "policy", "regulation", "data protection", "privacy"],
            "FinanceAgent": ["payment", "financial", "price", "cost", "penalty", 
                            "tax", "invoice", "fee", "money", "dollar"],
            "OperationsAgent": ["sla", "service level", "uptime", "delivery", 
                               "support", "performance", "operational", "maintenance"]
        }
        
        # Determine which agents to include
        selected_agents = []
        for agent, agent_keywords in keywords.items():
            if any(keyword in query_lower for keyword in agent_keywords):
                selected_agents.append(agent)
        
        # If no specific match, include all agents
        if not selected_agents:
            selected_agents = list(keywords.keys())
        
        # Default execution order prioritizes legal → compliance → finance → operations
        agent_order = ["LegalAgent", "ComplianceAgent", "FinanceAgent", "OperationsAgent"]
        execution_order = [agent for agent in agent_order if agent in selected_agents]
        
        return {
            "agents": selected_agents,
            "execution_order": execution_order,
            "reasoning": f"Keyword-based selection: detected {len(selected_agents)} relevant agents"
        }
    
    def explain_plan(self, plan: Dict[str, Any]) -> str:
        """
        Generate human-readable explanation of the plan
        
        Args:
            plan: Plan dictionary
            
        Returns:
            Explanation string
        """
        explanation = []
        explanation.append("=" * 60)
        explanation.append("ANALYSIS PLAN")
        explanation.append("=" * 60)
        
        explanation.append(f"\nSelected Agents: {', '.join(plan['agents'])}")
        explanation.append(f"Execution Order: {' → '.join(plan['execution_order'])}")
        
        if plan.get("reasoning"):
            explanation.append(f"\nReasoning: {plan['reasoning']}")
        
        explanation.append("\nAgent Roles:")
        
        agent_descriptions = {
            "LegalAgent": "Analyzes legal enforceability, liability, and jurisdiction",
            "ComplianceAgent": "Ensures regulatory compliance (GDPR, ISO, etc.)",
            "FinanceAgent": "Identifies financial exposure and payment obligations",
            "OperationsAgent": "Validates operational feasibility and SLAs"
        }
        
        for agent in plan['agents']:
            if agent in agent_descriptions:
                explanation.append(f"  • {agent}: {agent_descriptions[agent]}")
        
        explanation.append("=" * 60)
        
        return "\n".join(explanation)


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Planning Module Test")
    print("=" * 60)
    
    planner = PlanningModule()
    
    # Test queries
    test_queries = [
        "What are the payment terms and financial penalties?",
        "Analyze all compliance and regulatory risks in this contract",
        "Review the entire contract for all types of risks",
        "What are the SLA requirements and uptime guarantees?",
        "Check for liability and indemnification clauses"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        
        plan = planner.generate_plan(query)
        explanation = planner.explain_plan(plan)
        
        print(explanation)
        print()
