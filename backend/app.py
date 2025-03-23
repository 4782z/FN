from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import joblib
from flask import request

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Load trained Fake News Detection model
model = joblib.load("opmodel.pkl")

def create_table():
    """Create database table if it doesn't exist."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            text TEXT,
            prediction TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

create_table()  # Ensure table exists at startup

@app.route("/predict", methods=["POST"])
def predict():
    """Predict whether the given text is Fake or Real and store the result."""
    data = request.json
    text = data.get("text", "")
    user_email = data.get("user_email", "guest")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    prediction = model.predict([text])[0]
    label = "Fake" if prediction == 1 else "Real"

    # Store the prediction in the database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO predictions (user_email, text, prediction) VALUES (?, ?, ?)", 
                   (user_email, text, label))
    conn.commit()
    conn.close()

    return jsonify({"prediction": label})

@app.route("/results", methods=["GET"])
def get_results():
    """Fetch past predictions from the database."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_email, text, prediction, date FROM predictions ORDER BY date DESC")
    results = cursor.fetchall()
    conn.close()

    results_list = [
        {"user_email": row[0], "text": row[1], "prediction": row[2], "date": row[3]} 
        for row in results
    ]
    
    return jsonify({"results": results_list})
#@app.route("/news", methods=["GET"])
#def news():
#    """API endpoint to get stored news articles."""
#    news_list = get_news()
#    return jsonify({"news": news_list, "count": len(news_list)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
