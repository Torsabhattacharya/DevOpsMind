from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class EmbeddingModel:
    """Generate embeddings for code chunks"""
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for single text"""
        embedding = self.model.encode(text)
        return embedding
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for multiple texts"""
        embeddings = self.model.encode(texts)
        return embeddings
    
    def embed_code_chunk(self, code: str, language: str = None) -> np.ndarray:
        """Generate embedding for code chunk with optional language context"""
        # Add language context to improve embeddings
        if language:
            enhanced_text = f"Language: {language}\nCode:\n{code}"
        else:
            enhanced_text = code
        
        return self.embed_text(enhanced_text)
    
    def get_query_embedding(self, query: str) -> np.ndarray:
        """Generate embedding for user query"""
        # Enhance query for better code search
        enhanced_query = f"Question about code: {query}"
        return self.embed_text(enhanced_query)