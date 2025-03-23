import React, { useEffect, useState } from "react";
import axios from "axios";
import "./styles.css";

function Results() {
  const [results, setResults] = useState([]);

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/results");
      setResults(response.data.results);
    } catch (error) {
      console.error("Error fetching results:", error);
    }
  };

  return (
    <div className="centered-content">
      <h2>Past Predictions</h2>
      <p>Here are your past Fake News detections.</p>
      <table className="results-table">
        <thead>
          <tr>
            <th>Email</th>
            <th>News Text</th>
            <th>Prediction</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {results.map((item, index) => (
            <tr key={index}>
              <td>{item.user_email}</td>
              <td>{item.text.substring(0, 50)}...</td> {/* Shortened text */}
              <td className={item.prediction === "Fake" ? "fake" : "real"}>{item.prediction}</td>
              <td>{new Date(item.date).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Results;
