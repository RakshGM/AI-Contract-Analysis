"""
Streamlit UI for AI-Powered Contract Analysis System
Provides a polished interface for multi-domain contract analysis
"""

import streamlit as st
import asyncio
from datetime import datetime
from ai_agents import (
    PlanningModule,
    build_graph,
    AgentState,
    MultiDomainClauseExtractor,
    ComplianceExtractionPipeline,
    FinancialRiskExtractionPipeline,
    IntermediatesStorage,
    BatchProcessor
)
from ai_agents.report_generator import (
    ReportGenerator,
    ReportConfig,
    ReportTone,
    ReportFormat,
    ReportFocus
)

# Page configuration
st.set_page_config(
    page_title="AI Contract Analysis",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI/UX
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Poppins:wght@400;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main {
        background: #ffffff !important;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        color: #000000 !important;
    }
    
    .main * {
        color: #000000;
    }
    
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: #000000 !important;
    }
    
    .main p, .main span, .main div {
        color: #000000 !important;
    }
    
    /* Header Styles */
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #1a1a1a;
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: #000000;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 600;
    }
    
    /* Section Headers */
    .section-header {
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #000000;
        border-bottom: 4px solid #667eea;
        padding-bottom: 0.8rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
    }
    
    /* Card Styles */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    
    /* Agent Cards */
    .agent-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-top: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
    }
    
    .agent-card.legal {
        border-top-color: #3b82f6;
    }
    
    .agent-card.compliance {
        border-top-color: #8b5cf6;
    }
    
    .agent-card.finance {
        border-top-color: #10b981;
    }
    
    .agent-card.operations {
        border-top-color: #f59e0b;
    }
    
    /* Risk Level Badges */
    .risk-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.2rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .risk-critical {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: white;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .risk-info {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
    }
    
    /* Status Indicators */
    .status-success {
        color: #10b981;
        font-weight: 600;
    }
    
    .status-warning {
        color: #f59e0b;
        font-weight: 600;
    }
    
    .status-error {
        color: #ef4444;
        font-weight: 600;
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #f3f4f6 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .feature-card:hover {
        border-color: #667eea;
        transform: scale(1.05);
        box-shadow: 0 15px 40px rgba(102,126,234,0.3);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #000000;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        font-family: 'Inter', sans-serif;
        color: #000000;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    /* Progress Bar */
    .progress-container {
        background: #e5e7eb;
        border-radius: 10px;
        overflow: hidden;
        height: 30px;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        transition: width 0.3s ease;
    }
    
    /* Button Enhancements */
    .stButton>button {
        background: #0066cc !important;
        color: white !important;
        border: 2px solid #0066cc !important;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,102,204,0.3);
    }
    
    .stButton>button:hover {
        background: #0052a3 !important;
        border-color: #0052a3 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,102,204,0.5);
    }
    
    .stButton>button:active {
        background: #003d7a !important;
        transform: translateY(0px);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stCheckbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div {
        color: white !important;
        font-family: 'Inter', sans-serif;
    }
    
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #6c757d;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* File Uploader Styling */
    .uploadedFile {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px dashed #10b981;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Success/Warning/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 5px solid #10b981;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 5px solid #f59e0b;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 5px solid #ef4444;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 5px solid #3b82f6;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: #f3f4f6;
        border-radius: 10px;
        font-weight: 700;
        color: #000000 !important;
    }
    
    /* Input Field Styling */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border: 2px solid #d1d5db;
        border-radius: 10px;
        padding: 0.75rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        background: white !important;
        color: #000000 !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #0066cc;
        box-shadow: 0 0 0 3px rgba(0,102,204,0.1);
    }
    
    .stTextInput label,
    .stTextArea label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* Metrics Display */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0066cc;
    }
    
    /* General Streamlit Elements */
    .stMarkdown, .stMarkdown p, .stMarkdown div {
        color: #000000;
    }
    
    /* Select boxes and dropdowns */
    .stSelectbox label,
    .stMultiSelect label,
    .stRadio label,
    .stCheckbox label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
        color: #000000 !important;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #000000;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'report' not in st.session_state:
    st.session_state.report = None

# Header with enhanced styling
st.markdown('<div class="main-header">📄 AI Contract Analysis System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by Multi-Agent AI • Comprehensive Risk Analysis • Instant Insights</div>', unsafe_allow_html=True)
st.markdown("---")

# Welcome Banner
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚖️</div>
            <div class="feature-title">Legal Analysis</div>
            <div class="feature-description">Liability & IP Review</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Compliance Check</div>
            <div class="feature-description">GDPR, HIPAA & SOC 2</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💰</div>
            <div class="feature-title">Financial Risk</div>
            <div class="feature-description">Cost & Penalty Analysis</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <div class="feature-title">Operations</div>
            <div class="feature-description">SLA & Resource Review</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Sidebar with enhanced styling
with st.sidebar:
    st.markdown("### ⚙️ Configuration", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Analysis settings with icons
    st.markdown("#### 🎯 Analysis Settings")
    analysis_mode = st.selectbox(
        "Analysis Mode",
        ["Quick Analysis", "Comprehensive", "Domain-Specific"],
        help="Choose the depth and scope of analysis",
        index=1
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Report settings with icons
    st.markdown("#### 📊 Report Settings")
    report_tone = st.selectbox(
        "Report Tone",
        ["Executive", "Technical", "Legal", "Casual"],
        help="Tone and language style for the report"
    )
    
    report_format = st.selectbox(
        "Report Format",
        ["Markdown", "HTML", "JSON", "Text"],
        help="Output format for the generated report"
    )
    
    report_focus = st.selectbox(
        "Report Focus",
        ["Balanced", "Risks", "Opportunities", "Compliance", "Financial"],
        help="Primary focus area for the analysis"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Options with better spacing
    st.markdown("#### 🔧 Options")
    include_structured = st.checkbox("📋 Include Structured Data", value=True)
    include_recommendations = st.checkbox("💡 Include Recommendations", value=True)
    show_raw = st.checkbox("🔍 Show Raw Agent Outputs", value=False)
    
    st.markdown("---")
    
    # Agent selection with icons
    st.markdown("#### 🤖 Agent Selection")
    use_auto_selection = st.checkbox("✨ Auto-select agents", value=True)
    
    if not use_auto_selection:
        agents = st.multiselect(
            "Select Agents",
            ["Legal", "Compliance", "Finance", "Operations"],
            default=["Legal", "Compliance", "Finance"]
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # System Status
    st.markdown("#### 📡 System Status")
    st.markdown('<div class="status-success">🟢 All Systems Operational</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 0.8rem; color: rgba(255,255,255,0.7); margin-top: 0.5rem;">4 AI Agents Ready</div>', unsafe_allow_html=True)

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📝 Analysis", "📊 Results", "📋 Report", "📚 History"])

with tab1:
    st.markdown('<div class="section-header">📝 Contract Analysis</div>', unsafe_allow_html=True)
    
    # Input method with better styling
    col_input1, col_input2 = st.columns([1, 3])
    with col_input1:
        input_method = st.radio("Input Method", ["📤 Upload File", "📝 Paste Text"])
    
    with col_input2:
        if "📤 Upload" in input_method:
            st.info("💡 Supported formats: PDF, DOCX, TXT • Max size: 10MB")
        else:
            st.info("💡 Paste your contract text directly for quick analysis")
    
    contract_text = ""
    if "📝 Paste" in input_method:
        st.markdown("##### 📄 Contract Text")
        contract_text = st.text_area(
            "Paste Contract Text",
            height=300,
            placeholder="Paste your contract text here...",
            label_visibility="collapsed"
        )
    else:
        st.markdown("##### 📁 Upload Contract File")
        uploaded_file = st.file_uploader(
            "Upload Contract File",
            type=['txt', 'pdf', 'docx'],
            help="Supported formats: TXT, PDF, DOCX",
            label_visibility="collapsed"
        )
        if uploaded_file:
            try:
                # Show file info
                file_details = f"**📎 File:** {uploaded_file.name} | **📦 Size:** {uploaded_file.size/1024:.1f} KB"
                st.markdown(file_details)
                
                # Handle text files
                if uploaded_file.type == "text/plain":
                    contract_text = uploaded_file.read().decode('utf-8')
                    with st.expander("👁️ Preview Contract", expanded=False):
                        st.text_area("Preview", contract_text, height=200, disabled=True)
                
                # Handle PDF files
                elif uploaded_file.type == "application/pdf":
                    from pypdf import PdfReader
                    pdf_reader = PdfReader(uploaded_file)
                    contract_text = ""
                    
                    progress_text = "📖 Extracting text from PDF..."
                    progress_bar = st.progress(0, text=progress_text)
                    
                    for i, page in enumerate(pdf_reader.pages):
                        contract_text += page.extract_text() + "\n"
                        progress_bar.progress((i + 1) / len(pdf_reader.pages), 
                                             text=f"{progress_text} Page {i+1}/{len(pdf_reader.pages)}")
                    
                    progress_bar.empty()
                    st.success(f"✅ Successfully extracted {len(contract_text):,} characters from {len(pdf_reader.pages)} pages")
                    
                    with st.expander("👁️ Preview Contract", expanded=False):
                        st.text_area("Preview", contract_text[:1000] + "...", height=200, disabled=True)
                
                # Handle DOCX files
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    from docx import Document
                    doc = Document(uploaded_file)
                    contract_text = "\n".join([para.text for para in doc.paragraphs])
                    st.success(f"✅ Successfully extracted {len(contract_text):,} characters from DOCX")
                    
                    with st.expander("👁️ Preview Contract", expanded=False):
                        st.text_area("Preview", contract_text[:1000] + "...", height=200, disabled=True)
                
                else:
                    st.warning("⚠️ Unsupported file type. Please use TXT, PDF, or DOCX.")
                    
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
                st.info("💡 Please try a different file or paste the text directly.")
    
    # Analysis query with better styling
    st.markdown("##### 🔍 Analysis Query (Optional)")
    query = st.text_input(
        "Analysis Query",
        placeholder="e.g., 'Focus on financial risks and liability caps' or leave empty for comprehensive analysis",
        help="Specify what aspects to focus on, or leave empty for full analysis",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Analysis buttons with enhanced styling
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    with col1:
        analyze_button = st.button("🚀 Analyze Contract", type="primary", use_container_width=True)
    with col2:
        extract_button = st.button("📑 Extract Clauses", use_container_width=True)
    with col3:
        quick_scan = st.button("⚡ Quick Scan", use_container_width=True)
    with col4:
        clear_button = st.button("🗑️", use_container_width=True)
    
    if clear_button:
        st.session_state.analysis_results = None
        st.session_state.report = None
        st.rerun()
    
    # Extract clauses with enhanced UI
    if extract_button and contract_text:
        with st.spinner("🔍 Extracting clauses from all domains..."):
            extractor = MultiDomainClauseExtractor()
            extraction_query = query if query else "Extract all key clauses"
            
            # Progress indicator
            progress_text = "Analyzing contract structure..."
            progress_bar = st.progress(0, text=progress_text)
            
            result = extractor.extract_clauses(contract_text, extraction_query)
            progress_bar.progress(100, text="✅ Extraction complete!")
            progress_bar.empty()
            
            if result.get("status") == "success":
                st.success("✅ Successfully extracted clauses from all domains!")
                
                data = result.get("data", {})
                
                # Domain icons
                domain_icons = {
                    "payment_terms": "💳",
                    "liability_caps": "⚖️",
                    "sla_terms": "📊",
                    "ip_clauses": "💡",
                    "data_protection": "🔒",
                    "termination_conditions": "🚪",
                    "compliance_requirements": "📋"
                }
                
                # Display extracted clauses by domain in columns
                cols = st.columns(2)
                for idx, (domain, clauses) in enumerate(data.items()):
                    if clauses and isinstance(clauses, list):
                        with cols[idx % 2]:
                            icon = domain_icons.get(domain, "📌")
                            with st.expander(f"{icon} {domain.replace('_', ' ').title()}", expanded=True):
                                for i, clause in enumerate(clauses, 1):
                                    if isinstance(clause, dict):
                                        st.json(clause)
                                    else:
                                        st.markdown(f"**{i}.** {clause}")
            else:
                st.warning(f"⚠️ Extraction status: {result.get('status')}")
    
    # Quick scan feature
    if quick_scan and contract_text:
        st.markdown("---")
        st.markdown('<div class="section-header">⚡ Quick Scan Results</div>', unsafe_allow_html=True)
        
        # Quick metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Document Length</div>
                <div class="metric-value">{:,}</div>
                <div style="font-size: 0.8rem; color: #6c757d;">characters</div>
            </div>
            """.format(len(contract_text)), unsafe_allow_html=True)
        
        with col2:
            word_count = len(contract_text.split())
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Word Count</div>
                <div class="metric-value">{:,}</div>
                <div style="font-size: 0.8rem; color: #6c757d;">words</div>
            </div>
            """.format(word_count), unsafe_allow_html=True)
        
        with col3:
            # Count $ signs as potential financial terms
            financial_terms = contract_text.count('$') + contract_text.lower().count('payment')
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Financial Terms</div>
                <div class="metric-value">{}</div>
                <div style="font-size: 0.8rem; color: #6c757d;">detected</div>
            </div>
            """.format(financial_terms), unsafe_allow_html=True)
        
        with col4:
            # Estimate complexity
            complexity = "High" if word_count > 5000 else "Medium" if word_count > 2000 else "Low"
            color = "#ef4444" if complexity == "High" else "#f59e0b" if complexity == "Medium" else "#10b981"
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Complexity</div>
                <div class="metric-value" style="color: {}">{}</div>
                <div style="font-size: 0.8rem; color: #6c757d;">estimated</div>
            </div>
            """.format(color, complexity), unsafe_allow_html=True)
        
        # Quick keyword detection
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🔎 Key Terms Detected")
        
        keywords = {
            "Legal": ["liability", "indemnify", "intellectual property", "terminate", "breach"],
            "Financial": ["payment", "fee", "penalty", "refund", "invoice"],
            "Compliance": ["GDPR", "HIPAA", "SOC 2", "compliance", "audit"],
            "Operations": ["SLA", "uptime", "response time", "support", "maintenance"]
        }
        
        cols = st.columns(4)
        for idx, (category, terms) in enumerate(keywords.items()):
            with cols[idx]:
                found_terms = [term for term in terms if term.lower() in contract_text.lower()]
                badge_color = "#10b981" if len(found_terms) > 2 else "#f59e0b" if len(found_terms) > 0 else "#6c757d"
                
                st.markdown(f"""
                <div style="padding: 1rem; background: {badge_color}20; border-radius: 10px; border-left: 4px solid {badge_color};">
                    <div style="font-weight: 800; color: #000000; font-size: 1.1rem;">{category}</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #000000;">{len(found_terms)}/{len(terms)}</div>
                    <div style="font-size: 0.8rem; color: #000000; font-weight: 700;">terms found</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.info("💡 For detailed analysis, click '🚀 Analyze Contract' button above")
    
    # Full analysis
    if analyze_button and contract_text:
        with st.spinner("🤖 Running multi-agent analysis..."):
            # Build query
            full_query = f"""
            Analyze this contract:
            
            {contract_text}
            
            {query if query else 'Provide comprehensive analysis covering legal, compliance, financial, and operational aspects.'}
            """
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Generate plan
            status_text.text("📋 Planning analysis...")
            progress_bar.progress(10)
            
            planner = PlanningModule()
            plan = planner.generate_plan(full_query)
            
            status_text.text(f"🤖 Executing {len(plan['agents'])} agents...")
            progress_bar.progress(30)
            
            # Execute agents
            graph = build_graph(plan)
            result = graph.invoke(AgentState(query=full_query))
            
            progress_bar.progress(80)
            status_text.text("📝 Generating report...")
            
            # Generate report
            config = ReportConfig(
                tone=ReportTone[report_tone.upper()],
                format=ReportFormat[report_format.upper()],
                focus=ReportFocus[report_focus.upper()],
                include_structured=include_structured,
                include_recommendations=include_recommendations,
                show_raw_analysis=show_raw
            )
            
            report = ReportGenerator.generate(result, config)
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            # Store results
            st.session_state.analysis_results = result
            st.session_state.report = report
            st.session_state.analysis_history.append({
                'timestamp': datetime.now(),
                'query': query or "Comprehensive analysis",
                'agents': plan['agents'],
                'result': result
            })
            
            st.success("✅ Analysis complete! View results in the Results and Report tabs.")
            st.balloons()

with tab2:
    st.markdown('<div class="section-header">📊 Analysis Results</div>', unsafe_allow_html=True)
    
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        # Enhanced metrics row with icons and colors
        st.markdown("#### 🎯 Agent Execution Status")
        col1, col2, col3, col4 = st.columns(4)
        
        agent_status = [
            ("legal", "⚖️ Legal", "#3b82f6"),
            ("compliance", "🔒 Compliance", "#8b5cf6"),
            ("finance", "💰 Finance", "#10b981"),
            ("operations", "⚙️ Operations", "#f59e0b")
        ]
        
        for col, (key, label, color) in zip([col1, col2, col3, col4], agent_status):
            with col:
                status = "✅ Complete" if results.get(key) else "⏸️ Not Run"
                status_color = "#000000" if results.get(key) else "#6c757d"
                
                st.markdown(f"""
                <div style="padding: 1.5rem; background: {color}15; border-radius: 10px; border-top: 4px solid {color}; text-align: center;">
                    <div style="font-size: 2rem;">{label.split()[0]}</div>
                    <div style="font-weight: 800; color: #000000; margin: 0.5rem 0; font-size: 1.1rem;">{label.split()[1]}</div>
                    <div style="font-size: 0.95rem; color: {status_color}; font-weight: 800;">{status}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Display each agent's output with enhanced styling
        if results.get("legal"):
            st.markdown('<div class="agent-card legal">', unsafe_allow_html=True)
            with st.expander("⚖️ Legal Analysis", expanded=True):
                st.markdown("""
                <div style="background: linear-gradient(135deg, #3b82f610 0%, #3b82f605 100%); 
                            padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
                    <h4 style="color: #000000; margin-bottom: 1rem; font-weight: 900;">📋 Legal Risk Assessment</h4>
                """, unsafe_allow_html=True)
                st.markdown(results["legal"])
                st.markdown('</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if results.get("compliance"):
            st.markdown('<div class="agent-card compliance">', unsafe_allow_html=True)
            with st.expander("🔒 Compliance Analysis", expanded=True):
                st.markdown("""
                <div style="background: linear-gradient(135deg, #8b5cf610 0%, #8b5cf605 100%); 
                            padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
                    <h4 style="color: #000000; margin-bottom: 1rem; font-weight: 900;">🔍 Compliance Review</h4>
                """, unsafe_allow_html=True)
                st.markdown(results["compliance"])
                st.markdown('</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if results.get("finance"):
            st.markdown('<div class="agent-card finance">', unsafe_allow_html=True)
            with st.expander("💰 Financial Analysis", expanded=True):
                st.markdown("""
                <div style="background: linear-gradient(135deg, #10b98110 0%, #10b98105 100%); 
                            padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
                    <h4 style="color: #000000; margin-bottom: 1rem; font-weight: 900;">💵 Financial Impact Assessment</h4>
                """, unsafe_allow_html=True)
                st.markdown(results["finance"])
                st.markdown('</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if results.get("operations"):
            st.markdown('<div class="agent-card operations">', unsafe_allow_html=True)
            with st.expander("⚙️ Operations Analysis", expanded=True):
                st.markdown("""
                <div style="background: linear-gradient(135deg, #f59e0b10 0%, #f59e0b05 100%); 
                            padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
                    <h4 style="color: #000000; margin-bottom: 1rem; font-weight: 900;">🔧 Operational Feasibility</h4>
                """, unsafe_allow_html=True)
                st.markdown(results["operations"])
                st.markdown('</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Structured data with enhanced styling
        if include_structured:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">📊 Structured Data Extraction</div>', unsafe_allow_html=True)
            
            cols = st.columns(2)
            
            with cols[0]:
                if results.get("compliance_risks"):
                    st.markdown("""
                    <div style="background: #8b5cf615; padding: 1rem; border-radius: 10px; border-left: 4px solid #8b5cf6;">
                        <h4 style="color: #000000; font-weight: 900;">🔒 Compliance Risks</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    st.json(results["compliance_risks"])
            
            with cols[1]:
                if results.get("finance_risks"):
                    st.markdown("""
                    <div style="background: #10b98115; padding: 1rem; border-radius: 10px; border-left: 4px solid #10b981;">
                        <h4 style="color: #000000; font-weight: 900;">💰 Financial Risks</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    st.json(results["finance_risks"])
        
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); 
                    border-radius: 20px; border: 2px dashed #9ca3af;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
            <h3 style="color: #6c757d;">No Analysis Results Yet</h3>
            <p style="color: #9ca3af;">Upload a contract and run analysis to see results here</p>
            <br>
            <a href="#" style="color: #667eea; text-decoration: none; font-weight: 600;">
                👈 Go to Analysis Tab
            </a>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">📋 Generated Report</div>', unsafe_allow_html=True)
    
    if st.session_state.report:
        # Enhanced header with download options
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown("""
            <div style="padding: 1rem; background: linear-gradient(135deg, #10b98115 0%, #10b98105 100%); 
                        border-radius: 10px; border-left: 4px solid #10b981;">
                <div style="font-size: 0.9rem; color: #6c757d;">Report Generated</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #10b981;">
                    {} • {} Format • {} Tone
                </div>
            </div>
            """.format(
                datetime.now().strftime('%B %d, %Y at %I:%M %p'),
                report_format,
                report_tone
            ), unsafe_allow_html=True)
        
        with col2:
            st.download_button(
                label="📥 Download",
                data=st.session_state.report,
                file_name=f"contract_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{report_format.lower()}",
                mime="text/plain",
                use_container_width=True,
                type="primary"
            )
        
        with col3:
            if st.button("📧 Share", use_container_width=True):
                st.info("Share functionality coming soon!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Report display with styling
        st.markdown("""
        <div style="background: #ffffff; padding: 2rem; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #e5e7eb;">
        """, unsafe_allow_html=True)
        
        # Display report
        if report_format == "HTML":
            st.components.v1.html(st.session_state.report, height=800, scrolling=True)
        elif report_format == "JSON":
            import json
            st.json(json.loads(st.session_state.report))
        else:
            st.markdown(st.session_state.report)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Feedback section with enhanced styling
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">💭 Feedback</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            rating = st.select_slider(
                "⭐ Rate this analysis",
                options=["😞 Poor", "😐 Fair", "🙂 Good", "😊 Very Good", "🤩 Excellent"],
                value="🙂 Good"
            )
        
        with col2:
            helpful = st.radio(
                "Was this helpful?",
                ["👍 Yes", "👎 No", "🤔 Partially"],
                horizontal=True
            )
        
        feedback = st.text_area(
            "💬 Additional comments (optional)",
            placeholder="Share your thoughts about the analysis quality, accuracy, or suggestions for improvement..."
        )
        
        if st.button("✉️ Submit Feedback", type="primary", use_container_width=False):
            st.success("✅ Thank you for your feedback! We appreciate your input.")
            st.balloons()
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); 
                    border-radius: 20px; border: 2px dashed #9ca3af;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📋</div>
            <h3 style="color: #6c757d;">No Report Generated Yet</h3>
            <p style="color: #9ca3af;">Complete an analysis to generate a comprehensive report</p>
            <br>
            <a href="#" style="color: #667eea; text-decoration: none; font-weight: 600;">
                👈 Go to Analysis Tab
            </a>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-header">📚 Analysis History</div>', unsafe_allow_html=True)
    
    if st.session_state.analysis_history:
        # Summary stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Analyses</div>
                <div class="metric-value">{len(st.session_state.analysis_history)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_agents = sum(len(entry['agents']) for entry in st.session_state.analysis_history)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Agent Runs</div>
                <div class="metric-value">{total_agents}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            latest = st.session_state.analysis_history[-1]['timestamp']
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Latest Analysis</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #667eea;">
                    {latest.strftime('%I:%M %p')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # History entries with enhanced styling
        for i, entry in enumerate(reversed(st.session_state.analysis_history), 1):
            entry_num = len(st.session_state.analysis_history) - i + 1
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                        padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;
                        border-left: 5px solid #667eea; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="color: #667eea; margin: 0;">📊 Analysis #{entry_num}</h4>
                        <p style="color: #6c757d; font-size: 0.9rem; margin: 0.5rem 0;">
                            🕐 {entry['timestamp'].strftime('%B %d, %Y at %I:%M %p')}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("View Details", expanded=False):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown("**📝 Query:**")
                    st.info(entry['query'])
                
                with col_b:
                    st.markdown("**🤖 Agents Used:**")
                    for agent in entry['agents']:
                        st.markdown(f"• {agent}")
                
                col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 3])
                
                with col_btn1:
                    if st.button(f"🔄 Load Results", key=f"load_{i}", use_container_width=True):
                        st.session_state.analysis_results = entry['result']
                        st.success("✅ Results loaded! Check the Results tab.")
                        st.rerun()
                
                with col_btn2:
                    if st.button(f"🗑️ Delete", key=f"delete_{i}", use_container_width=True):
                        st.session_state.analysis_history.remove(entry)
                        st.warning("Deleted!")
                        st.rerun()
        
        # Clear all button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear All History", type="secondary"):
            st.session_state.analysis_history = []
            st.success("All history cleared!")
            st.rerun()
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); 
                    border-radius: 20px; border: 2px dashed #9ca3af;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📚</div>
            <h3 style="color: #6c757d;">No Analysis History</h3>
            <p style="color: #9ca3af;">Your analysis history will appear here</p>
            <br>
            <a href="#" style="color: #667eea; text-decoration: none; font-weight: 600;">
                👈 Start Your First Analysis
            </a>
        </div>
        """, unsafe_allow_html=True)

# Enhanced Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
            border-radius: 15px; margin-top: 3rem;'>
    <h3 style='color: #1a1a1a; font-weight: 800; margin-bottom: 1rem; font-size: 1.8rem;'>
        AI-Powered Contract Analysis System
    </h3>
    <p style='color: #2a2a2a; font-size: 0.95rem; margin-bottom: 0.5rem; font-weight: 700;'>
        Built with ❤️ using Streamlit • Groq Llama AI • LangGraph • Pinecone
    </p>
    <div style='display: flex; justify-content: center; gap: 2rem; margin-top: 1rem; flex-wrap: wrap;'>
        <div style='color: #1a1a1a; font-weight: 800; font-size: 1.05rem;'>⚖️ Legal Analysis</div>
        <div style='color: #1a1a1a; font-weight: 800; font-size: 1.05rem;'>🔒 Compliance Check</div>
        <div style='color: #1a1a1a; font-weight: 800; font-size: 1.05rem;'>💰 Financial Risk</div>
        <div style='color: #1a1a1a; font-weight: 800; font-size: 1.05rem;'>⚙️ Operations Review</div>
    </div>
    <p style='color: #2a2a2a; font-size: 0.85rem; margin-top: 1rem; font-weight: 700;'>
        Version 2.0 • © 2026 • Powered by Multi-Agent AI and Groq
    </p>
</div>
""", unsafe_allow_html=True)
