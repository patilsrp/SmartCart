from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
import uvicorn
from rag import SmartCartRAG
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SmartCart AI Service",
    description="RAG-powered conversational commerce API using LangChain, pgvector, HuggingFace, and OpenAI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_system: Optional[SmartCartRAG] = None

class Query(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="User's shopping query")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")

class QueryWithHistory(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="User's shopping query")
    history: List[Dict[str, str]] = Field(default_factory=list, description="Conversation history")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")

class ProductRecommendation(BaseModel):
    answer: str = Field(..., description="AI-generated product recommendation")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")
    timestamp: str = Field(..., description="Response timestamp")

class HealthCheck(BaseModel):
    status: str
    vector_store: str
    llm: str
    embeddings: str
    timestamp: str

conversation_sessions: Dict[str, List[Dict[str, str]]] = {}

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG system on startup."""
    global rag_system
    try:
        logger.info("Initializing SmartCart RAG system...")
        rag_system = SmartCartRAG()
        logger.info("RAG system initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}")
        logger.warning("Service starting without RAG - endpoints will return errors")

@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint with service information."""
    return {
        "service": "SmartCart AI Service",
        "version": "1.0.0",
        "status": "operational" if rag_system else "degraded",
        "endpoints": {
            "/recommend": "Single-turn product recommendations",
            "/recommend/conversational": "Multi-turn conversational recommendations",
            "/health": "Service health check",
            "/docs": "Interactive API documentation"
        }
    }

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint to verify all components are working."""
    status = {
        "status": "healthy" if rag_system else "unhealthy",
        "vector_store": "connected" if rag_system else "disconnected",
        "llm": "ready" if rag_system else "unavailable",
        "embeddings": "loaded" if rag_system else "not loaded",
        "timestamp": datetime.now().isoformat()
    }
    
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    return status

@app.post("/recommend", response_model=ProductRecommendation)
async def recommend(query: Query):
    """
    Single-turn product recommendation endpoint.
    
    This endpoint processes a shopping query and returns AI-generated recommendations
    based on semantic search through the product catalog.
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not available")
    
    try:
        logger.info(f"Processing query: {query.question}")
        answer = rag_system.ask(query.question)
        
        response = ProductRecommendation(
            answer=answer,
            session_id=query.session_id,
            timestamp=datetime.now().isoformat()
        )
        
        if query.session_id:
            if query.session_id not in conversation_sessions:
                conversation_sessions[query.session_id] = []
            conversation_sessions[query.session_id].append({"role": "user", "content": query.question})
            conversation_sessions[query.session_id].append({"role": "assistant", "content": answer})
        
        return response
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend/conversational", response_model=ProductRecommendation)
async def recommend_conversational(query: QueryWithHistory):
    """
    Multi-turn conversational recommendation endpoint.
    
    This endpoint maintains conversation context, allowing for follow-up questions
    like "show me cheaper ones" or "what about in blue?".
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not available")
    
    try:
        logger.info(f"Processing conversational query: {query.question}")
        logger.info(f"History length: {len(query.history)} turns")
        
        answer = rag_system.ask_with_history(query.question, query.history)
        
        response = ProductRecommendation(
            answer=answer,
            session_id=query.session_id,
            timestamp=datetime.now().isoformat()
        )
        
        if query.session_id:
            conversation_sessions[query.session_id] = query.history + [
                {"role": "user", "content": query.question},
                {"role": "assistant", "content": answer}
            ]
        
        return response
    
    except Exception as e:
        logger.error(f"Error processing conversational query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Retrieve conversation history for a session."""
    if session_id not in conversation_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "history": conversation_sessions[session_id],
        "turn_count": len(conversation_sessions[session_id]) // 2
    }

@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear conversation history for a session."""
    if session_id in conversation_sessions:
        del conversation_sessions[session_id]
    
    return {"message": f"Session {session_id} cleared"}

@app.post("/ingest")
async def trigger_ingestion(background_tasks: BackgroundTasks):
    """
    Trigger product catalog re-ingestion (admin endpoint).
    This would typically be called when the product catalog is updated.
    """
    def run_ingestion():
        try:
            from ingest import ingest_products
            ingest_products()
            logger.info("Product ingestion completed")
        except Exception as e:
            logger.error(f"Ingestion failed: {e}")
    
    background_tasks.add_task(run_ingestion)
    return {"message": "Ingestion started in background"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )