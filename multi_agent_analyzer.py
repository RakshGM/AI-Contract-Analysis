"""
Alternative analyzer using Groq Mixtral (optional). Falls back to the primary pipeline.
"""

from __future__ import annotations

import os
from typing import Dict, Any

from ai_agents.main import run as primary_run

try:
	from groq import Groq
except ImportError:  # pragma: no cover
	Groq = None

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def analyze_with_groq(query: str) -> Dict[str, Any]:
	if Groq is None or not GROQ_API_KEY:
		# Fallback to primary pipeline
		return primary_run(query)

	client = Groq(api_key=GROQ_API_KEY)
	prompt = f"Analyze the following contract query and return a concise summary. Query: {query}"
	chat_completion = client.chat.completions.create(
		model="mixtral-8x7b-32768",
		messages=[{"role": "user", "content": prompt}],
	)
	content = chat_completion.choices[0].message.content
	return {"groq_summary": content}


if __name__ == "__main__":
	sample_query = "Summarize financial and compliance risks"
	print(analyze_with_groq(sample_query))
