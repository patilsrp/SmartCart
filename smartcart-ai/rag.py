import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain.schema import BaseMessage, HumanMessage, AIMessage
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class SmartCartRAG:
    def __init__(self):
        """Initialize the RAG system with embeddings, vector store, and LLM."""
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        connection_string = os.environ.get("PG_CONN")
        if not connection_string:
            raise ValueError("PG_CONN environment variable not set!")
        
        self.store = PGVector(
            embeddings=self.embeddings,
            collection_name="products",
            connection=connection_string,
            use_jsonb=True
        )
        
        self.retriever = self.store.as_retriever(
            search_kwargs={"k": 4}
        )
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            max_tokens=500
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are SmartCart's helpful shopping assistant. Your goal is to help customers find the perfect products from our catalog.

Instructions:
- Recommend ONLY from the products provided below
- Be concise but friendly
- Explain WHY each product matches their needs
- If nothing fits perfectly, suggest the closest alternatives and explain the trade-offs
- Format prices with ₹ symbol
- If asked about products we don't have, politely say we don't carry them

Available Products:
{context}

Remember: You can only recommend products from the list above."""),
            MessagesPlaceholder(variable_name="history", optional=True),
            ("human", "{question}")
        ])
        
        self.chain = self._build_chain()
    
    def _format_products(self, docs: List[Document]) -> str:
        """Format retrieved products for the prompt context."""
        if not docs:
            return "No products found matching your criteria."
        
        formatted = []
        for i, doc in enumerate(docs, 1):
            meta = doc.metadata
            product_info = (
                f"{i}. {meta['name']} ({meta['brand']})\n"
                f"   Price: ₹{meta['price']:,}\n"
                f"   Category: {meta['category']}\n"
                f"   Description: {meta['description']}"
            )
            formatted.append(product_info)
        
        return "\n\n".join(formatted)
    
    def _extract_price_filter(self, question: str) -> Optional[Dict[str, Any]]:
        """Extract price constraints from the question."""
        filters = {}
        
        under_match = re.search(r'under\s+₹?(\d+)[k]?\b', question, re.IGNORECASE)
        if under_match:
            price = int(under_match.group(1))
            if 'k' in question.lower():
                price *= 1000
            filters["price"] = {"$lte": price}
            return filters
        
        below_match = re.search(r'below\s+₹?(\d+)[k]?\b', question, re.IGNORECASE)
        if below_match:
            price = int(below_match.group(1))
            if 'k' in question.lower():
                price *= 1000
            filters["price"] = {"$lte": price}
            return filters
        
        less_than_match = re.search(r'less\s+than\s+₹?(\d+)[k]?\b', question, re.IGNORECASE)
        if less_than_match:
            price = int(less_than_match.group(1))
            if 'k' in question.lower():
                price *= 1000
            filters["price"] = {"$lte": price}
            return filters
        
        cheap_match = re.search(r'cheap|budget|affordable|economical', question, re.IGNORECASE)
        if cheap_match:
            filters["price"] = {"$lte": 50000}
            return filters
        
        return None
    
    def _build_chain(self):
        """Build the LangChain RAG pipeline."""
        def retrieve_with_filters(inputs):
            question = inputs.get("question", "")
            price_filter = self._extract_price_filter(question)
            
            if price_filter:
                search_kwargs = {"k": 6, "filter": price_filter}
            else:
                search_kwargs = {"k": 4}
            
            retriever = self.store.as_retriever(search_kwargs=search_kwargs)
            docs = retriever.invoke(question)
            return self._format_products(docs)
        
        chain = (
            {
                "context": RunnableLambda(retrieve_with_filters),
                "question": RunnablePassthrough(),
                "history": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        return chain
    
    def ask(self, question: str, history: Optional[List[BaseMessage]] = None) -> str:
        """
        Process a question through the RAG pipeline.
        
        Args:
            question: The user's question
            history: Optional conversation history
        
        Returns:
            The AI assistant's response
        """
        try:
            inputs = {
                "question": question,
                "history": history or []
            }
            response = self.chain.invoke(inputs)
            return response
        except Exception as e:
            logger.error(f"Error in RAG chain: {e}")
            return "I apologize, but I encountered an error while searching for products. Please try again."
    
    def ask_with_history(self, question: str, conversation_history: List[Dict[str, str]]) -> str:
        """
        Process a question with conversation history.
        
        Args:
            question: The user's question
            conversation_history: List of {"role": "user/assistant", "content": "..."} dicts
        
        Returns:
            The AI assistant's response
        """
        messages = []
        for turn in conversation_history:
            if turn["role"] == "user":
                messages.append(HumanMessage(content=turn["content"]))
            elif turn["role"] == "assistant":
                messages.append(AIMessage(content=turn["content"]))
        
        return self.ask(question, messages)

def create_rag_instance():
    """Factory function to create a RAG instance."""
    return SmartCartRAG()

if __name__ == "__main__":
    rag = SmartCartRAG()
    
    test_queries = [
        "Show me a quiet laptop under 60k for college",
        "I need a budget smartphone with good camera",
        "What tablets do you have?",
        "Looking for noise canceling headphones"
    ]
    
    print("Testing RAG system with sample queries:\n")
    for query in test_queries:
        print(f"Q: {query}")
        response = rag.ask(query)
        print(f"A: {response}\n")
        print("-" * 80 + "\n")