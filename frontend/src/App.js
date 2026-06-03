import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';
import ProductList from './components/ProductList';
import Cart from './components/Cart';
import ChatAssistant from './components/ChatAssistant';
import SearchBar from './components/SearchBar';
import { CartProvider } from './context/CartContext';
import { AuthProvider } from './context/AuthContext';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [showChat, setShowChat] = useState(false);

  return (
    <AuthProvider>
      <CartProvider>
        <Router>
          <div className="App">
            <header className="app-header">
              <div className="container">
                <div className="header-content">
                  <Link to="/" className="logo">
                    <h1>🛒 SmartCart</h1>
                  </Link>
                  <SearchBar onSearch={setSearchQuery} />
                  <nav className="nav-menu">
                    <Link to="/" className="nav-link">Products</Link>
                    <Link to="/cart" className="nav-link">Cart</Link>
                    <button 
                      className="chat-toggle-btn"
                      onClick={() => setShowChat(!showChat)}
                    >
                      💬 AI Assistant
                    </button>
                  </nav>
                </div>
              </div>
            </header>

            <main className="main-content">
              <Routes>
                <Route path="/" element={<ProductList searchQuery={searchQuery} />} />
                <Route path="/cart" element={<Cart />} />
              </Routes>
            </main>

            {showChat && (
              <ChatAssistant onClose={() => setShowChat(false)} />
            )}

            <ToastContainer position="bottom-right" />
          </div>
        </Router>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;