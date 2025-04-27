# Real-Time News Sentiment Analysis App

A multipage Streamlit app for real-time news sentiment analytics. Fetches news, analyzes sentiment (using NLTK VADER), and provides interactive visualizations and data export tools.

## Features
- **Multipage navigation:** Dashboard, Sentiment Explorer, Live Feed, Trending Topics, Source Comparison, Download & Export, Settings & About
- **Sentiment analysis:** Real-time sentiment scoring of news articles
- **Visualizations:** Sentiment distribution, bar charts, word clouds, trending topics, source comparison, and more
- **Custom controls:** Set topic, date range, and number of articles (max 100)
- **Download/export:** Export analyzed data as CSV and save charts as images
- **Secure API key management:** Store your NewsAPI key in `.streamlit/secrets.toml`

## Project Structure
- `app.py`: Main landing/documentation page (start here)
- `/pages/`: All analytics and feature pages
- `utils/`: Helper modules for news fetching, sentiment analysis, and visualization
- `requirements.txt`: Python dependencies

## Setup & Usage
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Add your NewsAPI key:**
   - Create a file at `.streamlit/secrets.toml` with the following content:
     ```toml
     NEWS_API_KEY = "your_newsapi_key_here"
     ```
3. **Run the app:**
   ```bash
   streamlit run app.py
   ```
4. **Navigate using the sidebar** to access all features.

## Pages & Features
- **Dashboard:** Welcome, documentation, and navigation help
- **Sentiment Explorer:** Visualize sentiment distribution, top words, and top sources
- **Live Feed:** Latest news articles as cards, with sentiment and links
- **Trending Topics:** Top trending keywords and frequency over time
- **Source Comparison:** Compare sentiment and coverage between news sources
- **Download & Export:** Download analyzed data and export charts
- **Settings & About:** API key management, preferences, and credits

## Tech Stack
- Streamlit, NewsAPI.org, NLTK VADER, Plotly, pandas, matplotlib, wordcloud

---
**Developed by Shahmeer**

For feedback or contributions, see this README or open an issue.
