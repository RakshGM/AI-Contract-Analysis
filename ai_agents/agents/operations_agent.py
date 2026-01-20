"""
Operations agent for SLA and delivery feasibility.
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

from ai_agents.prompt_templates import PromptTemplates
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


def operations_agent(state: dict) -> dict:
	"""Analyze operational aspects of the contract."""
	query = state.get("query", "")
	context = get_cached_context(query, top_k=2)

	if state.get("agent_context"):
		context = f"{context}\n\nPrevious findings:\n{state['agent_context']}"

	prompt = PromptTemplates.get_operations_agent_prompt(context, query)

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
			analysis = f"[Operations analysis unavailable: {exc}]"
	else:
		analysis = "Operations analysis placeholder (no GROQ_API_KEY configured)."

	state["operations"] = analysis

	# Skip multi-turn context for faster processing
	# previous = state.get("agent_context", "")
	# state["agent_context"] = f"{previous}\nOperations Agent Findings: {analysis}".strip()

	IntermediatesStorage.store_intermediate_result(query, "OperationsAgent", analysis, analysis_type="operations")
	return state


__all__ = ["operations_agent"]
