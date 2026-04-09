import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict, Any

class FAISSVectorDB:
    """FAISS vector store for code embeddings"""
    
    def __init__(self, dimension=384):
        self.dimension = dimension
        self.index = None
        self.chunks = []
        self.metadata = []
        self.initialized = False
    
    def initialize(self):
        """Initialize empty index"""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.initialized = True
    
    def add_chunks(self, chunks: List[str], embeddings: np.ndarray, metadata: List[Dict]):
        """Add chunks with their embeddings to the index"""
        if not self.initialized:
            self.initialize()
        
        # Convert embeddings to float32 for FAISS
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Add to index
        self.index.add(embeddings_array)
        
        # Store chunks and metadata
        self.chunks.extend(chunks)
        self.metadata.extend(metadata)
        
        print(f"Added {len(chunks)} chunks. Total: {self.index.ntotal}")
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        """Search for similar chunks"""
        if not self.initialized or self.index.ntotal == 0:
            return []
        
        query = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query, min(k, self.index.ntotal))
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.chunks):
                results.append({
                    'chunk': self.chunks[idx],
                    'metadata': self.metadata[idx],
                    'score': float(distances[0][i]),
                    'similarity': 1 / (1 + float(distances[0][i]))  # Convert distance to similarity
                })
        
        return results
    
    def save(self, path: str):
        """Save index and data to disk"""
        save_path = Path(path)
        save_path.mkdir(exist_ok=True)
        
        # Save FAISS index
        if self.index:
            faiss.write_index(self.index, str(save_path / "index.faiss"))
        
        # Save chunks and metadata
        with open(save_path / "data.pkl", 'wb') as f:
            pickle.dump({
                'chunks': self.chunks,
                'metadata': self.metadata
            }, f)
        
        print(f"Saved vector store to {path}")
    
    def load(self, path: str):
        """Load index and data from disk"""
        load_path = Path(path)
        
        # Load FAISS index
        index_path = load_path / "index.faiss"
        if index_path.exists():
            self.index = faiss.read_index(str(index_path))
            self.initialized = True
        
        # Load chunks and metadata
        data_path = load_path / "data.pkl"
        if data_path.exists():
            with open(data_path, 'rb') as f:
                data = pickle.load(f)
                self.chunks = data['chunks']
                self.metadata = data['metadata']
        
        print(f"Loaded vector store from {path}. Total chunks: {self.index.ntotal if self.index else 0}")
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store"""
        return {
            "total_chunks": self.index.ntotal if self.index else 0,
            "dimension": self.dimension,
            "initialized": self.initialized
        }
    
    def clear(self):
        """Clear all data"""
        self.index = None
        self.chunks = []
        self.metadata = []
        self.initialized = False
        self.initialize()