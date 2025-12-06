import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("data", "content.db")

def init_db():
    """Initialize the SQLite database."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            keywords TEXT,
            content TEXT,
            seo_score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_article(topic: str, keywords: list[str], content: str, seo_score: int):
    """Save a generated article to the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    keywords_str = ", ".join(keywords)
    c.execute('''
        INSERT INTO articles (topic, keywords, content, seo_score)
        VALUES (?, ?, ?, ?)
    ''', (topic, keywords_str, content, seo_score))
    conn.commit()
    conn.close()

def get_articles():
    """Retrieve all saved articles."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, topic, keywords, content, seo_score, created_at FROM articles ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return rows
