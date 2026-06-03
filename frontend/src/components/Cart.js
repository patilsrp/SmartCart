import React from 'react';
import { useCart } from '../context/CartContext';
import { toast } from 'react-toastify';

const Cart = () => {
  const { cart, removeFromCart, updateQuantity, getCartTotal, clearCart } = useCart();

  const handleCheckout = () => {
    if (cart.length === 0) {
      toast.error('Your cart is empty!');
      return;
    }
    
    toast.success('Order placed successfully!');
    clearCart();
  };

  if (cart.length === 0) {
    return (
      <div className="container">
        <div className="cart-container">
          <div className="empty-cart">
            <h2>Your Cart is Empty</h2>
            <p>Add some products to get started!</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="cart-container">
        <h2>Shopping Cart ({cart.length} items)</h2>
        
        {cart.map(item => (
          <div key={item.id} className="cart-item">
            <div className="cart-item-info">
              <div className="cart-item-title">{item.name}</div>
              <div className="cart-item-price">₹{item.price?.toLocaleString()}</div>
            </div>
            
            <div className="quantity-controls">
              <button 
                className="quantity-btn"
                onClick={() => updateQuantity(item.id, item.quantity - 1)}
              >
                -
              </button>
              <span>{item.quantity}</span>
              <button 
                className="quantity-btn"
                onClick={() => updateQuantity(item.id, item.quantity + 1)}
              >
                +
              </button>
              <button 
                style={{ marginLeft: '1rem', color: '#f44336', cursor: 'pointer', border: 'none', background: 'none' }}
                onClick={() => removeFromCart(item.id)}
              >
                Remove
              </button>
            </div>
          </div>
        ))}
        
        <div className="cart-total">
          <div className="total-amount">
            Total: ₹{getCartTotal().toLocaleString()}
          </div>
          <button className="checkout-btn" onClick={handleCheckout}>
            Proceed to Checkout
          </button>
        </div>
      </div>
    </div>
  );
};

export default Cart;