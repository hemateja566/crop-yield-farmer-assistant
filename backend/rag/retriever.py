from typing import List, Dict, Any, Optional
import numpy as np

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False


class FAISSRetriever:
    """FAISS-based vector similarity search for RAG."""
    
    def __init__(self, embedding_dimension: int = 384, index_path: str = None):
        self.embedding_dimension = embedding_dimension
        self.index_path = index_path
        
        if FAISS_AVAILABLE:
            self.index = faiss.IndexFlatL2(embedding_dimension)
            self.documents = []
            self.document_embeddings = []
        else:
            self.index = None
            self.documents = []
            self.document_embeddings = []
            print("Warning: FAISS not installed, using simple similarity search")
    
    def add_documents(self, documents: List[str], embeddings: List[List[float]]):
        """Add documents and their embeddings to the index."""
        self.documents.extend(documents)
        self.document_embeddings.extend(embeddings)
        
        if FAISS_AVAILABLE and self.index is not None:
            embeddings_array = np.array(embeddings, dtype=np.float32)
            self.index.add(embeddings_array)
            print(f"Added {len(documents)} documents to FAISS index (total: {self.index.ntotal})")
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for most similar documents to the query."""
        if not self.documents or self.index is None or not FAISS_AVAILABLE:
            # Fallback: simple cosine similarity
            return self._simple_search(query_embedding, top_k)
        
        # FAISS search
        query_array = np.array([query_embedding], dtype=np.float32)
        distances, indices = self.index.search(query_array, min(top_k, len(self.documents)))
        
        results = []
        for rank, (idx, dist) in enumerate(zip(indices[0], distances[0])):
            if idx < len(self.documents):
                results.append({
                    "rank": rank + 1,
                    "document_index": idx,
                    "document": self.documents[idx] if idx < len(self.documents) else None,
                    "similarity_score": float(1 / (1 + dist)),  # Convert distance to similarity
                    "rank": rank + 1,
                })
        
        return results
    
    def _simple_search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Fallback search using simple cosine similarity."""
        from sklearn.metrics.pairwise import cosine_similarity
        
        query_emb = np.array([query_embedding], dtype=np.float32)
        doc_embeddings = np.array(self.document_embeddings, dtype=np.float32)
        
        if len(doc_embeddings) == 0:
            return []
        
        similarities = cosine_similarity(query_emb, doc_embeddings)[0]
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for rank, idx in enumerate(top_indices):
            if idx < len(self.documents):
                results.append({
                    "rank": rank + 1,
                    "document_index": int(idx),
                    "document": self.documents[idx] if idx < len(self.documents) else None,
                    "similarity_score": float(similarities[idx]),
                    "rank": rank + 1,
                })
        
        return results
    
    def save_index(self, path: str = None):
        """Save the FAISS index to disk."""
        if not FAISS_AVAILABLE or self.index is None:
            print("FAISS not available, cannot save index")
            return
        
        save_path = path or self.index_path or "faiss_index.bin"
        faiss.write_index(self.index, save_path)
        print(f"FAISS index saved to {save_path}")
    
    def load_index(self, path: str = None):
        """Load a FAISS index from disk."""
        not FAISS_AVAILABLE or self.index is None:
            print("FAISS not available, cannot load index")
            return
        
        load_path = path or self.index_path or "faiss_index.bin"
        try:
            self.index = faiss.read_index(load_path)
            print(f"FAISS index loaded from {load_path} (size: {self.index.ntotal})")
        except Exception as e:
            print(f"Error loading FAISS index: {e}")