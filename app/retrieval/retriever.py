from typing import List, Dict
from app.embeddings.embedding_model import EmbeddingModel
from app.vectorstore.vectordb import FAISSVectorDB


class SemanticRetriever:
    """Retrieve relevant code chunks using semantic search"""

    def __init__(self, vector_db: FAISSVectorDB, embedding_model: EmbeddingModel):
        self.vector_db = vector_db
        self.embedding_model = embedding_model

    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        """Retrieve relevant chunks for a query"""
        # Generate query embedding
        query_embedding = self.embedding_model.get_query_embedding(query)

        # Search in vector DB
        results = self.vector_db.search(query_embedding, k)

        return results

    def retrieve_with_filter(self, query: str, language: str = None, k: int = 5) -> List[Dict]:
        """Retrieve with language filter"""
        results = self.retrieve(query, k * 2)  # Get more results then filter

        if language:
            filtered = [
                r for r in results
                if r.get('metadata', {}).get('language') == language
            ]
            return filtered[:k]

        return results[:k]

    def format_results(self, results: List[Dict]) -> str:
        """Format retrieval results for LLM context"""
        if not results:
            return "No relevant code found."

        formatted = []

        for i, result in enumerate(results, 1):
            metadata = result.get('metadata', {})
            chunk = result.get('chunk', '')

            formatted.append(f"""
### Result {i} - File: {metadata.get('file', 'unknown')}
**Language:** {metadata.get('language', 'unknown')}
**Similarity:** {result.get('similarity', 0):.2f}

```{metadata.get('language', 'text')}
{chunk[:800]}""")
        return "\n".join(formatted)