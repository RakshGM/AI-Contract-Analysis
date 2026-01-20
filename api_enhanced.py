"""
FastAPI server with UI integration for contract analysis.
Includes endpoints for upload, analysis, report generation, and status tracking.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai_agents.main import run
from ai_agents.report_generator import (
    ReportGenerator,
    ReportConfig,
    ReportTone,
    ReportFormat,
    ReportFocus,
)
from document_parser import load_document, split_document
from embed_and_upsert import embed_and_upload

app = FastAPI(
    title="Contract Analysis API",
    description="Multi-agent contract analysis system",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    """Request model for analysis."""

    query: str


class ReportRequest(BaseModel):
    """Request model for report generation."""

    query: str
    tone: str = "executive"
    format: str = "markdown"
    focus: str = "balanced"
    include_structured: bool = True
    include_recommendations: bool = True


# Simple in-memory storage for demo
analysis_results = {}
upload_counter = 0


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve main UI page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contract Analysis System</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }
            header h1 { font-size: 2.5em; margin-bottom: 10px; }
            header p { font-size: 1.1em; opacity: 0.9; }
            
            .content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                padding: 40px;
            }
            
            .panel {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            
            .panel h2 {
                color: #333;
                font-size: 1.5em;
                margin-bottom: 10px;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }
            
            .form-group {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            
            label {
                font-weight: 600;
                color: #555;
                font-size: 0.95em;
            }
            
            input[type="text"],
            input[type="file"],
            textarea,
            select {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 0.95em;
                font-family: inherit;
                transition: border-color 0.3s;
            }
            
            input[type="text"]:focus,
            input[type="file"]:focus,
            textarea:focus,
            select:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 8px rgba(102, 126, 234, 0.1);
            }
            
            textarea {
                resize: vertical;
                min-height: 120px;
                font-family: 'Courier New', monospace;
            }
            
            button {
                padding: 12px 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 0.95em;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            
            button:active {
                transform: translateY(0);
            }
            
            .results {
                background: #f9f9f9;
                border-left: 4px solid #667eea;
                padding: 20px;
                border-radius: 6px;
                max-height: 400px;
                overflow-y: auto;
            }
            
            .result-item {
                margin-bottom: 15px;
                padding-bottom: 15px;
                border-bottom: 1px solid #e0e0e0;
            }
            
            .result-item:last-child {
                border-bottom: none;
                margin-bottom: 0;
                padding-bottom: 0;
            }
            
            .result-label {
                font-weight: 600;
                color: #667eea;
                margin-bottom: 5px;
            }
            
            .result-value {
                color: #555;
                font-size: 0.9em;
                line-height: 1.5;
            }
            
            .status {
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 15px;
                font-size: 0.9em;
            }
            
            .status.success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            
            .status.error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            
            .status.loading {
                background: #d1ecf1;
                color: #0c5460;
                border: 1px solid #bee5eb;
            }
            
            .spinner {
                display: inline-block;
                width: 12px;
                height: 12px;
                border: 2px solid #667eea;
                border-top: 2px solid transparent;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-right: 8px;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            .options {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }
            
            @media (max-width: 900px) {
                .content {
                    grid-template-columns: 1fr;
                }
                header h1 { font-size: 2em; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🔍 Contract Analysis System</h1>
                <p>Multi-domain intelligent contract analysis using AI agents</p>
            </header>
            
            <div class="content">
                <div class="panel">
                    <h2>📄 Upload & Analyze</h2>
                    
                    <div class="form-group">
                        <label>Upload Contract File</label>
                        <input type="file" id="contractFile" accept=".txt,.pdf,.md">
                    </div>
                    
                    <button onclick="uploadContract()">Upload & Process</button>
                    
                    <div class="form-group">
                        <label>Or Enter Contract Text</label>
                        <textarea id="contractText" placeholder="Paste contract text here..."></textarea>
                    </div>
                    
                    <button onclick="analyzeText()">Analyze Text</button>
                    
                    <div id="uploadStatus"></div>
                </div>
                
                <div class="panel">
                    <h2>⚙️ Analysis Options</h2>
                    
                    <div class="form-group">
                        <label>Query/Prompt</label>
                        <input type="text" id="query" placeholder="e.g., Analyze for compliance risks" value="Comprehensive contract risk analysis">
                    </div>
                    
                    <div class="options">
                        <div class="form-group">
                            <label>Report Tone</label>
                            <select id="tone">
                                <option value="executive">Executive</option>
                                <option value="technical">Technical</option>
                                <option value="legal">Legal</option>
                                <option value="casual">Casual</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label>Focus Area</label>
                            <select id="focus">
                                <option value="balanced">Balanced</option>
                                <option value="risks">Risks</option>
                                <option value="compliance">Compliance</option>
                                <option value="financial">Financial</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="options">
                        <div class="form-group">
                            <label>Output Format</label>
                            <select id="format">
                                <option value="markdown">Markdown</option>
                                <option value="json">JSON</option>
                                <option value="html">HTML</option>
                                <option value="text">Plain Text</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label>Include</label>
                            <select id="include">
                                <option value="all">All Sections</option>
                                <option value="summary">Summary Only</option>
                                <option value="structured">Structured Data</option>
                            </select>
                        </div>
                    </div>
                    
                    <button onclick="generateReport()">Generate Report</button>
                    
                    <div id="reportStatus"></div>
                </div>
            </div>
            
            <div style="padding: 40px; border-top: 1px solid #e0e0e0;">
                <h2 style="margin-bottom: 20px; color: #333;">📊 Results</h2>
                <div id="results" class="results" style="background: #fff; border: 2px solid #e0e0e0; min-height: 200px; padding: 20px;">
                    <p style="color: #999;">Analysis results will appear here...</p>
                </div>
            </div>
        </div>
        
        <script>
            function showStatus(elementId, message, type) {
                const el = document.getElementById(elementId);
                el.innerHTML = `<div class="status ${type}">${message}</div>`;
            }
            
            async function uploadContract() {
                const file = document.getElementById('contractFile').files[0];
                if (!file) {
                    showStatus('uploadStatus', 'Please select a file', 'error');
                    return;
                }
                
                showStatus('uploadStatus', '<span class="spinner"></span>Uploading...', 'loading');
                
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const response = await fetch('/upload-contract', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await response.json();
                    
                    if (response.ok) {
                        showStatus('uploadStatus', `✓ Uploaded ${data.uploaded_chunks} chunks`, 'success');
                        document.getElementById('results').innerHTML = JSON.stringify(data, null, 2);
                    } else {
                        showStatus('uploadStatus', `Error: ${data.message}`, 'error');
                    }
                } catch (error) {
                    showStatus('uploadStatus', `Error: ${error.message}`, 'error');
                }
            }
            
            async function analyzeText() {
                const text = document.getElementById('contractText').value;
                if (!text) {
                    showStatus('uploadStatus', 'Please enter contract text', 'error');
                    return;
                }
                
                showStatus('uploadStatus', '<span class="spinner"></span>Analyzing...', 'loading');
                
                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query: text })
                    });
                    const data = await response.json();
                    
                    if (response.ok) {
                        showStatus('uploadStatus', '✓ Analysis complete', 'success');
                        displayResults(data.result);
                    } else {
                        showStatus('uploadStatus', `Error: ${data.detail}`, 'error');
                    }
                } catch (error) {
                    showStatus('uploadStatus', `Error: ${error.message}`, 'error');
                }
            }
            
            async function generateReport() {
                const query = document.getElementById('query').value;
                const tone = document.getElementById('tone').value;
                const focus = document.getElementById('focus').value;
                const format = document.getElementById('format').value;
                
                showStatus('reportStatus', '<span class="spinner"></span>Generating report...', 'loading');
                
                try {
                    const response = await fetch('/generate-report', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query, tone, format, focus })
                    });
                    const data = await response.json();
                    
                    if (response.ok) {
                        showStatus('reportStatus', '✓ Report generated', 'success');
                        displayReport(data.report, format);
                    } else {
                        showStatus('reportStatus', `Error: ${data.detail}`, 'error');
                    }
                } catch (error) {
                    showStatus('reportStatus', `Error: ${error.message}`, 'error');
                }
            }
            
            function displayResults(result) {
                const resultsDiv = document.getElementById('results');
                let html = '';
                
                for (const [key, value] of Object.entries(result)) {
                    if (value) {
                        html += `<div class="result-item">
                            <div class="result-label">${key.toUpperCase()}</div>
                            <div class="result-value">${String(value).substring(0, 200)}...</div>
                        </div>`;
                    }
                }
                
                resultsDiv.innerHTML = html || '<p style="color: #999;">No results</p>';
            }
            
            function displayReport(report, format) {
                const resultsDiv = document.getElementById('results');
                if (format === 'json') {
                    resultsDiv.innerHTML = '<pre>' + JSON.stringify(JSON.parse(report), null, 2) + '</pre>';
                } else if (format === 'html') {
                    resultsDiv.innerHTML = report;
                } else {
                    resultsDiv.innerHTML = '<pre>' + report + '</pre>';
                }
            }
        </script>
    </body>
    </html>
    """


