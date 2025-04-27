import streamlit as st
import pandas as pd
from utils.news_fetch import fetch_news
from utils.sentiment_analysis import analyze_sentiment
from datetime import datetime, timedelta

st.set_page_config(page_title="Download & Export", layout="wide")
st.title("⬇️ Download & Export")

with st.expander('Controls', expanded=True):
    query = st.text_input("Enter Topic/Keyword:", "Technology")
    num_articles = st.slider("Number of Articles:", 10, 100, 50)
    end_date = datetime.now()
    default_start = end_date - timedelta(days=7)
    start_date = st.date_input("From Date", default_start)
    end_date = st.date_input("To Date", end_date)
    from_date_str = start_date.strftime('%Y-%m-%d')
    to_date_str = end_date.strftime('%Y-%m-%d')
    fetch = st.button('Fetch Data')

if 'fetch' in locals() and fetch:
    news_data = fetch_news(query, from_date=from_date_str, to_date=to_date_str, page_size=num_articles)
    if not news_data:
        st.warning("No articles found for this query.")
    else:
        df = pd.DataFrame(news_data)
        df['text_combined'] = df['title'] + " " + df['content'].fillna('')
        df['sentiment'] = df['text_combined'].apply(analyze_sentiment)
        st.subheader("Download CSV")
        st.download_button("Download CSV", data=df.to_csv(index=False), file_name='news_sentiment.csv', mime='text/csv')
        st.subheader("Data Preview")
        st.dataframe(df.head(50))
        st.subheader("Data Schema")
        st.json({col: str(dtype) for col, dtype in df.dtypes.items()})
        st.subheader("Export Visualizations")
        st.info("Right-click any Plotly chart in the app to save as PNG/SVG!")
