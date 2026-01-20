"""
Embed document chunks and upload to Pinecone vector database
"""

import os
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import hashlib
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize embedding model
EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
EMBEDDING_DIMENSION = 1024

# Initialize Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "contract-analysis")


def initialize_embedding_model():
    """Initialize and return the sentence transformer model"""
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    return model


def embed_text(text: str, model: SentenceTransformer = None) -> List[float]:
    """
    Embed a single text using sentence transformers
    
    Args:
        text: Text to embed
        model: Optional pre-loaded model
        
    Returns:
        Embedding vector
    """
    if model is None:
        model = initialize_embedding_model()
    
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def embed_chunks(chunks: List[Dict[str, Any]], model: SentenceTransformer = None) -> List[Dict[str, Any]]:
    """
    Embed multiple chunks
    
    Args:
        chunks: List of chunk dictionaries
        model: Optional pre-loaded model
        
    Returns:
        Chunks with embeddings added
    """
    if model is None:
        model = initialize_embedding_model()
    
    print(f"Embedding {len(chunks)} chunks...")
    
    texts = [chunk["chunk_text"] for chunk in chunks]
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    
    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()
    
    return chunks


def initialize_pinecone():
    """Initialize Pinecone client and return index"""
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY not found in environment variables")
    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Check if index exists
    existing_indexes = pc.list_indexes().names()
    
    if PINECONE_INDEX not in existing_indexes:
        print(f"Creating Pinecone index: {PINECONE_INDEX}")
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print(f"Index '{PINECONE_INDEX}' created successfully")
    else:
        print(f"Using existing index: {PINECONE_INDEX}")
    
    return pc.Index(PINECONE_INDEX)


def generate_chunk_id(chunk_text: str, chunk_index: int, document_id: str = "default") -> str:
    """Generate unique ID for a chunk"""
    content = f"{document_id}_{chunk_index}_{chunk_text[:50]}"
    return hashlib.md5(content.encode()).hexdigest()


def upload_to_pinecone(chunks: List[Dict[str, Any]], index, document_id: str = "default", 
                       namespace: str = "contracts") -> Dict[str, Any]:
    """
    Upload embedded chunks to Pinecone
    
    Args:
        chunks: List of chunks with embeddings
        index: Pinecone index object
        document_id: Identifier for the source document
        namespace: Pinecone namespace
        
    Returns:
        Upload statistics
    """
    vectors = []
    
    for i, chunk in enumerate(chunks):
        vector_id = generate_chunk_id(chunk["chunk_text"], i, document_id)
        
        metadata = {
            "chunk_id": chunk.get("chunk_id", i),
            "chunk_text": chunk["chunk_text"],
            "document_id": document_id,
            "start_char": chunk.get("start_char", 0),
            "end_char": chunk.get("end_char", 0),
            "length": chunk.get("length", len(chunk["chunk_text"])),
            "timestamp": datetime.now().isoformat()
        }
        
        vectors.append({
            "id": vector_id,
            "values": chunk["embedding"],
            "metadata": metadata
        })
    
    # Upload in batches
    batch_size = 100
    uploaded = 0
    
    print(f"Uploading {len(vectors)} vectors to Pinecone...")
    
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch, namespace=namespace)
        uploaded += len(batch)
        print(f"  Uploaded {uploaded}/{len(vectors)} vectors")
    
    return {
        "total_chunks": len(chunks),
        "uploaded": uploaded,
        "document_id": document_id,
        "namespace": namespace
    }


def embed_and_upload(chunks: List[Dict[str, Any]], document_id: str = "default",
                    namespace: str = "contracts") -> Dict[str, Any]:
    """
    Complete pipeline: embed chunks and upload to Pinecone
    
    Args:
        chunks: List of chunk dictionaries (from document_parser)
        document_id: Identifier for the source document
        namespace: Pinecone namespace
        
    Returns:
        Upload statistics
    """
    # Initialize model and Pinecone
    model = initialize_embedding_model()
    index = initialize_pinecone()
    
    # Embed chunks
    embedded_chunks = embed_chunks(chunks, model)
    
    # Upload to Pinecone
    stats = upload_to_pinecone(embedded_chunks, index, document_id, namespace)
    
    print(f"\n✓ Successfully embedded and uploaded {stats['uploaded']} chunks")
    return stats


def query_similar_chunks(query: str, top_k: int = 3, namespace: str = "contracts") -> List[Dict[str, Any]]:
    """
    Query Pinecone for similar chunks
    
    Args:
        query: Query text
        top_k: Number of results to return
        namespace: Pinecone namespace
        
    Returns:
        List of matching chunks with scores
    """
    # Embed query
    model = initialize_embedding_model()
    query_embedding = embed_text(query, model)
    
    # Query Pinecone
    index = initialize_pinecone()
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
            "metadata": match.metadata
        })
    
    return matches


# Example usage
if __name__ == "__main__":
    from document_parser import load_document, split_document
    
    # Example contract text
    sample_contract = """
    SERVICE AGREEMENT
    
    This Service Agreement is entered into as of January 1, 2024, between
    XYZ Corporation ("Provider") and ABC Inc. ("Client").
    
    1. SERVICES
    Provider agrees to provide software development and consulting services
    as described in Exhibit A. All services must comply with industry standards
    and GDPR requirements.
    
    2. PAYMENT TERMS
    Client shall pay Provider $50,000 per month, payable on the first business
    day of each month. Late payments will incur a penalty of 1.5% per month.
    Total contract value is estimated at $600,000 for the 12-month term.
    
    3. SERVICE LEVEL AGREEMENT
    Provider guarantees 99.9% uptime for all hosted services. Failure to meet
    this SLA will result in service credits of $1,000 per 0.1% below target.
    
    4. LIABILITY AND INDEMNIFICATION
    Provider's total liability is capped at $1,000,000 per incident, except
    for cases of gross negligence or willful misconduct. Client agrees to
    indemnify Provider against third-party claims.
    
    5. TERM AND TERMINATION
    This Agreement commences on January 1, 2024 and continues for 12 months.
    Either party may terminate with 30 days written notice. Early termination
    by Client requires payment of remaining fees.
    
    6. DATA PROTECTION
    Provider shall implement appropriate technical and organizational measures
    to ensure GDPR compliance, including encryption, access controls, and
    regular security audits.
    """
    
    print("=" * 60)
    print("Document Processing and Embedding Pipeline")
    print("=" * 60)
    
    # Load and split document
    text = load_document(text_content=sample_contract)
    chunks = split_document(text, chunk_size=500, overlap=100)
    
    print(f"\n1. Document loaded: {len(text)} characters")
    print(f"2. Split into {len(chunks)} chunks")
    
    # Embed and upload
    try:
        stats = embed_and_upload(chunks, document_id="sample_contract_001")
        
        print(f"\n3. Upload complete:")
        print(f"   - Total chunks: {stats['total_chunks']}")
        print(f"   - Uploaded: {stats['uploaded']}")
        print(f"   - Document ID: {stats['document_id']}")
        print(f"   - Namespace: {stats['namespace']}")
        
        # Test query
        print("\n4. Testing query...")
        query = "What are the payment terms and penalties?"
        results = query_similar_chunks(query, top_k=3)
        
        print(f"\nQuery: '{query}'")
        print(f"Found {len(results)} matches:")
        for i, result in enumerate(results, 1):
            print(f"\n  Match {i} (score: {result['score']:.3f}):")
            print(f"  {result['metadata']['chunk_text'][:200]}...")
    
    except Exception as e:
        print(f"\n⚠ Error: {str(e)}")
        print("Make sure PINECONE_API_KEY is set in your .env file")
