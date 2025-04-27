import streamlit as st
import pandas as pd
from utils.news_fetch import fetch_news
from utils.sentiment_analysis import analyze_sentiment
from datetime import datetime, timedelta

st.set_page_config(page_title="Live Feed", layout="wide")
st.title("📰 Live Feed")

with st.expander('Controls', expanded=True):
    query = st.text_input("Enter Topic/Keyword:", "Technology")
    num_articles = st.slider("Number of Articles:", 10, 100, 50)
    end_date = datetime.now()
    default_start = end_date - timedelta(days=7)
    start_date = st.date_input("From Date", default_start)
    end_date = st.date_input("To Date", end_date)
    from_date_str = start_date.strftime('%Y-%m-%d')
    to_date_str = end_date.strftime('%Y-%m-%d')
    fetch = st.button('Fetch Live Feed')

if 'fetch' in locals() and fetch:
    news_data = fetch_news(query, from_date=from_date_str, to_date=to_date_str, page_size=num_articles)
    if not news_data:
        st.warning("No articles found for this query.")
    else:
        df = pd.DataFrame(news_data)
        df['text_combined'] = df['title'] + " " + df['content'].fillna('')
        df['sentiment'] = df['text_combined'].apply(analyze_sentiment)
        df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
        # Optionally compute compound score if not present
        from nltk.sentiment import SentimentIntensityAnalyzer
        sia = SentimentIntensityAnalyzer()
        df['compound'] = df['text_combined'].apply(lambda x: sia.polarity_scores(x)['compound'])
        df = df.sort_values('publishedAt', ascending=False)
        for _, row in df.iterrows():
            with st.container():
                st.markdown(f"### {row['title']}")
                meta = f"Source: {row['source']} | Published: {row['publishedAt'].strftime('%Y-%m-%d %H:%M') if pd.notnull(row['publishedAt']) else 'N/A'}"
                st.markdown(f"*{meta}*")
                # News image
                if 'urlToImage' in row and pd.notnull(row['urlToImage']):
                    st.image(row['urlToImage'], width=320)
                elif 'image' in row and pd.notnull(row['image']):
                    st.image(row['image'], width=320)
                else:
                    st.write('_No image available._')
                # Description
                desc = row['description'] if 'description' in row and pd.notnull(row['description']) else 'No description available.'
                st.write(desc)
                # Sentiment and score
                sentiment_color = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}.get(row['sentiment'], 'gray')
                st.markdown(f"**Sentiment:** <span style='color:{sentiment_color}'>{row['sentiment']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Compound Score:** {row['compound']:.3f}")
                # Read article button
                if 'url' in row and pd.notnull(row['url']):
                    st.markdown(f"[Read Article]({row['url']})", unsafe_allow_html=True)
                st.markdown('---')
