"""
Context cache for sharing retrieved chunks across agents
"""

from typing import Optional
from pinecone_setup import retrieve_chunks

# Simple cache to avoid redundant retrieval calls
_context_cache = {}


def get_cached_context(query: str, top_k: int = 2) -> str:
    """
    Get context with caching to avoid redundant Pinecone queries
    
    Args:
        query: Query string
        top_k: Number of chunks to retrieve
        
    Returns:
        Context string from retrieved chunks
    """
    cache_key = f"{query}:{top_k}"
    
    if cache_key in _context_cache:
        return _context_cache[cache_key]
    
    try:
        matches = retrieve_chunks(query, top_k=top_k)
        context = "\n\n".join(m.get("chunk_text", "") for m in matches)
        _context_cache[cache_key] = context
        return context
    except Exception:
        return ""


def clear_context_cache():
    """Clear the context cache"""
    global _context_cache
    _context_cache = {}
