import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";

const categoryIcons = {
  Electronics: "📱",
  Books: "📖",
  Fashion: "👟",
  "Home & Kitchen": "🏠",
  Sports: "⚽",
  Beauty: "💄",
};

function getStars(rating) {
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5 ? 1 : 0;
  const empty = 5 - full - half;
  return "★".repeat(full) + (half ? "½" : "") + "☆".repeat(empty);
}

function formatPrice(price) {
  return price.toLocaleString("en-IN");
}

function ProductCard({ product }) {
  const { addToCart } = useCart();

  const discount = Math.round(
    ((product.originalPrice - product.price) / product.originalPrice) * 100
  );

  const icon = categoryIcons[product.category] || "📦";

  const badgeClass = product.badge
    ? product.badge === "Best Seller"
      ? "best-seller"
      : product.badge === "Amazon's Choice"
        ? "amazons-choice"
        : "deal"
    : "";

  return (
    <div className="product-card">
      {product.badge && (
        <span className={`product-card-badge ${badgeClass}`}>
          {product.badge}
        </span>
      )}

      {/* ✅ FIXED _id */}
      <Link to={`/product/${product._id}`}>
        <div className="product-card-image-wrapper">
          {product.image ? (
            <img
              src={product.image}
              alt={product.name}
              className="product-card-image"
              onError={(e) => {
                e.target.style.display = "none";
                e.target.parentElement.innerHTML = `<div class="product-card-image-placeholder" style="background: ${product.imageColor || '#f0f0f0'}">${icon}</div>`;
              }}
            />
          ) : (
            <div
              className="product-card-image-placeholder"
              style={{ background: product.imageColor || "#f0f0f0" }}
            >
              {icon}
            </div>
          )}
        </div>
      </Link>

      <div className="product-card-info">
        <div className="product-card-brand">{product.brand}</div>

        {/* ✅ FIXED _id */}
        <Link to={`/product/${product._id}`}>
          <div className="product-card-name">{product.name}</div>
        </Link>

        <div className="product-card-rating">
          <span className="stars">{getStars(product.rating)}</span>
          <span className="rating-count">
            {product.reviews?.toLocaleString?.() || 0}
          </span>
        </div>

        <div className="product-card-price">
          {discount > 0 && (
            <span className="price-discount">-{discount}%</span>
          )}
          <span className="price-symbol">₹</span>
          <span className="price-value">{formatPrice(product.price)}</span>
        </div>

        {product.originalPrice > product.price && (
          <div>
            <span className="price-original">
              M.R.P: ₹{formatPrice(product.originalPrice)}
            </span>
          </div>
        )}

        <div className="product-card-delivery">
          FREE Delivery by Amazon
        </div>

        <button
          className="product-card-add-btn"
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            addToCart(product);
          }}
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
}

export default ProductCard;
export { getStars, formatPrice, categoryIcons };