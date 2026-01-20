# Quick Start Guide: Advanced Features

## Overview

You now have access to 4 major new features that make contract analysis faster, structured, and persistent:

1. **Parallel Processing** - Run multiple agents concurrently
2. **Structured Extraction** - Get JSON-formatted results, not just text
3. **Multi-Turn Interaction** - Agents building on each other's findings
4. **Result Caching** - Store and retrieve analyses from Pinecone

---

## Feature 1: Structured Extraction (Start Here!)

### What It Does
Instead of plain text responses, agents return structured JSON with:
- Compliance violations and missing clauses
- Financial risks and payment terms
- Legal clauses and liability caps
- Operational constraints and SLAs

### How to Use

```python
from ai_agents.structured_extraction import (
    ComplianceExtractionPipeline,
    FinancialRiskExtractionPipeline,
    MultiDomainClauseExtractor
)

# Get compliance risks as structured JSON
compliance = ComplianceExtractionPipeline.extract_compliance_risks(
    context="contract text here...",
    query="What are the compliance risks?"
)

# Result format:
# {
#     "status": "success",
#     "data": {
#         "regulations_violated": [...],
#         "missing_clauses": [...],
#         "overall_compliance_score": 85,
#         "priority_actions": [...]
#     }
# }

if compliance["status"] == "success":
    print(f"Compliance Score: {compliance['data']['overall_compliance_score']}")
    for violation in compliance['data']['regulations_violated']:
        print(f"  - {violation['regulation']}: {violation['description']}")
```

### Available Pipelines
- `ComplianceExtractionPipeline.extract_compliance_risks()`
- `FinancialRiskExtractionPipeline.extract_financial_risks()`
- `MultiDomainClauseExtractor.extract_clauses()`

---

## Feature 2: Result Caching (Quick Retrieval)

### What It Does
Stores analysis results in Pinecone so you can:
- Retrieve the same analysis without re-running
- Find similar past analyses
- Build a searchable audit trail

### How to Use

```python
from ai_agents.intermediates_storage import IntermediatesStorage

# Store results
IntermediatesStorage.store_intermediate_result(
    query="Analyze payment terms",
    agent_name="FinanceAgent",
    result={"payment_obligations": [...]},
    analysis_type="financial_risk"
)

# Retrieve exact result
cached = IntermediatesStorage.retrieve_intermediate_result(
    query="Analyze payment terms",
    agent_name="FinanceAgent"
)

if cached:
    print("Retrieved cached analysis:", cached)

# Find similar past analyses
similar = IntermediatesStorage.retrieve_similar_queries(
    query="New contract payment analysis",
    top_k=3
)

for similar_result in similar:
    print(f"Similar: {similar_result['query']}")
    print(f"  Similarity: {similar_result['similarity_score']:.2f}")
```

---

## Feature 3: Multi-Turn Agent Interaction

### What It Does
Agents now see previous findings and can build sophisticated cross-domain analysis:

```
Legal Agent → identifies liability gaps
              ↓
Compliance Agent → recognizes regulatory exposure (using Legal findings)
                   ↓
Finance Agent → quantifies financial impact (using Legal + Compliance)
                 ↓
Operations Agent → proposes execution plan (using all previous findings)
```

### How It Works (Automatic)
You don't need to do anything special - it's built into the agents:

```python
from ai_agents.planner import PlanningModule
from ai_agents.graph import build_parallel_graph, AgentState

planner = PlanningModule()
plan = planner.generate_plan("Analyze all aspects")
graph = build_parallel_graph(plan)

# Run once - agents automatically use each other's context
result = graph.invoke(AgentState({"query": "Analyze all aspects"}))

# result now contains cumulative analysis from all domains
```

### Access Multi-Turn Context
```python
# Each agent extends the shared context
print(result.get("agent_context"))
# Output:
# Legal Agent Findings: ...
# Compliance Agent Findings: ... (includes Legal context)
# Finance Agent Findings: ... (includes Legal + Compliance context)
# Operations Agent Findings: ... (full context)
```

---

## Feature 4: Parallel Processing

### What It Does
Runs multiple agents at the same time (when possible) instead of one-by-one.

### Performance Gain
- **Before**: 4 agents × 5 seconds each = 20 seconds
- **After**: All agents run mostly in parallel = 5-7 seconds

### How to Enable
```python
from ai_agents.graph import build_parallel_graph

# Use parallel graph builder (vs original sequential)
plan = planner.generate_plan("Query")
graph = build_parallel_graph(plan)  # ← enables parallelism
```

---

## Complete Example: All Features Together

