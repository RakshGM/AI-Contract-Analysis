# System Architecture Diagram

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    AI-POWERED CONTRACT ANALYSIS SYSTEM                    ║
║                          Production v2.0                                  ║
╚══════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACES                                  │
├────────────────────┬──────────────────────┬────────────────────────────┤
│   Streamlit Web UI  │     REST API         │      CLI Scripts          │
│                     │   (FastAPI)          │    (Python)               │
│  • Interactive      │  • /analyze          │  • quickstart_demo.py     │
│  • File Upload      │  • /batch-analyze    │  • test_*.py              │
│  • Real-time        │  • /extract-clauses  │                           │
│  • Reports          │  • /upload           │                           │
│  • History          │  • /job/{id}         │                           │
└────────────────────┴──────────────────────┴────────────────────────────┘
                                  ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                       ORCHESTRATION LAYER                                 │
├─────────────────┬───────────────────┬──────────────────┬────────────────┤
│  Planning       │   LangGraph       │  Batch           │  Parallel      │
│  Module         │   Orchestrator    │  Processor       │  Processor     │
│                 │                   │                  │                │
│ • Auto-select   │ • State mgmt      │ • Multi-contract │ • Async exec   │
│   agents        │ • Sequential      │ • Concurrent     │ • Dependency   │
│ • Keyword       │   execution       │   processing     │   tracking     │
│   fallback      │ • Context share   │ • Job tracking   │                │
└─────────────────┴───────────────────┴──────────────────┴────────────────┘
                                  ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         AGENT LAYER (4 Specialized Agents)                │
├──────────────┬──────────────┬──────────────┬──────────────────────────┤
│ Legal Agent  │ Compliance   │ Finance      │ Operations Agent         │
│              │ Agent        │ Agent        │                          │
│ • Liability  │ • GDPR       │ • Payments   │ • SLA feasibility        │
│ • IP rights  │ • HIPAA      │ • Penalties  │ • Timelines              │
│ • Termination│ • SOC 2      │ • Exposure   │ • Resource adequacy      │
│ • Indemnif.  │ • Audit req  │ • Cost calc  │ • Operational risks      │
└──────────────┴──────────────┴──────────────┴──────────────────────────┘
                                  ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    EXTRACTION & PROCESSING LAYER                          │
├────────────────────────┬─────────────────────┬─────────────────────────┤
│  Multi-Domain          │  Compliance         │  Financial Risk         │
│  Clause Extractor      │  Pipeline           │  Pipeline               │
│                        │                     │                         │
│ • Payment terms        │ • Regulatory gaps   │ • Payment obligations   │
│ • Liability caps       │ • Missing clauses   │ • Penalty exposure      │
│ • IP clauses           │ • Compliance score  │ • Total cost estimate   │
│ • SLA terms            │ • Priority actions  │ • Uncapped liabilities  │
│ • Termination          │ • Timeline          │ • Mitigation needs      │
│ • Data protection      │                     │                         │
└────────────────────────┴─────────────────────┴─────────────────────────┘
                                  ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        AI & STORAGE INFRASTRUCTURE                        │
├───────────────────────┬──────────────────────┬─────────────────────────┤
│  Google Gemini AI     │   Pinecone Vector    │  Document Parser        │
│  (LLM)                │   Database           │                         │
│                       │                      │                         │
│ • gemini-2.5-flash    │ • RAG retrieval      │ • TXT support           │
│ • Analysis generation │ • Embeddings store   │ • PDF support (planned) │
│ • Structured output   │ • Intermediate cache │ • DOCX support (planned)│
│ • Multi-turn context  │ • Similar queries    │ • Chunking              │
└───────────────────────┴──────────────────────┴─────────────────────────┘
                                  ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         OUTPUT GENERATION LAYER                           │
├──────────────────────┬───────────────────────┬────────────────────────┤
│  Report Generator    │  Intermediates        │  Structured Data       │
│                      │  Storage              │  Export                │
│                      │                       │                        │
│ Formats:             │ • Store results       │ • JSON extraction      │
│ • Markdown           │ • Retrieve cached     │ • Risk scores          │
│ • HTML               │ • Multi-agent merge   │ • Clause mappings      │
│ • JSON               │ • Query similarity    │ • Metrics              │
│ • Text               │                       │                        │
│                      │                       │                        │
│ Tones:               │                       │                        │
│ • Executive          │                       │                        │
│ • Technical          │                       │                        │
│ • Legal              │                       │                        │
│ • Casual             │                       │                        │
│                      │                       │                        │
│ Focus:               │                       │                        │
│ • Balanced           │                       │                        │
│ • Risks              │                       │                        │
│ • Opportunities      │                       │                        │
│ • Compliance         │                       │                        │
│ • Financial          │                       │                        │
└──────────────────────┴───────────────────────┴────────────────────────┘
                                  ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                            OUTPUT DELIVERY                                │
