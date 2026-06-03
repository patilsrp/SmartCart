import React, { useState, useRef, useEffect } from 'react';
import api from '../services/api';
import { useCart } from '../context/CartContext';
import { toast } from 'react-toastify';

const ChatAssistant = ({ onClose }) => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! I\'m your SmartCart AI assistant. I can help you find the perfect products. What are you looking for today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const messagesEndRef = useRef(null);
  const { addToCart } = useCart();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const extractProductRecommendations = (text) => {
    const productPattern = /(\d+)\.\s*([^(]+)\s*\(([^)]+)\)\s*Price:\s*₹([\d,]+)/g;
    const products = [];
    let match;

    while ((match = productPattern.exec(text)) !== null) {
      products.push({
        name: match[2].trim(),
        brand: match[3].trim(),
        price: parseInt(match[4].replace(/,/g, ''))
      });
    }

    return products;
  };

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const history = messages.map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      const response = await api.post('/ai/recommend/conversational', {
        question: input,
        history: history,
        session_id: sessionId
      });

      const assistantMessage = { 
        role: 'assistant', 
        content: response.data.answer,
        products: extractProductRecommendations(response.data.answer)
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, I\'m having trouble connecting right now. Please try again.' 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const quickAddToCart = async (productName) => {
    try {
      const response = await api.get('/products');
      const product = response.data.find(p => 
        p.name.toLowerCase().includes(productName.toLowerCase())
      );
      
      if (product) {
        addToCart(product);
        toast.success(`${product.name} added to cart!`);
      }
    } catch (error) {
      console.error('Error adding to cart:', error);
    }
  };

  return (
    <div className="chat-assistant">
      <div className="chat-header">
        <h3>AI Shopping Assistant</h3>
        <button 
          style={{ background: 'none', border: 'none', color: 'white', fontSize: '1.5rem', cursor: 'pointer' }}
          onClick={onClose}
        >
          ×
        </button>
      </div>
      
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.content}
              {msg.products && msg.products.length > 0 && (
                <div style={{ marginTop: '0.5rem' }}>
                  {msg.products.map((product, idx) => (
                    <button
                      key={idx}
                      style={{
                        display: 'block',
                        margin: '0.25rem 0',
                        padding: '0.25rem 0.5rem',
                        background: '#667eea',
                        color: 'white',
                        border: 'none',
                        borderRadius: '3px',
                        cursor: 'pointer',
                        fontSize: '0.85rem'
                      }}
                      onClick={() => quickAddToCart(product.name)}
                    >
                      Quick Add: {product.name}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="message-content">
              <span style={{ fontStyle: 'italic' }}>Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="chat-input-container">
        <input
          type="text"
          className="chat-input"
          placeholder="Ask about products..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
        />
        <button 
          className="chat-send-btn"
          onClick={sendMessage}
          disabled={loading || !input.trim()}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatAssistant;