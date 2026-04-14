import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import axios from "axios";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import ProductCard from "../components/ProductCard";

function Search() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sort, setSort] = useState(searchParams.get("sort") || "");

  const query = searchParams.get("q") || "";
  const category = searchParams.get("category") || "";

  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams();
    if (query) params.set("search", query);
    if (category) params.set("category", category);
    if (sort) params.set("sort", sort);

    axios
      .get(`http://localhost:5000/api/products?${params.toString()}`)
      .then((res) => {
        setProducts(res.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [query, category, sort]);

  const handleSortChange = (e) => {
    const newSort = e.target.value;
    setSort(newSort);
    const newParams = new URLSearchParams(searchParams);
    if (newSort) {
      newParams.set("sort", newSort);
    } else {
      newParams.delete("sort");
    }
    setSearchParams(newParams);
  };

  const displayTitle = category
    ? category
    : query
    ? `Results for "${query}"`
    : "All Products";

  return (
    <div>
      <Navbar />

      <div className="search-results-page">
        {/* Header */}
        <div className="search-results-header">
          <div>
            <h2 style={{ fontSize: 22, fontWeight: 700, marginBottom: 4 }}>
              {displayTitle}
            </h2>
            <span className="search-results-count">
              {loading ? (
                "Loading..."
              ) : (
                <>
                  Showing <strong>{products.length}</strong> results
                  {query && (
                    <>
                      {" "}
                      for <strong>&quot;{query}&quot;</strong>
                    </>
                  )}
                </>
              )}
            </span>
          </div>

          <select
            className="search-sort-select"
            value={sort}
            onChange={handleSortChange}
          >
            <option value="">Sort by: Featured</option>
            <option value="price-low">Price: Low to High</option>
            <option value="price-high">Price: High to Low</option>
            <option value="rating">Avg. Customer Reviews</option>
            <option value="reviews">Most Reviews</option>
          </select>
        </div>

        {/* Category Filters */}
        <div
          style={{
            display: "flex",
            gap: 8,
            marginBottom: 16,
            flexWrap: "wrap",
          }}
        >
          <Link
            to="/search"
            style={{
              padding: "6px 14px",
              borderRadius: 20,
              fontSize: 13,
              fontWeight: 500,
              background: !category ? "var(--amazon-dark)" : "#f0f2f2",
              color: !category ? "#fff" : "var(--amazon-text)",
              border: "1px solid var(--amazon-border)",
            }}
          >
            All
          </Link>
          {["Electronics", "Books", "Fashion", "Home & Kitchen", "Sports", "Beauty"].map(
            (cat) => (
              <Link
                key={cat}
                to={`/search?category=${encodeURIComponent(cat)}${
                  query ? `&q=${encodeURIComponent(query)}` : ""
                }`}
                style={{
                  padding: "6px 14px",
                  borderRadius: 20,
                  fontSize: 13,
                  fontWeight: 500,
                  background:
                    category === cat ? "var(--amazon-dark)" : "#f0f2f2",
                  color: category === cat ? "#fff" : "var(--amazon-text)",
                  border: "1px solid var(--amazon-border)",
                }}
              >
                {cat}
              </Link>
            )
          )}
        </div>

        {/* Results */}
        {loading ? (
          <div className="spinner-container">
            <div className="spinner" />
          </div>
        ) : products.length === 0 ? (
          <div style={{ textAlign: "center", padding: 60 }}>
            <span style={{ fontSize: 48, display: "block", marginBottom: 16 }}>
              🔍
            </span>
            <h2>No results found</h2>
            <p style={{ color: "var(--amazon-text-light)", marginBottom: 16 }}>
              Try different keywords or browse categories
            </p>
            <Link to="/">
              <button className="cart-checkout-btn" style={{ maxWidth: 200 }}>
                Go Home
              </button>
            </Link>
          </div>
        ) : (
          <div className="products-grid">
            {products.map((p) => (
              <ProductCard key={p.id} product={p} />
            ))}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}

export default Search;
