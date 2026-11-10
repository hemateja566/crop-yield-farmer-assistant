from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from app.rag.chatbot import RAGChatbot
from app.config import SUPPORTED_LANGUAGES

router = APIRouter(prefix="/chat", tags=["Chatbot"])


@router.post("/ask", response_model=dict)
async def ask_question(
    question: str,
    crop_type: Optional[str] = None,
    farmer_language: str = "en",
):
    """Ask the AI farmer advisory chatbot a question."""
    try:
        # Initialize RAG chatbot (in production, would be singleton)
        rag = RAGChatbot()
        
        # Get advisory response
        result = rag.get_advice(
            question=question,
            crop_type=crop_type,
            farmer_language=farmer_language,
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chatbot error: {str(e)}",
        )


@router.get("/languages", response_model=dict)
async def get_supported_languages():
    """Get supported languages for the chatbot."""
    return {
        "languages": SUPPORTED_LANGUAGES,
        "descriptions": {
            "en": "English",
            "te": "Telugu",
            "hi": "Hindi",
        },
    }


@router.post("/multilingual", response_model=dict)
async def multilingual_question(
    question: str,
    target_language: str = "te",
):
    """Get response in a specific Indian language."""
    try:
        rag = RAGChatbot()
        
        # Get advice in English first
        english_result = rag.get_advice(question=question, farmer_language="en")
        
        # In production, would translate to target language
        # For now, return English with language marker
        return {
            "original_question": question,
            "target_language": target_language,
            "answer": english_result["answer"],
            "note": f"Translated to {target_language} (feature coming soon)",
            "sources": english_result.get("sources", []),
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Multilingual error: {str(e)}",
        )


@router.get("/knowledge-base/status", response_model=dict)
async def get_knowledge_base_status():
    """Get knowledge base status and statistics."""
    try:
        rag = RAGChatbot()
        support = rag.get_multilingual_support()
        
        return {
            "initialized": rag._initialized,
            "supported_languages": support["supported_languages"],
            "document_chunks": len(rag.retriever.documents) if rag.retriever else 0,
            "message": "Knowledge base ready" if rag._initialized else "Initializing...",
        }
    except Exception as e:
        return {
            "initialized": False,
            "error": str(e),
        }