import requests
import sqlite3
from config import NEWS_API_KEY, NEWS_API_URL

def fetch_news():
    """Fetch latest news articles from NewsAPI and store them in the database."""
    params = {
        "apiKey": NEWS_API_KEY,
        "country": "us",  # Fetch US news (change as needed)
        "category": "general",  # Can be business, tech, etc.
        "pageSize": 10  # Limit to 10 articles
    }
    
    response = requests.get(NEWS_API_URL, params=params)
    
    if response.status_code == 200:
        news_data = response.json().get("articles", [])
        store_news(news_data)
    else:
        print("Error fetching news:", response.status_code, response.text)

def store_news(news_list):
    """Store fetched news articles in an SQLite database."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            url TEXT,
            source TEXT,
            published_at TEXT
        )
    """)
    
    # Insert news into database
    for news in news_list:
        cursor.execute("""
            INSERT INTO news (title, description, url, source, published_at)
            VALUES (?, ?, ?, ?, ?)
        """, (news["title"], news["description"], news["url"], news["source"]["name"], news["publishedAt"]))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fetch_news()  # Run script to fetch and store news
