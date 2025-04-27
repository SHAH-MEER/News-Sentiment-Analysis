import streamlit as st

st.set_page_config(page_title="Settings & About", layout="wide")
st.title("⚙️ Settings & About")

st.header("API Key Management")
st.markdown("""
- The NewsAPI key is securely stored in `.streamlit/secrets.toml`.
- To update your API key, edit the secrets file and restart the app.
""")

st.header("Preferences")
st.markdown("""
- Set your preferred auto-refresh interval in the sidebar on each page.
- All user preferences are stored locally.
""")

st.header("About This App")
st.markdown("""
**Real-Time News Sentiment Analysis App**

- Built with [Streamlit](https://streamlit.io/)
- News fetched from [NewsAPI.org](https://newsapi.org/)
- Sentiment analysis powered by [NLTK VADER](https://github.com/cjhutto/vaderSentiment)
- Visualizations with [Plotly](https://plotly.com/python/)

**Developed by:** Shahmeer

**Usage:**
- Enter a topic/keyword, select article count and date range, and analyze news sentiment in real time!
- Explore trending topics, compare sources, and download your data.
""")
