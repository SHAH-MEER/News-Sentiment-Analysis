import requests
import streamlit as st
from typing import List, Dict

def fetch_news(query: str, from_date: str = None, to_date: str = None, page_size: int = 50) -> List[Dict]:
    """
    Fetch news articles from NewsAPI by keyword/topic and optional date range.
    Returns a list of dicts with keys: title, source, publishedAt, content.
    """
    api_key = st.secrets["NEWS_API_KEY"]
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": api_key,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    articles = []
    for article in data.get("articles", []):
        articles.append({
            "title": article.get("title", ""),
            "source": article.get("source", {}).get("name", ""),
            "publishedAt": article.get("publishedAt", ""),
            "content": article.get("content", ""),
            "urlToImage": article.get("urlToImage", ""),
            "url": article.get("url", ""),
            "description": article.get("description", "")
        })
    return articles
