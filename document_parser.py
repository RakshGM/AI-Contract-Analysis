"""
Document parsing utilities for contract analysis
"""

import re
from typing import List, Dict, Any
from pypdf import PdfReader
import os


def load_document(file_path: str = None, text_content: str = None) -> str:
    """
    Load document from file or direct text input
    
    Args:
        file_path: Path to PDF or text file
        text_content: Direct text content
        
    Returns:
        Extracted text content
    """
    if text_content:
        return text_content
    
    if not file_path:
        raise ValueError("Either file_path or text_content must be provided")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Handle PDF files
    if file_path.lower().endswith('.pdf'):
        return load_pdf(file_path)
    
    # Handle text files
    elif file_path.lower().endswith(('.txt', '.md', '.text')):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


def load_pdf(file_path: str) -> str:
    """
    Load and extract text from PDF file
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text content
    """
    try:
        reader = PdfReader(file_path)
        text_content = []
        
        for page in reader.pages:
            text_content.append(page.extract_text())
        
        return "\n\n".join(text_content)
    
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")


def split_document(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Split document into overlapping chunks for embedding
    
    Args:
        text: Full document text
        chunk_size: Target size for each chunk (in characters)
        overlap: Overlap between consecutive chunks
        
    Returns:
        List of chunks with metadata
    """
    # Clean text
    text = clean_text(text)
    
    chunks = []
    start = 0
    chunk_id = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence endings near the chunk boundary
            sentence_end = text.rfind('.', start, end)
            if sentence_end > start + chunk_size // 2:  # At least halfway through chunk
                end = sentence_end + 1
        
        chunk_text = text[start:end].strip()
        
        if chunk_text:
            chunks.append({
                "chunk_id": chunk_id,
                "chunk_text": chunk_text,
                "start_char": start,
                "end_char": end,
                "length": len(chunk_text)
            })
            chunk_id += 1
        
        # Move start position with overlap
        start = end - overlap
    
    return chunks


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.\,\;\:\-\(\)\[\]\{\}\"\'\/\@\#\$\%\&\*\+\=]', '', text)
    
    # Remove multiple consecutive periods
    text = re.sub(r'\.{2,}', '.', text)
    
    return text.strip()


def extract_sections(text: str) -> Dict[str, str]:
    """
    Extract numbered sections from contract text
    
    Args:
        text: Contract text
        
    Returns:
        Dictionary mapping section numbers to content
    """
    sections = {}
    
    # Pattern to match section headers like "1.", "1.1", "Section 1:", etc.
    section_pattern = r'(?:Section\s+)?(\d+(?:\.\d+)*)[\.:\s]+'
    
    matches = list(re.finditer(section_pattern, text, re.IGNORECASE))
    
    for i, match in enumerate(matches):
        section_num = match.group(1)
        start = match.end()
        
        # Find end of section (next section or end of text)
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)
        
        section_content = text[start:end].strip()
        sections[section_num] = section_content
    
    return sections


def extract_key_terms(text: str) -> Dict[str, List[str]]:
    """
    Extract key contract terms and entities
    
    Args:
        text: Contract text
        
    Returns:
        Dictionary of extracted terms by category
    """
    terms = {
        "parties": [],
        "dates": [],
        "amounts": [],
        "obligations": [],
        "definitions": []
    }
    
    # Extract monetary amounts
    amount_pattern = r'\$[\d,]+(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|EUR|GBP|dollars?)'
    terms["amounts"] = re.findall(amount_pattern, text, re.IGNORECASE)
    
    # Extract dates
    date_pattern = r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2}|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})\b'
    terms["dates"] = re.findall(date_pattern, text, re.IGNORECASE)
    
    # Extract party names (simplified - looks for quoted entities or "The Company", etc.)
    party_pattern = r'"([^"]+(?:Inc\.|LLC|Ltd\.|Corporation|Corp\.)?)"'
    terms["parties"] = re.findall(party_pattern, text)
    
    return terms


def get_document_stats(text: str) -> Dict[str, Any]:
    """
    Get statistics about the document
    
    Args:
        text: Document text
        
    Returns:
        Dictionary of statistics
    """
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    
    return {
        "total_characters": len(text),
        "total_words": len(words),
        "total_sentences": len([s for s in sentences if s.strip()]),
        "average_word_length": sum(len(w) for w in words) / len(words) if words else 0,
        "unique_words": len(set(w.lower() for w in words))
    }


# Example usage
if __name__ == "__main__":
    # Example with manual text
    sample_text = """
    This Service Agreement ("Agreement") is entered into as of January 1, 2024,
    between XYZ Corporation ("Provider") and ABC Inc. ("Client").
    
    1. Services
    Provider shall provide software development services as outlined in Exhibit A.
    
    2. Payment Terms
    Client agrees to pay $50,000 per month, due on the first business day of each month.
    Late payments will incur a penalty of 1.5% per month.
    
    3. Term and Termination
    This Agreement shall commence on January 1, 2024 and continue for 12 months.
    Either party may terminate with 30 days written notice.
    """
    
    # Load document
    text = load_document(text_content=sample_text)
    print(f"Loaded document: {len(text)} characters")
    
    # Split into chunks
    chunks = split_document(text, chunk_size=500, overlap=100)
    print(f"\nSplit into {len(chunks)} chunks")
    for chunk in chunks[:2]:
        print(f"  Chunk {chunk['chunk_id']}: {chunk['length']} chars")
    
    # Extract sections
    sections = extract_sections(text)
    print(f"\nFound {len(sections)} sections:")
    for num, content in list(sections.items())[:3]:
        print(f"  Section {num}: {content[:50]}...")
    
    # Get stats
    stats = get_document_stats(text)
    print(f"\nDocument stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
