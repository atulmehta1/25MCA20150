import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";

const categories = [
  "All",
  "Electronics",
  "Books",
  "Fashion",
  "Home & Kitchen",
  "Sports",
  "Beauty",
];

function Navbar() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const { cartCount } = useCart();
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (searchTerm.trim()) params.set("q", searchTerm.trim());
    if (selectedCategory !== "All") params.set("category", selectedCategory);
    navigate(`/search?${params.toString()}`);
  };

  return (
    <nav className="navbar">
      <div className="navbar-main">
        {/* Logo */}
        <Link to="/" className="navbar-logo">
          <span className="navbar-logo-text">Urbankart</span>
          <span className="navbar-logo-suffix">.com</span>
        </Link>

        {/* Deliver To */}
        <div className="navbar-deliver">
          <span className="navbar-deliver-label">Deliver to</span>
          <span className="navbar-deliver-location">
            📍 India
          </span>
        </div>

        {/* Search Bar */}
        <form className="navbar-search" onSubmit={handleSearch}>
          <select
            className="navbar-search-category"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
          <input
            type="text"
            className="navbar-search-input"
            placeholder="Search Amazon.in"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <button type="submit" className="navbar-search-btn">
            <svg viewBox="0 0 24 24">
              <path d="M10.5 2a8.5 8.5 0 015.664 14.869l5.345 5.345a1 1 0 01-1.414 1.414l-5.345-5.345A8.5 8.5 0 1110.5 2zm0 2a6.5 6.5 0 100 13 6.5 6.5 0 000-13z" />
            </svg>
          </button>
        </form>

        {/* Right Actions */}
        <div className="navbar-actions">
          {/* Account */}
          {user ? (
            <div className="navbar-action" onClick={logout} title="Click to logout">
              <span className="navbar-action-label">Hello, {user.name}</span>
              <span className="navbar-action-value">Sign Out</span>
            </div>
          ) : (
            <Link to="/login" className="navbar-action">
              <span className="navbar-action-label">Hello, sign in</span>
              <span className="navbar-action-value">Account & Lists</span>
            </Link>
          )}

          {/* Orders */}
          <Link to="/orders" className="navbar-action">
            <span className="navbar-action-label">Returns</span>
            <span className="navbar-action-value">& Orders</span>
          </Link>

          {/* Cart */}
          <Link to="/cart" className="navbar-cart">
            <div className="navbar-cart-icon">
              🛒
              {cartCount > 0 && (
                <span className="navbar-cart-count">{cartCount}</span>
              )}
            </div>
            <span className="navbar-cart-text">Cart</span>
          </Link>
        </div>
      </div>

      {/* Sub Navigation */}
      <div className="navbar-sub-wrapper">
        <div className="navbar-sub">
          <Link to="/search?category=Electronics" className="navbar-sub-link">
            📱 Electronics
          </Link>
          <Link to="/search?category=Books" className="navbar-sub-link">
            📚 Books
          </Link>
          <Link to="/search?category=Fashion" className="navbar-sub-link">
            👕 Fashion
          </Link>
          <Link to="/search?category=Home & Kitchen" className="navbar-sub-link">
            🏠 Home & Kitchen
          </Link>
          <Link to="/search?category=Sports" className="navbar-sub-link">
            ⚽ Sports
          </Link>
          <Link to="/search?category=Beauty" className="navbar-sub-link">
            💄 Beauty
          </Link>
          <span className="navbar-sub-link" style={{ color: "#fff", fontWeight: 700 }}>
            🔥 Today's Deals
          </span>
          <span className="navbar-sub-link">🆕 New Releases</span>
          <span className="navbar-sub-link">⭐ Customer Service</span>
          <span className="navbar-sub-link">🎁 Gift Cards</span>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;