import streamlit as st

st.set_page_config(page_title="📰 News Sentiment Dashboard", layout="wide")
st.title("📰 Dashboard")

st.markdown("""
# 📰 Real-Time News Sentiment Analysis App

Welcome! This dashboard gives you deep, real-time insights into the latest news articles, their sentiment, trending topics, and more. Use the sidebar to navigate through powerful analytics features.

---

## 🚀 **How to Use This App**
1. **Enter a topic/keyword** in the sidebar (e.g., "Technology", "Bitcoin").
2. **Select the number of articles** and the desired date range.
3. **Click the action button** to fetch and analyze news in real time.
4. **Navigate pages** from the sidebar for different analytics views and tools.

---

## 🗂️ **App Pages & Features**

### 1. **Dashboard**
- This page! Quick intro and navigation help.

### 2. **Sentiment Explorer**
- Visualize sentiment distribution, top words, and top sources for your query.
- Great for a high-level overview.

### 3. **Live Feed**
- See the latest news articles as cards, with title, source, time, image, sentiment, and a direct link.
- Perfect for real-time monitoring.

### 4. **Trending Topics**
- List and visualize the top trending keywords in the news.
- See how topic frequency changes over time.
- Click a topic to view related articles and their sentiment.

### 5. **Source Comparison**
- Compare sentiment, volume, and coverage between news sources (e.g., CNN vs. BBC).
- Interactive source selection and visualizations (grouped bar, heatmap).

### 6. **Download & Export**
- Download the analyzed data as CSV.
- Preview your data and schema.
- Export any visualization as an image (right-click Plotly charts).

### 7. **Settings & About**
- View API key management instructions.
- Set preferences (auto-refresh interval, etc.).
- Learn more about the app, tech stack, and credits.

---

## 🛠️ **Tech Stack**
- [Streamlit](https://streamlit.io/) for UI
- [NewsAPI.org](https://newsapi.org/) for news
- [NLTK VADER](https://github.com/cjhutto/vaderSentiment) for sentiment
- [Plotly](https://plotly.com/python/) for interactive charts

---

## 💡 **Tips**
- Use the date range filter for historical or recent news.
- Try different topics for broader or niche insights.
- Explore trending topics to spot news cycles and emerging stories.
- Download your data for further analysis!

---

**Developed by Shahmeer**

For feedback or contributions, see the project [README](../README.md).
""")
