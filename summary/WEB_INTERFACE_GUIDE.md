# 🌐 How to Use the Contract Analysis Web Interface

## ✅ Web Interface is Running!

**Local URL:** http://localhost:8501  
**Network URL:** http://192.168.174.45:8501

Open either URL in your web browser (Chrome, Firefox, Edge, etc.)

---

## 📋 Step-by-Step Guide to Analyze Contracts

### **Step 1: Open the Web Interface**
1. Click on: **http://localhost:8501** or paste it in your browser
2. You'll see the "AI-Powered Contract Analysis System" homepage

### **Step 2: Upload Your PDF Contract**
1. Go to the **"📝 Analysis"** tab (should be already selected)
2. Select **"Upload File"** radio button
3. Click **"Browse files"** button
4. Choose one of these files:
   - **sample_contract.pdf** (just created - includes legal, finance, operations, compliance)
   - Any other PDF/DOCX/TXT contract file you have

### **Step 3: Configure Analysis (Optional)**
On the left sidebar, you can customize:
- **Analysis Mode:** Quick Analysis / Comprehensive / Domain-Specific
- **Report Tone:** Executive / Technical / Legal / Casual
- **Report Format:** Markdown / HTML / JSON / Text
- **Report Focus:** Balanced / Risks / Opportunities / Compliance / Financial

### **Step 4: Run Analysis**
You have two options:

#### **Option A: Extract Clauses Only** (Fast)
- Click **"📑 Extract Clauses"** button
- This will extract all key clauses from 7 domains:
  - Payment Terms
  - Liability Caps
  - SLA Terms
  - Intellectual Property
  - Data Protection
  - Termination Conditions
  - Compliance Requirements

#### **Option B: Full Multi-Agent Analysis** (Comprehensive)
- Click **"🚀 Analyze Contract"** button
- This will:
  1. Run all 4 specialized agents (Legal, Compliance, Finance, Operations)
  2. Identify risks across all domains
  3. Calculate financial exposure
  4. Generate comprehensive report

### **Step 5: View Results**

After analysis completes, check these tabs:

#### **📊 Results Tab**
- View outputs from each agent:
  - **Legal Agent:** Liability risks, IP issues, termination concerns
  - **Compliance Agent:** GDPR/HIPAA gaps, regulatory requirements
  - **Finance Agent:** Payment obligations, penalty exposure, total costs
  - **Operations Agent:** SLA feasibility, resource adequacy, operational risks

#### **📋 Report Tab**
- View the generated comprehensive report
- Download report in your selected format
- Share with stakeholders

#### **📚 History Tab**
- See all previous analyses
- Re-run or compare results
- Provide feedback

---

## 📄 Sample Contract Content

The **sample_contract.pdf** we created includes:

### Legal Terms
- Liability cap: $1M per incident, $2.5M aggregate
- IP ownership with Provider
- Indemnification clauses
- 90-day termination notice

### Financial Terms
- $50,000/month service fees
- Net 30 payment terms
- 1.5% monthly late fee
- Up to $780,000 annual exposure
- Uncapped data breach liability

### Operational Requirements
- 99.9% uptime SLA (43 min/month downtime max)
- 1-hour critical response time
- 4-hour critical resolution time
- 24/7 support coverage

### Compliance Requirements
- GDPR compliance required
- HIPAA compliance (BAA missing!)
- SOC 2 Type II certification
- AES-256 encryption
- Quarterly penetration testing

### Risk Highlights
- **HIGH:** Uncapped data breach liability
- **HIGH:** Aggressive SLA targets
- **MEDIUM:** Missing HIPAA BAA
- **MEDIUM:** No force majeure clause

---

## 🎯 Example Analysis Queries

When uploading a contract, try these specific queries:

1. **Legal Focus:**
   - "What are the liability risks and termination conditions?"
   - "Analyze intellectual property ownership issues"

2. **Financial Focus:**
   - "Calculate total financial exposure including penalties"
   - "What are all payment obligations and late fees?"

3. **Operational Focus:**
   - "Is the 99.9% uptime SLA achievable?"
   - "Evaluate resource allocation and operational risks"

4. **Compliance Focus:**
   - "Identify all compliance requirements and gaps"
   - "Check GDPR, HIPAA, and SOC 2 compliance"

5. **Comprehensive:**
   - "Analyze all risks and provide recommendations"
   - "Full contract review across all domains"

---

## 🚨 Important Notes

### API Rate Limits
- **Free Tier:** 20 requests/day for Gemini API
- If you hit the limit, you'll see quota errors
- Wait ~20 seconds or use a paid API key

### File Support
- ✅ **PDF** - Fully supported (pypdf extraction)
- ✅ **DOCX** - Fully supported (python-docx extraction)
- ✅ **TXT** - Fully supported (direct text)
- File size: Recommended < 10MB

### Performance
- **Clause Extraction:** 2-5 seconds
- **Single Agent:** 5-10 seconds
- **Full Analysis (4 agents):** 15-30 seconds
- **Report Generation:** < 1 second

---

## 🔧 Troubleshooting

### "Module not found" errors
```bash
pip install streamlit pypdf python-docx
```

### "API quota exceeded"
- Wait for quota reset (daily limit)
- Or upgrade to paid Gemini API tier

### "Cannot read PDF"
- Ensure PDF is not password-protected
- Try converting to TXT first
- Check PDF is not corrupted

### Web page not loading
- Check terminal shows "Local URL: http://localhost:8501"
- Try refreshing browser (Ctrl+F5)
- Check firewall isn't blocking port 8501

---

## 📥 Where to Get Contract Files

### Use Our Sample
- **sample_contract.pdf** in `C:\AI-Tools\` directory
- Contains all 4 analysis domains

### Upload Your Own
- Any business contract (SaaS, employment, vendor, etc.)
- Service agreements
- Master service agreements (MSA)
- Statements of work (SOW)
- NDAs, partnership agreements

---

## 🎉 Quick Start Command

Already done! The interface is running at:
👉 **http://localhost:8501**

Just open your browser and start uploading contracts!

---

## 📧 Support

If you need help:
1. Check terminal output for error messages
2. Verify .env file has API keys configured
3. Ensure all dependencies are installed

**Current Status:** ✅ System running and ready!
