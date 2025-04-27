import streamlit as st
import pandas as pd
from utils.news_fetch import fetch_news
from utils.sentiment_analysis import analyze_sentiment
from utils.visualizations import plot_sentiment_distribution, plot_top_words, plot_top_sources
from datetime import datetime, timedelta

st.set_page_config(page_title="Sentiment Explorer", layout="wide")
st.title("📊 Sentiment Explorer")

# Controls in main page
with st.expander('Controls', expanded=True):
    query = st.text_input("Enter Topic/Keyword:", "Technology")
    num_articles = st.slider("Number of Articles:", 10, 100, 50)
    end_date = datetime.now()
    default_start = end_date - timedelta(days=7)
    start_date = st.date_input("From Date", default_start)
    end_date = st.date_input("To Date", end_date)
    from_date_str = start_date.strftime('%Y-%m-%d')
    to_date_str = end_date.strftime('%Y-%m-%d')
    fetch = st.button('Fetch and Analyze')

if 'fetch' in locals() and fetch:
    news_data = fetch_news(query, from_date=from_date_str, to_date=to_date_str, page_size=num_articles)
    if not news_data:
        st.warning("No articles found for this query.")
    else:
        df = pd.DataFrame(news_data)
        df['text_combined'] = df['title'] + " " + df['content'].fillna('')
        df['sentiment'] = df['text_combined'].apply(analyze_sentiment)

        st.subheader("Sentiment Distribution")
        st.plotly_chart(plot_sentiment_distribution(df), use_container_width=True)

        # Sentiment Counts Bar Chart (like Live Feed)
        import plotly.express as px
        sentiment_counts = df['sentiment'].value_counts().reindex(['Positive', 'Neutral', 'Negative'], fill_value=0)
        fig_bar = px.bar(
            x=sentiment_counts.index,
            y=sentiment_counts.values,
            color=sentiment_counts.index,
            color_discrete_map={'Positive':'green','Neutral':'gray','Negative':'red'},
            labels={'x':'Sentiment', 'y':'Count'},
            title='Article Sentiment Counts'
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("Top Words in News Articles")
        st.plotly_chart(plot_top_words(df), use_container_width=True)

        st.subheader("Top News Sources")
        st.plotly_chart(plot_top_sources(df), use_container_width=True)

        st.subheader("Sentiment Change Over Time")
        df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
        df_time = df.dropna(subset=['publishedAt']).copy()
        df_time['hour'] = df_time['publishedAt'].dt.floor('h')
        sentiment_map = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
        df_time['sentiment_score'] = df_time['sentiment'].map(sentiment_map)
        time_group = df_time.groupby('hour')['sentiment_score'].mean().reset_index()
        import plotly.express as px
        fig_time = px.line(time_group, x='hour', y='sentiment_score', title='Average Sentiment Over Time')
        st.plotly_chart(fig_time, use_container_width=True)
