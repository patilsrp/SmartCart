import React, { useState, useEffect } from 'react';
import { useCart } from '../context/CartContext';
import { toast } from 'react-toastify';
import api from '../services/api';

const ProductList = ({ searchQuery }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { addToCart } = useCart();

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await api.get('/products');
      setProducts(response.data);
    } catch (err) {
      setError('Failed to load products');
      console.error('Error fetching products:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = (product) => {
    addToCart(product);
    toast.success(`${product.name} added to cart!`);
  };

  const filteredProducts = products.filter(product => 
    searchQuery === '' || 
    product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    product.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    product.category?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const getCategoryEmoji = (category) => {
    const emojis = {
      laptop: '💻',
      smartphone: '📱',
      tablet: '📱',
      headphones: '🎧',
      earbuds: '🎧',
      'e-reader': '📚',
      default: '📦'
    };
    return emojis[category?.toLowerCase()] || emojis.default;
  };

  if (loading) return <div className="loading">Loading products...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="container">
      <h2 style={{ marginBottom: '2rem' }}>
        {searchQuery ? `Results for "${searchQuery}"` : 'All Products'}
      </h2>
      
      {filteredProducts.length === 0 ? (
        <div className="empty-cart">
          <p>No products found matching your search.</p>
        </div>
      ) : (
        <div className="product-grid">
          {filteredProducts.map(product => (
            <div key={product.id} className="product-card">
              <div className="product-image">
                {getCategoryEmoji(product.category)}
              </div>
              <h3 className="product-title">{product.name}</h3>
              <p className="product-brand">{product.brand}</p>
              <p className="product-description">{product.description}</p>
              <div className="product-price">₹{product.price?.toLocaleString()}</div>
              <button 
                className="add-to-cart-btn"
                onClick={() => handleAddToCart(product)}
              >
                Add to Cart
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProductList;