
import React, { useState } from "react";
import axios from "axios";
import { auth } from "./firebaseConfig";
import { useNavigate, Link } from "react-router-dom";
import "./styles.css";

function Dashboard() {
  const navigate = useNavigate();
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLogout = () => {
    auth.signOut();
    navigate("/login");
  };

  const handlePrediction = async () => {
    if (!text.trim()) {
      alert("Please enter some text to analyze.");
      return;
    }

    setLoading(true);
    try {
      const user = auth.currentUser;
      const userEmail = user ? user.email : "guest"; // Store user's email or "guest"

      const response = await axios.post("http://127.0.0.1:5000/predict", { text, user_email: userEmail });
      setResult(response.data.prediction);
    } catch (error) {
      console.error("Error predicting:", error);
      setResult("Error processing the request.");
    }
    setLoading(false);
  };

  return (
    <div className="centered-content">
      <h2>Dashboard</h2>
      <p>Welcome! Use the Fake News Detector below.</p>
      
      <textarea
        rows="4"
        cols="50"
        placeholder="Enter news text..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        required
      />
      <br></br>
      <button className="btn-glow" onClick={handlePrediction} disabled={loading}>
        {loading ? "Checking..." : "Check News"}
      </button>

      {result && (
        <div className={`result-box ${result === "Fake" ? "fake" : "real"}`}>
          Prediction: {result}
        </div>
      )}


      <Link to="/results"><button className="btn-glow">View Past Results</button></Link>
      <button className="btn-danger" onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default Dashboard;
