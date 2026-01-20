"""
FastAPI server for contract analysis.
"""

from __future__ import annotations

import io
from typing import Optional

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

from document_parser import load_document, split_document
from embed_and_upsert import embed_and_upload
from ai_agents.main import run

app = FastAPI(title="AI Contract Analysis API")


class AnalyzeRequest(BaseModel):
	query: str


@app.post("/upload-contract")
async def upload_contract(file: Optional[UploadFile] = File(default=None), text: Optional[str] = None):
	if not file and not text:
		return {"status": "error", "message": "Provide a file or text"}

	content = text
	if file:
		data = await file.read()
		content = data.decode("utf-8") if file.filename.lower().endswith(".txt") else data

	document_text = load_document(text_content=content) if isinstance(content, str) else load_document(file_path=None, text_content=content.decode("utf-8"))
	chunks = split_document(document_text)
	stats = embed_and_upload(chunks, document_id=file.filename if file else "manual_text")
	return {"status": "ok", "uploaded_chunks": stats["uploaded"], "document_id": stats["document_id"]}


@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
	result = run(request.query)
	return {"status": "ok", "result": result}


if __name__ == "__main__":
	import uvicorn

	uvicorn.run(app, host="0.0.0.0", port=8000)
