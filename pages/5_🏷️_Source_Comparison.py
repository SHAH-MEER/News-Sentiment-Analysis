import streamlit as st
import pandas as pd
from utils.news_fetch import fetch_news
from utils.sentiment_analysis import analyze_sentiment
from utils.visualizations import plot_source_comparison
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Source Comparison", layout="wide")
st.title("🏷️ Source Comparison")

with st.expander('Controls', expanded=True):
    query = st.text_input("Enter Topic/Keyword:", "Technology")
    num_articles = st.slider("Number of Articles:", 10, 100, 50)
    end_date = datetime.now()
    default_start = end_date - timedelta(days=7)
    start_date = st.date_input("From Date", default_start)
    end_date = st.date_input("To Date", end_date)
    from_date_str = start_date.strftime('%Y-%m-%d')
    to_date_str = end_date.strftime('%Y-%m-%d')
    fetch = st.button('Compare Sources')

if 'fetch' in locals() and fetch:
    news_data = fetch_news(query, from_date=from_date_str, to_date=to_date_str, page_size=num_articles)
    if not news_data:
        st.warning("No articles found for this query.")
    else:
        df = pd.DataFrame(news_data)
        df['text_combined'] = df['title'] + " " + df['content'].fillna('')
        df['sentiment'] = df['text_combined'].apply(analyze_sentiment)
        st.subheader("Sentiment by Source (Grouped Bar)")
        st.plotly_chart(plot_source_comparison(df, n=8), use_container_width=True)
        st.subheader("Source Selection")
        sources = df['source'].unique().tolist()
        selected_sources = st.multiselect("Select sources to compare:", sources, default=sources[:2])
        if selected_sources:
            filtered = df[df['source'].isin(selected_sources)]
            source_sentiment = filtered.groupby(['source', 'sentiment']).size().reset_index(name='count')
            fig = px.bar(source_sentiment, x='source', y='count', color='sentiment', barmode='group', title='Sentiment by Selected Sources')
            st.plotly_chart(fig, use_container_width=True)
        st.subheader("Source Sentiment Heatmap")
        pivot = df.pivot_table(index='source', columns='sentiment', values='title', aggfunc='count', fill_value=0)
        fig2 = px.imshow(pivot, text_auto=True, aspect='auto', title='Source vs Sentiment Heatmap')
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Source Sentiment Comparison (Average Score)")
        sentiment_map = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
        df['sentiment_score'] = df['sentiment'].map(sentiment_map)
        avg_sentiment = df.groupby('source')['sentiment_score'].mean().reset_index()
        fig3 = px.bar(avg_sentiment, x='source', y='sentiment_score', title='Average Sentiment Score by Source', color='sentiment_score', color_continuous_scale='RdYlGn')
        fig3.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig3, use_container_width=True)
