import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import plotly.graph_objects as go
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords', quiet=True)

def plot_sentiment_distribution(df: pd.DataFrame):
    import plotly.graph_objects as go
    sentiment_counts = df['sentiment'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=sentiment_counts.index, values=sentiment_counts.values, hole=0.3)])
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title="Sentiment Distribution")
    return fig

def plot_wordcloud(df: pd.DataFrame):
    text = " ".join(df['text_combined'])
    stop_words = set(stopwords.words('english')).union(STOPWORDS)
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stop_words).generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

def plot_top_words(df: pd.DataFrame, n=20):
    stop_words = set(stopwords.words('english')).union(STOPWORDS)
    unwanted_tokens = {'...', '|', '-', '—', 'chars]', '…', ',', '.', '–', '—', '‘', '’', '“', '”', '``', "''", '``', 'lenses', '26,', '2025', 'april'}
    words = pd.Series([
        w for w in " ".join(df['text_combined']).lower().split()
        if w not in stop_words and w not in unwanted_tokens and w.isalpha() and len(w) > 2
    ])
    top_words = words.value_counts().head(n)
    fig = go.Figure(go.Bar(x=top_words.values, y=top_words.index, orientation='h', marker_color='indigo'))
    fig.update_layout(
        yaxis=dict(autorange="reversed", tickfont=dict(size=14)),
        margin=dict(l=120, r=20, t=40, b=40),
        title="Top Words"
    )
    return fig

def plot_top_sources(df: pd.DataFrame, n=10):
    top_sources = df['source'].value_counts().head(n)
    fig = go.Figure(go.Bar(x=top_sources.values, y=top_sources.index, orientation='h', marker_color='teal'))
    fig.update_layout(
        yaxis=dict(autorange="reversed", tickfont=dict(size=14)),
        margin=dict(l=120, r=20, t=40, b=40),
        title="Top Sources"
    )
    return fig

def plot_source_comparison(df: pd.DataFrame, n=5):
    import plotly.express as px
    top_sources = df['source'].value_counts().head(n).index.tolist()
    filtered = df[df['source'].isin(top_sources)]
    source_sentiment = filtered.groupby(['source', 'sentiment']).size().reset_index(name='count')
    fig = px.bar(source_sentiment, x='source', y='count', color='sentiment', barmode='group', title='Sentiment by Source')
    fig.update_layout(margin=dict(l=60, r=20, t=40, b=40), yaxis_title='Article Count')
    return fig

def get_trending_topics(df: pd.DataFrame, n=10):
    from nltk.corpus import stopwords
    import string
    stop_words = set(stopwords.words('english'))
    unwanted_tokens = {'...', '|', '-', '—', 'chars]', '…', ',', '.', '–', '—', '‘', '’', '“', '”', '``', "''", '``'}
    words = [w.strip(string.punctuation).lower() for t in df['text_combined'] for w in t.split()]
    words = [w for w in words if w not in stop_words and w not in unwanted_tokens and len(w) > 3 and w.isalpha()]
    from collections import Counter
    return Counter(words).most_common(n)