```python
from ai_agents.planner import PlanningModule
from ai_agents.graph import build_parallel_graph, AgentState
from ai_agents.intermediates_storage import IntermediatesStorage
import json

# Initialize
planner = PlanningModule()

# Step 1: Plan which agents to run
query = "Analyze contract for compliance, financial, and operational risks"
plan = planner.generate_plan(query)
print(f"Will run agents: {plan['execution_order']}")

# Step 2: Build parallel graph
graph = build_parallel_graph(plan)

# Step 3: Execute (agents run in parallel + multi-turn context)
print("\nAnalyzing contract...")
result = graph.invoke(AgentState({"query": query}))

# Step 4: Access results
print("\n=== RESULTS ===")
print(f"\nCompliance Risks:")
if result.get("compliance_risks"):
    print(json.dumps(result["compliance_risks"], indent=2))

print(f"\nFinancial Risks:")
if result.get("finance_risks"):
    print(json.dumps(result["finance_risks"], indent=2))

# Step 5: Store in Pinecone for later retrieval
print("\nCaching results...")
IntermediatesStorage.store_multi_agent_results(
    query=query,
    results={
        "legal": {"analysis": result["legal"]},
        "compliance": result.get("compliance_risks", {}),
        "finance": result.get("finance_risks", {}),
        "operations": {"analysis": result["operations"]}
    }
)

# Step 6: Retrieve same analysis later
print("\nRetrieving cached compliance analysis...")
cached = IntermediatesStorage.retrieve_intermediate_result(
    query=query,
    agent_name="ComplianceAgent"
)
if cached:
    print("✓ Successfully retrieved from cache")
```

---

## Common Use Cases

### Use Case 1: Get Structured Risk Scores
```python
from ai_agents.structured_extraction import ComplianceExtractionPipeline

result = ComplianceExtractionPipeline.extract_compliance_risks(context, query)
score = result["data"]["overall_compliance_score"]

if score < 50:
    print("❌ High compliance risk!")
elif score < 75:
    print("⚠️  Medium compliance risk")
else:
    print("✅ Good compliance posture")
```

### Use Case 2: Find Historical Similar Contracts
```python
from ai_agents.intermediates_storage import IntermediatesStorage

similar = IntermediatesStorage.retrieve_similar_queries(
    query="new contract",
    analysis_type="compliance_risk",
    top_k=5
)

print(f"Found {len(similar)} similar contracts analyzed before")
for s in similar:
    print(f"  • {s['query']} (similarity: {s['similarity_score']:.1%})")
```

### Use Case 3: Multi-Domain Analysis with Context
```python
# Automatically leverages all agents + multi-turn
result = graph.invoke(AgentState({"query": query}))

# All domains analyzed with full context
print("Legal analysis:", result["legal"])
print("With compliance context:", result.get("agent_context"))
```

---

## Testing

### Run the test suite to see all features in action:
```bash
python test_parallel_and_multiturn.py
```

This will:
- ✅ Test parallel agent execution
- ✅ Demonstrate structured extraction
- ✅ Show intermediates storage
- ✅ Display multi-turn interaction
- ✅ Generate sample results

---

## File Reference

### New Files
- `ai_agents/structured_extraction.py` - Structured extraction pipelines
- `ai_agents/intermediates_storage.py` - Pinecone caching
- `test_parallel_and_multiturn.py` - Complete test suite
- `ADVANCED_FEATURES.md` - Detailed technical documentation

### Modified Files
- `ai_agents/graph.py` - Parallel support + extended state
- `ai_agents/agents/compliance_agent.py` - Structured extraction
- `ai_agents/agents/finance_agent.py` - Structured extraction
- `ai_agents/agents/legal_agent.py` - Multi-turn support
- `ai_agents/agents/operations_agent.py` - Multi-turn support

---

## Next Steps

1. **Run the test**: `python test_parallel_and_multiturn.py`
2. **Try structured extraction** with your own contract text
3. **Store results** in Pinecone for quick retrieval
4. **Build a report generator** using the structured JSON outputs
5. **Optimize** the pipelines for your specific contract types

---

## Troubleshooting

**Q: Structured extraction returns error status**
A: Check that your contract context isn't too long (>5000 chars). Summarize first or reduce context.

**Q: Pinecone storage failing**
A: Ensure Pinecone API key and index name are in your .env file. Check that index supports metadata storage.

**Q: Agents not using multi-turn context**
A: Multi-turn is automatic! Check `result["agent_context"]` to see accumulated findings.

**Q: Parallel execution still feels slow**
A: Verify you're using `build_parallel_graph()` not the old `build_graph()`. Also check your Gemini API rate limits.

---

## Support

For detailed technical documentation, see [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)

For architecture overview, see [.github/copilot-instructions.md](.github/copilot-instructions.md)
