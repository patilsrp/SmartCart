# SmartCart AI Service - RAG Implementation

A production-ready Retrieval-Augmented Generation (RAG) system for conversational commerce, built with LangChain, pgvector, HuggingFace, and OpenAI.

## Architecture

```
React Frontend → Spring Boot → Python AI Service (FastAPI)
                                      ↓
                    ┌─────────────────┼──────────────┐
                    ↓                 ↓              ↓
            HuggingFace          pgvector       OpenAI
           (embeddings)      (vector store)  (generation)
```

## Tech Stack

- **Python** - Core AI service implementation
- **FastAPI** - REST API framework
- **LangChain** - RAG orchestration and chains
- **HuggingFace** - Sentence transformer embeddings (`all-MiniLM-L6-v2`)
- **OpenAI API** - LLM generation (`gpt-4o-mini`)
- **pgvector** - PostgreSQL vector similarity search
- **Spring Boot** - Backend integration

## Setup

### 1. Install Dependencies

```bash
cd smartcart-ai
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and set:

```env
OPENAI_API_KEY=sk-your-api-key
PG_CONN=postgresql+psycopg://user:password@localhost:5432/smartcart
```

### 3. Setup Database

Enable pgvector extension:

```bash
psql -U your_user -d smartcart -f setup_database.sql
```

### 4. Ingest Products

```bash
python ingest.py
```

This embeds your product catalog into the vector store.

### 5. Start the Service

```bash
uvicorn main:app --reload --port 8001
```

API will be available at `http://localhost:8001`

## API Endpoints

### Single-turn Recommendation
```
POST /recommend
{
  "question": "Show me a quiet laptop under 60k for college",
  "session_id": "optional-session-id"
}
```

### Multi-turn Conversation
```
POST /recommend/conversational
{
  "question": "Now show me cheaper ones",
  "history": [
    {"role": "user", "content": "Show me laptops"},
    {"role": "assistant", "content": "..."}
  ],
  "session_id": "session-123"
}
```

### Health Check
```
GET /health
```

### API Documentation
```
GET /docs
```

## Testing

Run the evaluation suite:

```bash
python test_rag.py
```

This runs 10 test queries and measures:
- Product recall
- Keyword coverage
- Response quality
- Conversational continuity

## Spring Boot Integration

The Spring Boot application integrates via `AIRecommendationService`:

```java
@Autowired
private AIRecommendationService aiService;

AIRecommendationResponse response = aiService.getRecommendation(
    "Show me gaming laptops",
    sessionId
);
```

Configure the AI service URL in `application.properties`:

```properties
ai.service.url=http://localhost:8001
```

## Key Features

1. **Semantic Search**: Uses HuggingFace embeddings to understand query meaning
2. **Price Filtering**: Automatically extracts and applies price constraints
3. **Conversation Memory**: Maintains context across multiple turns
4. **Grounded Generation**: LLM only recommends products from your catalog
5. **Production Ready**: Error handling, health checks, logging

## How It Works

1. **Query Processing**: User question is embedded using HuggingFace
2. **Vector Search**: pgvector finds semantically similar products
3. **Context Building**: Top-k products formatted as prompt context
4. **Generation**: OpenAI LLM generates natural recommendation
5. **Response**: Structured JSON returned to Spring Boot

## Performance

- Embedding: ~50ms (CPU)
- Vector search: ~20ms (pgvector)
- Generation: ~500-1000ms (OpenAI)
- Total latency: ~1-1.5s per request

## Cost Optimization

- **Free embeddings**: HuggingFace runs locally
- **Cheap generation**: gpt-4o-mini costs ~$0.15 per 1M input tokens
- **Estimated cost**: <$1 for 1000 queries

## Interview Talking Points

- **Why separate Python service?**: Clean microservice boundary, Python AI ecosystem
- **Why pgvector?**: Production-ready vector DB with zero new infrastructure
- **Why HF + OpenAI split?**: Cost optimization - free embeddings, quality generation
- **RAG benefits**: Grounded responses, no hallucination, always current catalog