├──────────────────────────────────────────────────────────────────────────┤
│  • Downloadable reports (4 formats)                                       │
│  • Interactive UI displays                                                │
│  • JSON API responses                                                     │
│  • Saved analysis history                                                 │
│  • Email delivery (planned)                                               │
└──────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                            DATA FLOW EXAMPLE
═══════════════════════════════════════════════════════════════════════════

1. USER INPUT
   ↓
   "Analyze this contract for SLA compliance and financial risks"
   
2. PLANNING
   ↓
   Planner selects: [ComplianceAgent, FinanceAgent, OperationsAgent]
   
3. EXECUTION
   ↓
   ComplianceAgent → analyzes GDPR, HIPAA, audit requirements
   ↓
   FinanceAgent → calculates penalty exposure, payment obligations
   ↓
   OperationsAgent → evaluates 99.9% uptime, 4-hour resolution SLA
   
4. AGGREGATION
   ↓
   AgentState combines all findings with context sharing
   
5. REPORT GENERATION
   ↓
   ReportGenerator creates customized report (tone: executive, format: markdown)
   
6. OUTPUT
   ↓
   User receives comprehensive analysis with recommendations


═══════════════════════════════════════════════════════════════════════════
                         PERFORMANCE METRICS
═══════════════════════════════════════════════════════════════════════════

┌────────────────────────┬──────────────┬───────────────────────────────┐
│ Operation              │ Avg Time     │ Notes                         │
├────────────────────────┼──────────────┼───────────────────────────────┤
│ Clause Extraction      │ 2-5 sec      │ All 7 domains                 │
│ Single Agent Analysis  │ 5-10 sec     │ Per agent                     │
│ Full Analysis (4 agents)│ 10-30 sec   │ Sequential execution          │
│ Report Generation      │ < 1 sec      │ All formats                   │
│ Batch (3 contracts)    │ 15-45 sec    │ Concurrent processing         │
│ Storage/Retrieval      │ < 500ms      │ Pinecone cache                │
└────────────────────────┴──────────────┴───────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                          TECHNOLOGY STACK
═══════════════════════════════════════════════════════════════════════════

┌───────────────────┬────────────────────────────────────────────────────┐
│ Layer             │ Technology                                         │
├───────────────────┼────────────────────────────────────────────────────┤
│ LLM               │ Google Gemini 2.5 Flash                            │
│ Orchestration     │ LangGraph 1.0+                                     │
│ Vector DB         │ Pinecone 8.0+                                      │
│ Embeddings        │ Sentence Transformers (BAAI/bge-large-en-v1.5)     │
│ Web UI            │ Streamlit 1.x                                      │
│ API               │ FastAPI 0.128+                                     │
│ Document Parse    │ pypdf, python-docx, openpyxl                       │
│ Language          │ Python 3.9+                                        │
└───────────────────┴────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                    DEPLOYMENT ARCHITECTURE (Recommended)
═══════════════════════════════════════════════════════════════════════════

                         ┌─────────────────┐
                         │   Load Balancer │
                         └────────┬────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
            ┌───────────────┐          ┌───────────────┐
            │  Streamlit UI │          │  FastAPI      │
            │  Container    │          │  Container    │
            └───────┬───────┘          └───────┬───────┘
                    │                          │
                    └──────────┬───────────────┘
                               ▼
                    ┌─────────────────────┐
                    │  Agent Worker Pool  │
                    │  (Auto-scaling)     │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
         ┌──────────┐   ┌──────────┐   ┌──────────┐
         │ Gemini   │   │ Pinecone │   │  Redis   │
         │ API      │   │ Vector DB│   │  Cache   │
         └──────────┘   └──────────┘   └──────────┘


═══════════════════════════════════════════════════════════════════════════
                          SYSTEM STATUS: ✅ PRODUCTION READY
═══════════════════════════════════════════════════════════════════════════
```
