import React from "react";
import { Link } from "react-router-dom";
import "./styles.css";

function Layout({ children }) {
  return (
    <div className="layout">
      {/* Navbar */}
      <nav className="navbar">
        <h1 className="logo">🔹 Fake News Detector</h1>
        <div className="nav-links">
          <Link to="/">Home</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/results">Results</Link>
          <Link to="/login">Login</Link>
          <Link to="/signup">Signup</Link>
        </div>
      </nav>

      {/* Main Content */}
      <main className="content">{children}</main>

      {/* Footer */}
      <footer className="footer">
        <p>© 2025 Fake News Detector | Built for Mini-Project</p>
      </footer>
    </div>
  );
}

export default Layout;
