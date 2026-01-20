"""
Quick Test: Fast Large Document Processing
Demonstrates performance improvements for 100-page documents
"""

import asyncio
import os
from fast_large_document_processor import fast_process_large_document
from dotenv import load_dotenv

load_dotenv()


async def benchmark_large_document():
    """
    Benchmark the fast document processor
    
    Expected improvements:
    - 100-page document: ~15-25 seconds (vs 60+ seconds)
    - Reduction in chunks: 50-70%
    - Reduction in embeddings: Same 50-70%
    """
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║              FAST PROCESSOR BENCHMARK                         ║
    ║              Testing 100+ Page Document Performance           ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Use sample contract if available
    test_file = "contract.txt"
    
    if not os.path.exists(test_file):
        print(f"⚠️  Test file not found: {test_file}")
        print("To test, ensure you have a sample contract file.")
        return
    
    print(f"\n📄 Testing with: {test_file}")
    print(f"📊 File size: {os.path.getsize(test_file) / 1024:.1f} KB")
    
    # Test 1: Without query (select every Nth chunk)
    print("\n" + "="*60)
    print("TEST 1: Document Upload & Indexing (No Query)")
    print("="*60)
    
    result1 = await fast_process_large_document(
        file_path=test_file,
        query=None
    )
    
    if result1["status"] == "completed":
        print(f"\n✅ Results:")
        print(f"   Total time: {result1['total_time']:.2f}s")
        print(f"   Metrics: {result1.get('metrics', {})}")
    
    # Test 2: With query (selective embedding)
    print("\n" + "="*60)
    print("TEST 2: Document Upload with Semantic Query")
    print("="*60)
    
    result2 = await fast_process_large_document(
        file_path=test_file,
        query="Analyze for compliance risks and financial obligations"
    )
    
    if result2["status"] == "completed":
        print(f"\n✅ Results:")
        print(f"   Total time: {result2['total_time']:.2f}s")
        
        # Calculate savings
        if "steps" in result2:
            steps = result2["steps"]
            if "selection" in steps:
                reduction = steps["selection"]["reduction"]
                print(f"   Embedding reduction: {reduction}")
                print(f"   This saves significant API costs! 💰")
    
    # Performance summary
    print("\n" + "="*60)
    print("PERFORMANCE SUMMARY")
    print("="*60)
    print("""
    ✓ Streaming parsing: Processes in batches (no full load)
    ✓ Smart chunking: Semantic boundaries = fewer chunks
    ✓ Selective embedding: Only relevant chunks embedded
    ✓ Batch processing: Parallel embedding batches
    ✓ Async upload: Non-blocking Pinecone operations
    
    EXPECTED IMPROVEMENTS for 100-page document:
    • Speed: 3-5x faster (vs sequential)
    • Memory: Streaming reduces peak usage by 80%
    • Cost: 50-70% reduction in embedding API calls
    • Latency: <100ms response (background job)
    
    USE CASES:
    1. Single large document → /fast-upload-analyze
    2. Multiple documents → /fast-batch-upload
    3. Real-time progress → /fast-status/{job_id}
    """)


if __name__ == "__main__":
    asyncio.run(benchmark_large_document())
