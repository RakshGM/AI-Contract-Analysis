# Quick Reference Guide

## 🚀 Command Cheat Sheet

### Installation & Setup
```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the System

```bash
# Web UI (recommended)
python api_enhanced.py
# Then visit: http://localhost:8000

# CLI Analysis
python -m ai_agents.main

# Run Tests
python tests_comprehensive.py

# Pinecone Setup
python pinecone_setup.py
```

---

## 📝 Code Examples

### Simple Analysis
```python
from ai_agents.main import run

result = run("Analyze for compliance risks")
print(result["compliance_risks"])
```

### Generate Report
```python
from ai_agents.report_generator import create_report

report = create_report(result, tone="executive", format_type="markdown")
```

### Batch Processing
```python
from ai_agents.concurrent_processor import process_contracts_parallel

contracts = [("id1", "file1.txt", "query1"), ("id2", "file2.txt", "query2")]
results = process_contracts_parallel(contracts, max_concurrent=3)
```

### Store & Retrieve
```python
from ai_agents.intermediates_storage import IntermediatesStorage

# Store
IntermediatesStorage.store_intermediate_result(query, agent_name, result)

# Retrieve
cached = IntermediatesStorage.retrieve_intermediate_result(query, agent_name)

# Find similar
similar = IntermediatesStorage.retrieve_similar_queries(query, top_k=5)
```

---

## 🎨 Report Customization

### Tones
- `executive` - High-level, business-focused
- `technical` - Detailed, technical language
- `legal` - Formal, legally precise
- `casual` - Accessible, plain language

### Formats
- `markdown` - Document format
- `json` - Structured data
- `html` - Web page
- `text` - Plain text

### Focus Areas
- `risks` - Emphasize risks
- `opportunities` - Highlight positive
- `compliance` - Regulatory focus
- `financial` - Cost focus
- `balanced` - Equal coverage

### Example
```python
from ai_agents.report_generator import ReportConfig, ReportTone, ReportFormat, ReportFocus

config = ReportConfig(
    tone=ReportTone.LEGAL,
    format=ReportFormat.HTML,
    focus=ReportFocus.COMPLIANCE,
    include_recommendations=True
)
report = ReportGenerator.generate(state, config)
```

---

## 📊 Key Modules

| Module | Purpose | Key Function |
|--------|---------|--------------|
| `planner.py` | Agent selection | `generate_plan(query)` |
| `graph.py` | Orchestration | `build_parallel_graph(plan)` |
| `parallel_processor.py` | Async execution | `ParallelProcessor.run_parallel()` |
| `structured_extraction.py` | JSON extraction | `ComplianceExtractionPipeline.extract_compliance_risks()` |
| `intermediates_storage.py` | Caching | `IntermediatesStorage.store_intermediate_result()` |
| `report_generator.py` | Reports | `ReportGenerator.generate()` |
| `concurrent_processor.py` | Batch processing | `process_contracts_parallel()` |

---

## ⚙️ Configuration

### .env File
```env
GEMINI_API_KEY=your-key
PINECONE_API_KEY=your-key
PINECONE_INDEX=contract-analysis
GROQ_API_KEY=optional-key
GEMINI_MODEL=gemini-1.5-flash
```

### Agent Roles
- **Legal**: Liability, indemnity, termination, jurisdiction
- **Compliance**: GDPR, ISO, audit, policy
- **Finance**: Payment, pricing, penalties, tax
- **Operations**: SLA, uptime, delivery, support

---

## 📈 Performance Metrics

| Mode | Time | Use Case |
|------|------|----------|
| Sequential | 20-30s | Default |
| Parallel | 7-10s | Multiple agents |
| Cached | 2-3s | Repeated queries |
| Batch (10x) | ~30s | Multiple contracts |

---

## 🧪 Testing

```bash
# All tests
python tests_comprehensive.py

# Specific class
python -m unittest tests_comprehensive.TestStructuredPipelines

# With verbose output
python -m unittest tests_comprehensive -v

# Specific test method
python -m unittest tests_comprehensive.TestStructuredPipelines.test_compliance_extraction_returns_valid_structure
```

---

## 🔍 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| API key not found | Add to `.env` |
| Pinecone connection failed | Run `python pinecone_setup.py` |
| Slow execution | Use `build_parallel_graph()` |
| Missing dependencies | Run `pip install -r requirements.txt` |
| Import errors | Ensure virtual environment activated |

---

## 📚 File Reference

### Main Files
- `api_enhanced.py` - Web server with UI
- `ai_agents/main.py` - CLI entry point
- `tests_comprehensive.py` - Full test suite

### Configuration
- `.env` - Environment variables
- `requirements.txt` - Python dependencies

### Documentation
- `PROJECT_DOCUMENTATION.md` - Full system guide
- `IMPLEMENTATION_GUIDE.md` - Implementation details
- `QUICKSTART.md` - Quick start (if exists)
- `ADVANCED_FEATURES.md` - Advanced usage (if exists)

---

## 🎯 Next Steps

1. **Setup**: Configure `.env` with API keys
2. **Test**: Run `python tests_comprehensive.py`
3. **Run**: Start UI with `python api_enhanced.py`
4. **Analyze**: Upload contracts or enter text
5. **Customize**: Generate reports with preferred settings
6. **Scale**: Use batch processor for multiple contracts

---

## 💡 Pro Tips

1. **Faster Analysis**: Use parallel mode and cache results
2. **Better Reports**: Customize tone and focus for audience
3. **Cost Savings**: Enable caching for repeated queries
4. **Batch Processing**: Analyze 10+ contracts concurrently
5. **Multi-Turn**: Agents automatically use previous findings
6. **JSON Export**: Get structured data from extraction pipelines

---

## 📞 Support

- Full docs: See `PROJECT_DOCUMENTATION.md`
- Examples: Check module docstrings
- Tests: Review `tests_comprehensive.py`
- Issues: Check troubleshooting section

---

**Ready to analyze contracts? Start with:**
```bash
python api_enhanced.py
```

Then visit: **http://localhost:8000**

