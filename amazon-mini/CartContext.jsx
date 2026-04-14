import { createContext, useContext, useState, useCallback } from "react";

const CartContext = createContext();

export function CartProvider({ children }) {
  const [cart, setCart] = useState(() => {
    try {
      const saved = localStorage.getItem("amazon_cart");
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [toast, setToast] = useState({ show: false, message: "" });

  const saveCart = (newCart) => {
    setCart(newCart);
    localStorage.setItem("amazon_cart", JSON.stringify(newCart));
  };

  const showToast = useCallback((message) => {
    setToast({ show: true, message });
    setTimeout(() => setToast({ show: false, message: "" }), 2500);
  }, []);

  const addToCart = (product) => {
    const pid = product._id || product.id;
    const existing = cart.find((item) => (item._id || item.id) === pid);
    if (existing) {
      const updated = cart.map((item) =>
        (item._id || item.id) === pid ? { ...item, qty: item.qty + 1 } : item
      );
      saveCart(updated);
    } else {
      saveCart([...cart, { ...product, qty: 1 }]);
    }
    showToast(`✓ ${product.name} added to cart`);
  };

  const removeFromCart = (productId) => {
    const updated = cart.filter((item) => (item._id || item.id) !== productId);
    saveCart(updated);
    showToast("Item removed from cart");
  };

  const updateQty = (productId, qty) => {
    if (qty < 1) {
      removeFromCart(productId);
      return;
    }
    const updated = cart.map((item) =>
      (item._id || item.id) === productId ? { ...item, qty } : item
    );
    saveCart(updated);
  };

  const clearCart = () => {
    saveCart([]);
  };

  const cartCount = cart.reduce((sum, item) => sum + item.qty, 0);
  const cartTotal = cart.reduce((sum, item) => sum + item.price * item.qty, 0);

  return (
    <CartContext.Provider
      value={{
        cart,
        addToCart,
        removeFromCart,
        updateQty,
        clearCart,
        cartCount,
        cartTotal,
        toast,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error("useCart must be used within CartProvider");
  return ctx;
}
