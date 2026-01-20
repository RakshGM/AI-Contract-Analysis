"""
Pinecone-backed storage for intermediate agent results.
Supports exact storage/retrieval and similarity search for prior analyses.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "contract-analysis")
EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
EMBEDDING_DIM = 1024


class IntermediatesStorage:
	"""Utility class for storing and retrieving intermediate agent results."""

	_model = None
	_pc = None

	@staticmethod
	def _get_model():
		if IntermediatesStorage._model is None:
			IntermediatesStorage._model = SentenceTransformer(EMBEDDING_MODEL)
		return IntermediatesStorage._model

	@staticmethod
	def _get_pinecone_index():
		if not PINECONE_API_KEY:
			raise RuntimeError("PINECONE_API_KEY not set; cannot use Pinecone storage")

		if IntermediatesStorage._pc is None:
			IntermediatesStorage._pc = Pinecone(api_key=PINECONE_API_KEY)

		pc = IntermediatesStorage._pc
		existing = pc.list_indexes().names()
		if PINECONE_INDEX not in existing:
			pc.create_index(
				name=PINECONE_INDEX,
				dimension=EMBEDDING_DIM,
				metric="cosine",
				spec=ServerlessSpec(cloud="aws", region="us-east-1"),
			)
		return pc.Index(PINECONE_INDEX)

	@staticmethod
	def _embed(text: str) -> List[float]:
		model = IntermediatesStorage._get_model()
		return model.encode(text, normalize_embeddings=True).tolist()

	@staticmethod
	def _make_id(query: str, agent_name: str, date_str: Optional[str] = None) -> str:
		payload = f"{query}|{agent_name}|{date_str or datetime.utcnow().date().isoformat()}"
		return hashlib.md5(payload.encode()).hexdigest()

	@staticmethod
	def store_intermediate_result(
		query: str,
		agent_name: str,
		result: Any,
		analysis_type: str = "general",
		namespace: str = "intermediates",
	) -> Dict[str, Any]:
		"""Store a single agent result in Pinecone."""
		try:
			index = IntermediatesStorage._get_pinecone_index()
			vector = IntermediatesStorage._embed(query)
			record_id = IntermediatesStorage._make_id(query, agent_name)

			metadata = {
				"query": query,
				"agent": agent_name,
				"analysis_type": analysis_type,
				"timestamp": datetime.utcnow().isoformat(),
				"result_preview": str(result)[:500],
				"result_full": json.dumps(result, default=str) if not isinstance(result, str) else result,
			}

			index.upsert(vectors=[{"id": record_id, "values": vector, "metadata": metadata}], namespace=namespace)

			return {"status": "stored", "id": record_id, "namespace": namespace}
		except Exception as exc:  # noqa: BLE001
			return {"status": "error", "error": str(exc)}

	@staticmethod
	def store_multi_agent_results(query: str, results: Dict[str, Any], namespace: str = "intermediates") -> Dict[str, Any]:
		"""Store combined results for multiple agents under a single record."""
		try:
			index = IntermediatesStorage._get_pinecone_index()
			vector = IntermediatesStorage._embed(query)
			record_id = IntermediatesStorage._make_id(query, "multi")

			metadata = {
				"query": query,
				"agent": "multi",
				"analysis_type": "combined",
				"timestamp": datetime.utcnow().isoformat(),
				"result_preview": str(results)[:500],
				"result_full": json.dumps(results, default=str),
			}

			index.upsert(vectors=[{"id": record_id, "values": vector, "metadata": metadata}], namespace=namespace)
			return {"status": "stored", "id": record_id, "namespace": namespace}
		except Exception as exc:  # noqa: BLE001
			return {"status": "error", "error": str(exc)}

	@staticmethod
	def retrieve_intermediate_result(
		query: str,
		agent_name: str,
		namespace: str = "intermediates",
		top_k: int = 1,
	) -> Optional[Dict[str, Any]]:
		"""Retrieve the most similar stored result for the given query and agent."""
		try:
			index = IntermediatesStorage._get_pinecone_index()
			vector = IntermediatesStorage._embed(query)
			res = index.query(
				vector=vector,
				top_k=top_k,
				namespace=namespace,
				filter={"agent": {"$eq": agent_name}},
				include_metadata=True,
			)
			if not res.matches:
				return None
			best = res.matches[0]
			return {
				"id": best.id,
				"score": best.score,
				"metadata": best.metadata,
			}
		except Exception:  # noqa: BLE001
			return None

	@staticmethod
	def retrieve_similar_queries(
		query: str,
		analysis_type: str = "general",
		namespace: str = "intermediates",
		top_k: int = 5,
	) -> List[Dict[str, Any]]:
		"""Find historically similar analyses."""
		try:
			index = IntermediatesStorage._get_pinecone_index()
			vector = IntermediatesStorage._embed(query)
			res = index.query(
				vector=vector,
				top_k=top_k,
				namespace=namespace,
				filter={"analysis_type": {"$eq": analysis_type}},
				include_metadata=True,
			)
			matches = []
			for match in res.matches:
				matches.append(
					{
						"id": match.id,
						"similarity_score": match.score,
						"query": match.metadata.get("query"),
						"agent": match.metadata.get("agent"),
						"analysis_type": match.metadata.get("analysis_type"),
						"timestamp": match.metadata.get("timestamp"),
						"result_preview": match.metadata.get("result_preview"),
					}
				)
			return matches
		except Exception:  # noqa: BLE001
			return []


__all__ = ["IntermediatesStorage"]
