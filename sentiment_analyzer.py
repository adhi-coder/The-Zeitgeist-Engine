import pandas as pd
from textblob import TextBlob
import nltk
import re

try:
    nltk.data.find('corpora/wordnet')
except nltk.downloader.DownloadError:
    nltk.download('wordnet')
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except nltk.downloader.DownloadError:
    nltk.download('vader_lexicon')
class SentimentAnalyzer:
    def __init__(self):
        pass

    def _clean_text(self, text: str) -> str:
        if text is None:
            return ""
        text = str(text).lower() 
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'https?://\S+|www\.\S+', '', text) 
        text = re.sub(r'<.*?>+', '', text)
        text = re.sub(r'[%s]' % re.escape(r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'), '', text) 
        text = re.sub(r'\n', ' ', text) 
        text = re.sub(r'\s+', ' ', text).strip() 
        return text

    def analyze_sentiment(self, text: str) -> tuple[float, float]:
        """
        Analyzes the sentiment of a given text using TextBlob.
        Returns polarity (float from -1.0 to 1.0) and subjectivity (float from 0.0 to 1.0).
        """
        cleaned_text = self._clean_text(text)
        if not cleaned_text:
            return 0.0, 0.0

        analysis = TextBlob(cleaned_text)
        return analysis.sentiment.polarity, analysis.sentiment.subjectivity

    def add_sentiment_columns(self, df: pd.DataFrame, text_column: str = "content") -> pd.DataFrame:
        """
        Adds 'sentiment_polarity' and 'sentiment_subjectivity' columns to a DataFrame.
        """
        if text_column not in df.columns:
            print(f"Error: Text column '{text_column}' not found in DataFrame. Trying 'description' instead.")
            if "description" in df.columns:
                text_column = "description"
            else:
                print("No suitable text column found for sentiment analysis. Returning DataFrame as is.")
                return df

        print(f"Analyzing sentiment for column: '{text_column}'...")
        df[['sentiment_polarity', 'sentiment_subjectivity']] = df[text_column].apply(
            lambda x: pd.Series(self.analyze_sentiment(x))
        )
        print("Sentiment analysis complete.")
        return df

if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    data = {
        "content": [
            "This is a fantastic product, I absolutely love it!",
            "The service was terrible and I'm very disappointed.",
            "The event took place in the city center. It was okay.",
            None,
            "The weather forecast predicts rain, which is neither good nor bad."
        ],
        "description": [
            "Fantastic. Love it.",
            "Terrible. Disappointed.",
            "Event happened. Okay.",
            None,
            "Weather is neutral."
        ]
    }
    dummy_df = pd.DataFrame(data)

    print("--- Original DataFrame ---")
    print(dummy_df)

    dummy_df_with_sentiment = analyzer.add_sentiment_columns(dummy_df, text_column="content")

    print("\n--- DataFrame with Sentiment ---")
    print(dummy_df_with_sentiment)
