# AI Agents Contract Analysis System - Copilot Instructions

## Architecture Overview

This is a **multi-agent contract analysis system** using LangGraph orchestration. It combines three layers:

1. **Document Processing**: Load, parse, and embed contracts (via Pinecone + Sentence Transformers)
2. **Agentic Planning**: Dynamic agent selection based on query content (`planner.py`)
3. **Specialized Agents**: Domain-specific analysis (legal, compliance, finance, operations)

### Key Data Flow

```
User Query
  ↓
Planner (determines relevant agents)
  ↓
LangGraph builds execution order dynamically
  ↓
Each Agent: retrieve_chunks(query) → Prompt with context → LLM response
  ↓
Combined results in AgentState
```

## Critical Patterns

### 1. Specialized Agents Pattern
- All agents (legal, compliance, finance, operations) follow identical structure in `ai_agents/agents/`:
  ```python
  def agent_name(state):
      context = retrieve_chunks(state["query"])
      prompt = PromptTemplates.get_agent_prompt(context, question)
      response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
      state["field"] = result
      return state
  ```
- Each agent updates ONE field in `AgentState` TypedDict (e.g., `state["legal"]`, `state["finance"]`)
- State flows through LangGraph edges defined by planner's `execution_order`

### 2. Vector Retrieval (RAG Pattern)
- All agents use identical helper functions:
  - `embed_query(q)` → encodes query using `SentenceTransformer("BAAI/bge-large-en-v1.5")`
  - `retrieve_chunks(query)` → returns top-3 Pinecone matches with metadata
- Context format: `"\n\n".join([m["metadata"]["chunk_text"] for m in matches])`
- Pinecone index initialized globally in agent files (anti-pattern but consistent across codebase)

### 3. LLM Provider Choice
- **Main agents** (`ai_agents/agents/`) use **Google Gemini** (`gemini-2.5-flash`)
- **Alternative implementation** (`multi_agent_analyzer.py`) uses **Groq** (`mixtral-8x7b-32768`)
- LLM calls are simple: `client.models.generate_content(model=X, contents=prompt)`
- **Note**: Use `gemini-2.5-flash` or `gemini-2.5-pro` (v1.5 models are deprecated)
- No streaming or tool-use patterns implemented

### 4. Dynamic Agent Orchestration
- `PlanningModule.generate_plan(query)` calls Gemini with structured prompt asking for JSON
- Returns `{"agents": [...], "execution_order": [...], "reasoning": "..."}`
- Falls back to keyword-based selection if JSON parsing fails (see `fallback_plan()`)
- LangGraph builds graph with agents in `execution_order`, chains them with edges

### 5. Prompt Template Convention
- All prompts centralized in `ai_agents/prompt_templates.py`
- Template method: `get_agent_prompt(role, context, question, instructions)` wraps specifics
- Structure: role → context excerpts → task/instructions → question → request for structured answer

## Environment & Dependencies

**Required .env variables:**
```
GEMINI_API_KEY          # Google AI Studio key
GEMINI_MODEL            # Model name (default: gemini-2.5-flash)
PINECONE_API_KEY        # Vector DB access
PINECONE_INDEX          # Index name
GROQ_API_KEY           # Optional, for multi_agent_analyzer.py
```

**Key packages:**
- `langgraph` (0.x) - agent orchestration
- `sentence-transformers` - embeddings (BAAI/bge model)
- `pinecone-client` - vector retrieval
- `google-genai` - Gemini LLM
- `fastapi` - REST API (`api.py`)

## Developer Workflows

### Adding a New Specialized Agent
1. Create `ai_agents/agents/your_agent.py` matching structure in `legal_agent.py`
2. Define state field in `AgentState` TypedDict in `ai_agents/graph.py`
3. Add prompt method to `PromptTemplates` class
4. Import and add node in `build_graph()` function
5. Add keyword mapping in planner's `fallback_plan()` for keyword-based fallback

### Processing a New Contract
1. Use `api.py` POST `/upload-contract` endpoint to upload file
2. Internally calls: `load_document()` → `split_document()` → `embed_and_upload()` (to Pinecone)
3. Query using `query_contract.py` or via `multi_agent_analyzer.py` directly

### Testing Query Flow
```python
from ai_agents.planner import PlanningModule
from ai_agents.graph import build_graph, AgentState

planner = PlanningModule()
plan = planner.generate_plan("Your query")
graph = build_graph(plan)
result = graph.invoke(AgentState({"query": "Your query"}))
```

## File Organization

- `ai_agents/main.py` - Entry point for orchestration demo
- `ai_agents/graph.py` - LangGraph state & builder
- `ai_agents/planner.py` - Dynamic agent selection
- `ai_agents/agents/*.py` - Individual agent implementations
- `api.py` - FastAPI wrapper for contract upload/analysis
- `multi_agent_analyzer.py` - Alternative pipeline using Groq (kept for comparison)
- `document_parser.py`, `embed_and_upsert.py` - Utility functions for document processing

## Important Implementation Notes

- **Global state duplication**: Both `ai_agents/agents/` and `multi_agent_analyzer.py` redefine identical embedding/Pinecone setup (not DRY)
- **No error handling**: Agent functions assume successful LLM responses; no retry/fallback logic
- **Stateless agents**: Each agent execution is independent; no context persistence between queries
- **JSON fallback**: Planner gracefully falls back to keyword matching if LLM returns invalid JSON
