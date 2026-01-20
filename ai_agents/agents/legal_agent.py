"""
Legal agent for contract analysis.
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

from ai_agents.prompt_templates import PromptTemplates
from ai_agents.intermediates_storage import IntermediatesStorage
from ai_agents.structured_extraction import MultiDomainClauseExtractor
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


def legal_agent(state: dict) -> dict:
	"""Analyze legal aspects of the contract."""
	query = state.get("query", "")
	context = get_cached_context(query, top_k=1)

	if state.get("agent_context"):
		context = f"{context}\n\nPrevious findings:\n{state['agent_context']}"

	prompt = PromptTemplates.get_legal_agent_prompt(context, query)

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
			analysis = f"[Legal analysis unavailable: {exc}]"
	else:
		analysis = "Legal analysis placeholder (no GROQ_API_KEY configured)."

	# Skip structured extraction for faster processing
	# Uncomment if detailed clause extraction is needed
	# structured = MultiDomainClauseExtractor.extract_clauses(context, query)
	# if structured.get("status") == "success":
	#     state["legal_clauses"] = structured.get("data")

	state["legal"] = analysis

	# Update multi-turn context (skip for faster processing)
	# previous = state.get("agent_context", "")
	# state["agent_context"] = f"{previous}\nLegal Agent Findings: {analysis}".strip()

	# Persist intermediate result
	IntermediatesStorage.store_intermediate_result(query, "LegalAgent", analysis, analysis_type="legal")
	return state


__all__ = ["legal_agent"]
