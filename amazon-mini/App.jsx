import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useCart } from "./context/CartContext";
import Home from "./pages/Home";
import Cart from "./pages/Cart";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import ProductDetail from "./pages/ProductDetail";
import Search from "./pages/Search";
import Checkout from "./pages/Checkout";
import OrderSuccess from "./pages/OrderSuccess";

function ToastNotification() {
  const { toast } = useCart();
  return <div className={`toast ${toast.show ? "show" : ""}`}>{toast.message}</div>;
}

function App() {
  return (
    <BrowserRouter>
      <ToastNotification />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/product/:id" element={<ProductDetail />} />
        <Route path="/search" element={<Search />} />
        <Route path="/checkout" element={<Checkout />} />
        <Route path="/order-success" element={<OrderSuccess />} />
        <Route
          path="*"
          element={
            <div style={{ textAlign: "center", padding: 80 }}>
              <span style={{ fontSize: 64, display: "block", marginBottom: 16 }}>
                🔍
              </span>
              <h2>Page Not Found</h2>
              <p style={{ color: "#565959", marginBottom: 20 }}>
                The page you are looking for doesn&apos;t exist.
              </p>
              <a href="/" style={{ color: "#007185" }}>
                Go to Home
              </a>
            </div>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;