import React from "react";
import { Link } from "react-router-dom";
import "./styles.css";

function Home() {
  return (
    <div className="centered-content">
      <h1 className="title">Fake News Detector</h1>
      <p>Verify news authenticity with AI-powered detection.</p>
      <Link to="/signup">
        <button className="btn-glow">Get Started</button>
      </Link>
    </div>
  );
}

export default Home;
