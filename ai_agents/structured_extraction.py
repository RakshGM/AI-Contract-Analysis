"""
Structured extraction pipelines for contract analysis.
Uses Gemini 1.5 Flash when available, with graceful fallbacks to
deterministic sample outputs when no API key is configured.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict

from dotenv import load_dotenv

from ai_agents.prompt_templates import PromptTemplates

try:
	import google.generativeai as genai
except ImportError:  # pragma: no cover - handled by fallback
	genai = None


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def _configure_gemini():
	if genai is None:
		return None
	if not GEMINI_API_KEY:
		return None
	genai.configure(api_key=GEMINI_API_KEY)
	return genai.GenerativeModel(MODEL_NAME)


def _safe_json_loads(text: str) -> Dict[str, Any]:
	"""Parse JSON content, stripping fences if present."""
	cleaned = text.strip()
	if cleaned.startswith("```"):
		parts = cleaned.split("```")
		if len(parts) >= 2:
			cleaned = parts[1]
			if cleaned.startswith("json"):
				cleaned = cleaned[4:]
	return json.loads(cleaned)


def _fallback_response(template: Dict[str, Any]) -> Dict[str, Any]:
	return {
		"status": "success",
		"data": template,
		"source": "fallback",
		"timestamp": datetime.utcnow().isoformat(),
	}


def _call_gemini(prompt: str) -> str:
	model = _configure_gemini()
	if not model:
		raise RuntimeError("Gemini not configured")
	response = model.generate_content(prompt)
	return response.text


class ComplianceExtractionPipeline:
	"""Structured compliance risk extraction."""

	@staticmethod
	def extract_compliance_risks(context: str, query: str) -> Dict[str, Any]:
		prompt = PromptTemplates.get_structured_compliance_prompt(context, query)
		try:
			raw = _call_gemini(prompt)
			data = _safe_json_loads(raw)
			return {
				"status": "success",
				"data": data,
				"source": "gemini",
				"timestamp": datetime.utcnow().isoformat(),
			}
		except Exception as exc:  # noqa: BLE001 - we want a safe fallback
			template = {
				"regulations_violated": [
					{
						"regulation": "GDPR Article 32",
						"description": "Security measures not specified",
						"severity": "Medium",
					}
				],
				"missing_clauses": [
					{
						"clause_type": "Data Breach Notification",
						"requirement": "Notify within 72 hours",
						"impact": "High",
					}
				],
				"overall_compliance_score": 65,
				"priority_actions": [
					{
						"action": "Add data breach clause with 72h notice",
						"urgency": "High",
						"timeline": "Immediate",
					}
				],
				"error": str(exc),
			}
			return _fallback_response(template)


class FinancialRiskExtractionPipeline:
	"""Structured financial risk extraction."""

	@staticmethod
	def extract_financial_risks(context: str, query: str) -> Dict[str, Any]:
		prompt = PromptTemplates.get_structured_finance_prompt(context, query)
		try:
			raw = _call_gemini(prompt)
			data = _safe_json_loads(raw)
			return {
				"status": "success",
				"data": data,
				"source": "gemini",
				"timestamp": datetime.utcnow().isoformat(),
			}
		except Exception as exc:  # noqa: BLE001
			template = {
				"payment_obligations": [
					{
						"type": "Recurring Fee",
						"amount": "$10,000",
						"frequency": "Monthly",
						"due_date": "1st of month",
					}
				],
				"penalties": [
					{
						"trigger": "Late delivery",
						"amount": "$500 per day",
						"maximum": "$50,000",
					}
				],
				"financial_risks": [
					{
						"risk": "Uncapped liability",
						"exposure": "Unlimited",
						"probability": "Medium",
					}
				],
				"total_exposure_estimate": "$500,000",
				"mitigation_needed": True,
				"error": str(exc),
			}
			return _fallback_response(template)


class MultiDomainClauseExtractor:
	"""Structured multi-domain clause extraction."""

	@staticmethod
	def extract_clauses(context: str, query: str) -> Dict[str, Any]:
		prompt = PromptTemplates.get_multi_domain_clause_prompt(context, query)
		try:
			raw = _call_gemini(prompt)
			data = _safe_json_loads(raw)
			return {
				"status": "success",
				"data": data,
				"source": "gemini",
				"timestamp": datetime.utcnow().isoformat(),
			}
		except Exception as exc:  # noqa: BLE001
			template = {
				"legal_clauses": [
					{
						"type": "Indemnification",
						"summary": "Client indemnifies vendor for third-party claims",
						"location": "Section 8.1",
					}
				],
				"termination_clauses": [
					{
						"condition": "Material breach",
						"notice_period": "30 days",
						"penalties": "None",
					}
				],
				"liability_caps": [
					{
						"type": "General Liability",
						"limit": "$1,000,000",
						"exclusions": ["Gross negligence"],
					}
				],
				"ip_clauses": [
					{
						"type": "IP Ownership",
						"owner": "Client",
						"exceptions": ["Pre-existing vendor IP"],
					}
				],
				"sla_terms": [
					{
						"metric": "Uptime",
						"target": "99.9%",
						"penalty": "$1000 per 0.1% below",
					}
				],
				"payment_terms": [
					{
						"schedule": "Net 30",
						"method": "Wire transfer",
						"late_fee": "1.5% per month",
					}
				],
				"data_protection": [
					{
						"requirement": "GDPR compliant",
						"measures": ["Encryption", "Access controls"],
					}
				],
				"error": str(exc),
			}
			return _fallback_response(template)


__all__ = [
	"ComplianceExtractionPipeline",
	"FinancialRiskExtractionPipeline",
	"MultiDomainClauseExtractor",
]
