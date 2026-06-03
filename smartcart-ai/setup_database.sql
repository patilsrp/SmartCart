-- Enable pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a dedicated schema for AI-related tables (optional)
CREATE SCHEMA IF NOT EXISTS smartcart_ai;

-- Grant permissions if needed
-- GRANT ALL ON SCHEMA smartcart_ai TO your_user;

-- Show installed extensions to verify
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Example: Create a test table to verify vector functionality
CREATE TABLE IF NOT EXISTS test_vectors (
    id SERIAL PRIMARY KEY,
    embedding vector(384)  -- 384 dimensions for all-MiniLM-L6-v2
);

-- Clean up test table
DROP TABLE IF EXISTS test_vectors;

COMMENT ON EXTENSION vector IS 'pgvector extension for SmartCart RAG system - enables similarity search on product embeddings';