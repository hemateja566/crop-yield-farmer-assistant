from typing import List, Optional
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    from langchain.embeddings import HuggingFaceEmbeddings
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False


class EmbeddingGenerator:
    """Generate text embeddings using SentenceTransformers/HuggingFace."""
    
    def __init__(
        self, 
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: str = "cpu",
    ):
        self.model_name = model_name
        self.device = device
        
        if EMBEDDING_AVAILABLE:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={"device": device},
                encode_kwargs={"normalize_embeddings": True},
            )
            # Load the underlying model for direct use
            self.model = SentenceTransformer(model_name)
        else:
            self.embeddings = None
            self.model = None
    
    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a search query."""
        if self.embeddings:
            return self.embeddings.query_documents([query])[0]
        elif self.model:
            return self.model.encode(query).tolist()
        else:
            # Fallback: simple hash-based embedding (not recommended)
            print("Warning: Using fallback embedding method")
            return [hash(query) % 1000 / 1000.0] * 384
    
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents."""
        if self.embeddings:
            return self.embeddings.documents(documents)
        elif self.model:
            return self.model.encode(documents).tolist()
        else:
            print("Warning: Using fallback embedding method")
            return [[hash(doc) % 1000 / 1000.0] * 384 for doc in documents]
    
    def embed_query_text(self, query: str) -> np.ndarray:
        """Generate embedding as numpy array."""
        if self.embeddings:
            return self.embeddings.embed_query(query)
        elif self.model:
            return self.model.encode(query)
        else:
            return np.array([hash(query) % 1000 / 1000.0] * 384)
    
    def similarity_search(self, query: str, document_embeddings: List[List[float]], 
                         top_k: int = 5) -> List[int]:
        """Find the top-k most similar documents to a query."""
        from sklearn.metrics.pairwise import cosine_similarity
        
        query_embedding = self.embed_query(query)
        doc_embeddings = document_embeddings
        
        if not doc_embeddings:
            return []
        
        # Calculate cosine similarities
        similarities = cosine_similarity(
            [query_embedding], doc_embeddings
        )[0]
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        return top_indices.tolist()