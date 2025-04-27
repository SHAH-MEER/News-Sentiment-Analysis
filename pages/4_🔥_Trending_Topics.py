import streamlit as st
import pandas as pd
from utils.news_fetch import fetch_news
from utils.sentiment_analysis import analyze_sentiment
from utils.visualizations import get_trending_topics
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Trending Topics", layout="wide")
st.title("🔥 Trending Topics")

# Sidebar controls
with st.expander('Controls', expanded=True):
    query = st.text_input("Enter Topic/Keyword:", "Technology")
    num_articles = st.slider("Number of Articles:", 10, 100, 50)
    end_date = datetime.now()
    default_start = end_date - timedelta(days=7)
    start_date = st.date_input("From Date", default_start)
    end_date = st.date_input("To Date", end_date)
    from_date_str = start_date.strftime('%Y-%m-%d')
    to_date_str = end_date.strftime('%Y-%m-%d')
    fetch = st.button('Fetch Trending Topics')

if 'fetch' in locals() and fetch:
    news_data = fetch_news(query, from_date=from_date_str, to_date=to_date_str, page_size=num_articles)
    if not news_data:
        st.warning("No articles found for this query.")
    else:
        df = pd.DataFrame(news_data)
        df['text_combined'] = df['title'] + " " + df['content'].fillna('')
        df['sentiment'] = df['text_combined'].apply(analyze_sentiment)

        st.subheader("Top Trending Topics (Keywords)")
        top_topics = get_trending_topics(df, n=15)
        topics, counts = zip(*top_topics) if top_topics else ([],[])
        fig = px.bar(x=counts, y=topics, orientation='h', title='Top Trending Topics', labels={'x':'Frequency','y':'Topic'})
        fig.update_layout(yaxis=dict(autorange="reversed"), margin=dict(l=120, r=20, t=40, b=40))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Topic Frequency Over Time")
        df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
        all_topics = []
        for idx, row in df.iterrows():
            for word in row['text_combined'].split():
                all_topics.append({'topic': word.lower(), 'publishedAt': row['publishedAt'], 'sentiment': row['sentiment'], 'title': row['title']})
        topics_df = pd.DataFrame(all_topics)
        if not topics_df.empty:
            topics_df = topics_df[topics_df['topic'].isin(topics)]
            time_group = topics_df.groupby([topics_df['publishedAt'].dt.date, 'topic']).size().reset_index(name='count')
            fig2 = px.line(time_group, x='publishedAt', y='count', color='topic', title='Topic Frequency Over Time')
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Explore Articles by Topic")
        selected_topic = st.selectbox("Select a topic to view related articles:", topics)
        if selected_topic:
            related = topics_df[topics_df['topic'] == selected_topic]
            for idx, row in related.iterrows():
                st.markdown(f"**{row['title']}**  ")
                st.write(f"Sentiment: {row['sentiment']}")
