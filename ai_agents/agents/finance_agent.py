"""
Finance agent for financial exposure and obligations.
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

from ai_agents.prompt_templates import PromptTemplates
from ai_agents.structured_extraction import FinancialRiskExtractionPipeline
from ai_agents.intermediates_storage import IntermediatesStorage
from ai_agents.context_cache import get_cached_context

try:
	from groq import Groq
except ImportError:  # pragma: no cover
	Groq = None

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def _get_client():
	if Groq is None or not GROQ_API_KEY:
		return None
	return Groq(api_key=GROQ_API_KEY)


def finance_agent(state: dict) -> dict:
	"""Analyze financial aspects of the contract."""
	query = state.get("query", "")
	context = get_cached_context(query, top_k=1)

	if state.get("agent_context"):
		context = f"{context}\n\nPrevious findings:\n{state['agent_context']}"

	prompt = PromptTemplates.get_finance_agent_prompt(context, query)

	client = _get_client()
	analysis: Any
	if client:
		try:
			resp = client.chat.completions.create(
				model=MODEL_NAME,
				messages=[{"role": "user", "content": prompt}],
				temperature=0.2,
				max_tokens=2048
			)
			analysis = resp.choices[0].message.content
		except Exception as exc:  # noqa: BLE001
			analysis = f"[Finance analysis unavailable: {exc}]"
	else:
		analysis = "Finance analysis placeholder (no GROQ_API_KEY configured)."

	# Skip structured extraction for faster processing
	# structured = FinancialRiskExtractionPipeline.extract_financial_risks(context, query)
	# if structured.get("status") == "success":
	#     state["finance_risks"] = structured.get("data")

	state["finance"] = analysis

	# Skip multi-turn context for faster processing
	# previous = state.get("agent_context", "")
	# state["agent_context"] = f"{previous}\nFinance Agent Findings: {analysis}".strip()

	IntermediatesStorage.store_intermediate_result(query, "FinanceAgent", analysis, analysis_type="financial")
	return state


__all__ = ["finance_agent"]