@app.post("/upload-contract")
async def upload_contract(file: Optional[UploadFile] = File(None), text: Optional[str] = None):
    """Upload and process a contract file."""
    if not file and not text:
        raise HTTPException(status_code=400, detail="Provide a file or text")

    try:
        if file:
            content = await file.read()
            document_text = load_document(text_content=content.decode("utf-8"))
        else:
            document_text = load_document(text_content=text)

        chunks = split_document(document_text)
        stats = embed_and_upload(chunks, document_id=file.filename if file else "manual_upload")

        return {
            "status": "ok",
            "uploaded_chunks": stats["uploaded"],
            "total_chunks": stats["total_chunks"],
            "document_id": stats["document_id"],
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    """Analyze a contract based on query."""
    try:
        result = run(request.query)
        return {"status": "ok", "result": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/generate-report")
async def generate_report(request: ReportRequest):
    """Generate a customized report."""
    try:
        # Run analysis
        result = run(request.query)

        # Import here to avoid circular imports
        from ai_agents.graph import AgentState

        state = AgentState(
            query=request.query,
            legal=result.get("legal"),
            compliance=result.get("compliance"),
            finance=result.get("finance"),
            operations=result.get("operations"),
            legal_clauses=result.get("legal_clauses"),
            compliance_risks=result.get("compliance_risks"),
            finance_risks=result.get("finance_risks"),
            agent_context=result.get("agent_context"),
            final_summary=None,
        )

        config = ReportConfig(
            tone=ReportTone[request.tone.upper()],
            format=ReportFormat[request.format.upper()],
            focus=ReportFocus[request.focus.upper()],
            include_structured=request.include_structured,
            include_recommendations=request.include_recommendations,
        )

        report = ReportGenerator.generate(state, config)
        return {"status": "ok", "report": report}

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Contract Analysis API"}


if __name__ == "__main__":
    import uvicorn

    print("Starting Contract Analysis API server...")
    print("Visit http://localhost:8000 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8000)
