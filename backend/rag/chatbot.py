from typing import List, Dict, Any, Optional
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

from app.rag.embeddings import EmbeddingGenerator
from app.rag.retriever import FAISSRetriever


class RAGChatbot:
    """RAG-based farmer advisory chatbot."""
    
    def __init__(
        self, 
        knowledge_base_path: str = "data/knowledge_base",
        llm_model_id: str = "microsoft/DialoGPT-small",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.embedding_generator = EmbeddingGenerator(model_name=embedding_model)
        self.retriever = FAISSRetriever(embedding_dimension=384)
        self.llm_model_id = llm_model_id
        self.qa_chain = None
        self._initialized = False
        
        # Initialize with sample knowledge base
        self._initialize_knowledge_base(knowledge_base_path)
    
    def _initialize_knowledge_base(self, knowledge_base_path: str):
        """Initialize the knowledge base with documents and embeddings."""
        # Ingest documents
        ingestion = self._create_ingestion(knowledge_base_path)
        documents = ingestion.load_text_files()
        chunks = ingestion.split_documents(documents)
        
        if chunks:
            # Generate embeddings
            texts = [chunk.page_content for chunk in chunks]
            embeddings = self.embedding_generator.embed_documents(texts)
            
            # Add to FAISS index
            self.retriever.add_documents(documents=texts, embeddings=embeddings)
            
            # Build QA chain
            self._build_qa_chain()
            self._initialized = True
            print(f"Knowledge base initialized with {len(chunks)} document chunks")
        else:
            print("No knowledge base documents found")
    
    def _create_ingestion(self, knowledge_base_path: str):
        """Create document ingestion pipeline."""
        from app.rag.ingestion import DocumentIngestion
        ingestion = DocumentIngestion(knowledge_base_path)
        return ingestion
    
    def _build_qa_chain(self):
        """Build the LangChain QA retrieval chain."""
        if not self.retriever.documents:
            return
        
        # Create prompt template for agricultural advice
        prompt_template = """You are an AI agricultural assistant providing advice to farmers. 
        Use the following context from agricultural knowledge base to answer the farmer's question.
        
        Context: {context}
        
        Farmer's question: {question}
        
        Guidelines:
        1. Provide practical, actionable advice
        2. Cite sources from the knowledge base when possible
        3. Consider the crop type and local conditions if mentioned
        4. If the question is outside your knowledge, suggest consulting local agricultural extension
        5. Keep responses concise but informative
        
        Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template, 
            input_variables=["context", "question"]
        )
        
        try:
            from langchain.llms import HuggingFaceHub
            llm = HuggingFaceHub(
                repo_id=self.llm_model_id,
                model_kwargs={"temperature": 0.7, "max_new_tokens": 512},
            )
            
            from langchain.chains import RetrievalQA
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.retriever.index if hasattr(self.retriever, 'index') and self.retriever.index else None,
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT},
            )
            print("QA chain built successfully")
        except Exception as e:
            print(f"Error building QA chain: {e}")
    
    def detect_language(self, text: str) -> str:
        """Simple language detection - detect if text is Telugu, Hindi, or English."""
        # Simple heuristic based on Unicode ranges
        telugu_chars = sum(1 for c in text if '\u0C00' <= c <= '\u0C7F')
        hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097F')
        total_chars = len([c for c in text if c.isalpha()])
        
        if total_chars == 0:
            return "en"
        
        telugu_ratio = telugu_chars / total_chars if total_chars else 0
        hindi_ratio = hindi_chars / total_chars if total_chars else 0
        
        if telugu_ratio > 0.3:
            return "te"
        elif hindi_ratio > 0.3:
            return "hi"
        else:
            return "en"
    
    def translate_to_english(self, text: str, source_lang: str = "te") -> str:
        """Translate non-English text to English (placeholder)."""
        # In production, use a translation model or API
        # For now, return as-is
        return text
    
    def get_advice(self, question: str, crop_type: str = None, 
                   farmer_language: str = "en") -> Dict[str, Any]:
        """Get advisory response for a farmer's question."""
        if not self._initialized:
            return {
                "answer": "Knowledge base not initialized. Please contact support.",
                "sources": [],
                "original_question": question,
                "language": farmer_language,
            }
        
        # Detect and normalize language
        detected_lang = self.detect_language(question)
        question_en = self.translate_to_english(question, detected_lang) if detected_lang != "en" else question
        
        # Get query embedding
        query_embedding = self.embedding_generator.embed_query(question_en)
        
        # Search for relevant documents
        results = self.retriever.search(query_embedding, top_k=3)
        
        # Extract document texts
        sources = []
        context_parts = []
        for result in results:
            doc = result.get("document")
            if doc:
                context_parts.append(doc)
                sources.append({
                    "content": doc[:200] + "..." if len(doc) > 200 else doc,
                    "similarity": result.get("similarity_score", 0),
                })
        
        # Build context
        context = "\n\n".join(context_parts) if context_parts else "No relevant documents found."
        
        # Generate answer using QA chain or fallback
        answer = self._generate_answer(question_en, context)
        
        # Translate answer back to farmer's language if needed
        final_answer = self.translate_to_english(answer, "en")  # Placeholder
        if farmer_language != "en":
            # In production, would translate to Telugu/Hindi
            final_answer = f"[{Translated to {farmer_language}}] {answer}"
        
        return {
            "answer": final_answer,
            "sources": sources,
            "original_question": question,
            "detected_language": detected_lang,
            "language": farmer_language,
        }
    
    def _generate_answer(self, question: str, context: str) -> str:
        """Generate answer using QA chain or fallback LLM."""
        if self.qa_chain:
            try:
                result = self.qa_chain({"query": question})
                return result.get("result", str(result))
            except Exception as e:
                print(f"QA chain error: {e}")
        
        # Fallback: generate response based on context keywords
        return self._fallback_response(question, context)
    
    def _fallback_response(self, question: str, context: str) -> str:
        """Generate fallback answer when QA chain is unavailable."""
        question_lower = question.lower()
        
        # Check for key terms and provide relevant advice
        if "rice" in question_lower or "paddy" in question_lower:
            if "slow" in question_lower or "growing slowly" in question_lower:
                return (
                    "Slow growth in rice crops can be caused by several factors:\n"
                    "1. Nutrient deficiency - especially nitrogen\n"
                    "2. Water management issues - check soil moisture levels\n"
                    "3. Pest infestation - inspect leaves for discoloration\n"
                    "4. Soil pH imbalance - optimal range is 5.5-7.0\n\n"
                    "Recommendations:\n"
                    "• Check soil test results for NPK levels\n"
                    "• Apply balanced fertilizer if deficient\n"
                    "• Ensure proper water depth (5-7 cm for rice)\n"
                    "• Monitor for pests and diseases\n"
                    "• Consult local agricultural extension for specific recommendations"
                )
        
        if "wheat" in question_lower:
            return (
                "For wheat crop questions, consider:\n"
                "• Nutrient management (N, P, K requirements)\n"
                "• Irrigation at critical growth stages\n"
                "• Pest and disease monitoring (rust, smut)\n"
                "• Soil health and pH management\n"
                "• Consult local extension for region-specific advice"
            )
        
        if "fertilizer" in question_lower:
            return (
                "Fertilizer recommendations depend on your crop and soil conditions:\n"
                "• Get a soil test done first\n"
                "• Common NPK ratios: 10:26:26 or 15:15:15 for basal\n"
                "• Split applications often work better than one-time\n"
                "• Organic options: compost, farmyard manure\n"
                "• Apply based on growth stage and crop requirements"
            )
        
        if "irrigation" in question_lower or "water" in question_lower:
            return (
                "Irrigation advice:\n"
                "• Monitor soil moisture regularly\n"
                "• Avoid over-irrigation to prevent disease\n"
                "• Water early morning to reduce evaporation\n"
                "• Use soil moisture sensors for precision\n"
                "• Follow crop-specific water requirements\n"
                "• Consider alternate wetting and drying for rice"
            )
        
        # General advice using context
        if context and "Knowledge base" not in context:
            # Extract relevant info from context
            sentences = context.split('.')
            relevant = [s for s in sentences if any(kw in s.lower() for kw in ['rice', 'wheat', 'fertilizer', 'irrigation', 'pest'])]
            if relevant:
                return " ".join(relevant[:3]) + "."
        
        return (
            "I'd be happy to help with your agricultural question! For the most accurate advice, "
            "please provide details about your crop type, location, growth stage, and specific concerns. "
            "You can also ask about fertilizer recommendations, irrigation practices, pest management, "
            "or any other farming-related topic."
        )
    
    def get_multilingual_support(self, supported_langs: List[str] = None) -> Dict[str, Any]:
        """Get information about multilingual support."""
        if supported_langs is None:
            supported_langs = ["en", "te", "hi"]
        
        return {
            "supported_languages": supported_langs,
            "current_language": "en",
            "features": [
                "Language detection from farmer questions",
                "Context-aware responses in local languages",
                "Source citation in original language",
                "Translation support for expansion",
            ],
        }