from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon', quiet=True)

def analyze_sentiment(text: str) -> str:
    """
    Analyze sentiment of a text using VADER.
    Returns: 'Positive', 'Negative', or 'Neutral'.
    """
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(text)
    compound = score['compound']
    if compound >= 0.05:
        return 'Positive'
    elif compound <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'
