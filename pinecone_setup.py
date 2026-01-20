"""
Pinecone setup and query utilities
"""

import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "contract-analysis")
EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
EMBEDDING_DIMENSION = 1024

# Cache embedding model for performance
_cached_embedding_model = None

def get_embedding_model():
    """Get cached embedding model to avoid reloading"""
    global _cached_embedding_model
    if _cached_embedding_model is None:
        _cached_embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    return _cached_embedding_model


def setup_pinecone_index(index_name: str = None, dimension: int = EMBEDDING_DIMENSION):
    """
    Set up Pinecone index (create if not exists)
    
    Args:
        index_name: Name of the index
        dimension: Embedding dimension
        
    Returns:
        Pinecone index object
    """
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY not found. Please set it in your .env file")
    
    index_name = index_name or PINECONE_INDEX
    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # List existing indexes
    existing_indexes = pc.list_indexes().names()
    print(f"Existing indexes: {existing_indexes}")
    
    if index_name not in existing_indexes:
        print(f"Creating new index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print(f"✓ Index '{index_name}' created successfully")
    else:
        print(f"✓ Using existing index: {index_name}")
    
    index = pc.Index(index_name)
    
    # Get index stats
    stats = index.describe_index_stats()
    print(f"\nIndex stats:")
    print(f"  - Total vectors: {stats.total_vector_count}")
    print(f"  - Dimension: {stats.dimension}")
    print(f"  - Namespaces: {list(stats.namespaces.keys()) if stats.namespaces else 'None'}")
    
    return index


def delete_pinecone_index(index_name: str = None):
    """Delete a Pinecone index"""
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY not found")
    
    index_name = index_name or PINECONE_INDEX
    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    if index_name in pc.list_indexes().names():
        pc.delete_index(index_name)
        print(f"✓ Index '{index_name}' deleted")
    else:
        print(f"Index '{index_name}' does not exist")


def clear_namespace(namespace: str = "contracts", index_name: str = None):
    """
    Clear all vectors in a specific namespace
    
    Args:
        namespace: Namespace to clear
        index_name: Index name
    """
    index_name = index_name or PINECONE_INDEX
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(index_name)
    
    index.delete(delete_all=True, namespace=namespace)
    print(f"✓ Cleared namespace '{namespace}' in index '{index_name}'")


def embed_query(query: str) -> List[float]:
    """
    Embed a query text
    
    Args:
        query: Query text
        
    Returns:
        Embedding vector
    """
    model = get_embedding_model()
    embedding = model.encode(query, normalize_embeddings=True)
    return embedding.tolist()


def retrieve_chunks(query: str, top_k: int = 1, namespace: str = "contracts",
                   index_name: str = None) -> List[Dict[str, Any]]:
    """
    Retrieve relevant chunks for a query
    
    Args:
        query: Query text
        top_k: Number of results
        namespace: Pinecone namespace
        index_name: Index name
        
    Returns:
        List of matching chunks
    """
    index_name = index_name or PINECONE_INDEX
    
    # Embed query
    query_embedding = embed_query(query)
    
    # Query Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(index_name)
    
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        namespace=namespace,
        include_metadata=True
    )
    
    matches = []
    for match in results.matches:
        matches.append({
            "id": match.id,
            "score": match.score,
            "metadata": match.metadata,
            "chunk_text": match.metadata.get("chunk_text", "")
        })
    
    return matches


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Pinecone Setup Utility")
    print("=" * 60)
    
    try:
        # Setup index
        index = setup_pinecone_index()
        
        print("\n✓ Pinecone is ready for use!")
        print(f"\nTo use in your code:")
        print(f"  from pinecone_setup import retrieve_chunks")
        print(f"  matches = retrieve_chunks('your query here')")
        
    except Exception as e:
        print(f"\n⚠ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure you have a .env file with PINECONE_API_KEY")
        print("2. Get your API key from https://www.pinecone.io/")
        print("3. Add to .env: PINECONE_API_KEY=your-key-here")
