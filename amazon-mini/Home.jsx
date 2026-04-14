import img1 from "../assets/1.jpeg";
import img2 from "../assets/2.jpeg";
import img3 from "../assets/3.jpeg";
import img4 from "../assets/4.jpeg";
import img5 from "../assets/5.jpeg";
import img6 from "../assets/6.jpeg";

import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import HeroBanner from "../components/HeroBanner";
import ProductCard from "../components/ProductCard";

const categoryData = [
  { name: "Electronics", image: img1 },
  { name: "Books", image: img2 },
  { name: "Fashion", image: img3 },
  { name: "Home & Kitchen", image: img4 },
  { name: "Sports", image: img5 },
  { name: "Beauty", image: img6 },
];

function Home() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/products")
      .then((res) => {
        console.log("API DATA:", res.data);
        setProducts(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const deals = products.filter((p) => p.badge === "Deal of the Day");
  const bestSellers = products.filter((p) => p.badge === "Best Seller");
  const topRated = [...products]
    .sort((a, b) => b.rating - a.rating)
    .slice(0, 8);

  return (
    <div>
      <Navbar />
      <HeroBanner />

      {/* ✅ Category Cards */}
      <div className="categories-grid">
        {categoryData.map((cat) => (
          <Link
            key={cat.name}
            to={`/search?category=${encodeURIComponent(cat.name)}`}
            className="category-card"
          >
            <h3 className="category-card-title">{cat.name}</h3>

            <div className="category-card-image">
              <img
                src={cat.image}
                alt={cat.name}
                className="category-img"
              />
            </div>

            <span className="category-card-link">See all deals →</span>
          </Link>
        ))}
      </div>

      {loading ? (
        <div className="spinner-container">
          <div className="spinner" />
        </div>
      ) : (
        <>
          {/* 🔥 Deals Section */}
          {deals.length > 0 && (
            <div className="deals-scroll-section">
              <h2>Today's Deals</h2>
              <div className="deals-scroll">
                {deals.map((product) => (
                  <Link
                    to={`/product/${product._id}`}
                    key={product._id}
                    className="deal-card"
                  >
                    <img
                      src={product.image}
                      alt={product.name}
                      className="deal-card-image"
                    />

                    <div className="deal-card-discount">
                      Up to{" "}
                      {Math.round(
                        ((product.originalPrice - product.price) /
                          product.originalPrice) *
                        100
                      )}
                      % off
                    </div>

                    <div className="deal-card-title">
                      {product.name}
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {/* 🏆 Best Sellers */}
          {bestSellers.length > 0 && (
            <>
              <div className="section-header">
                <h2 className="section-title">Best Sellers</h2>
              </div>

              <div className="products-grid">
                {bestSellers.map((p) => (
                  <ProductCard key={p._id} product={p} />
                ))}
              </div>
            </>
          )}

          {/* ⭐ Top Rated */}
          <div className="section-header">
            <h2 className="section-title">Top Rated Products</h2>
          </div>

          <div className="products-grid">
            {topRated.map((p) => (
              <ProductCard key={p._id} product={p} />
            ))}
          </div>

          {/* ✅ FALLBACK (IMPORTANT FIX) */}
          {products.length > 0 && (
            <>
              <div className="section-header">
                <h2 className="section-title">All Products</h2>
              </div>

              <div className="products-grid">
                {products.map((p) => (
                  <ProductCard key={p._id} product={p} />
                ))}
              </div>
            </>
          )}
        </>
      )}

      <Footer />
    </div>
  );
}

export default Home;