
import pandas as pd
from datetime import datetime, timedelta
import os
from news_collector import NewsCollector
from sentiment_analyzer import SentimentAnalyzer


NEWSDATA_API_KEY = "pub_9d23f45a6e8b4e32b9a7c1234567890a1b2"
NEWSDATA_API_BASE_URL = "https://newsdata.io/api/1/" 



def main():
    collector = NewsCollector(api_key=NEWSDATA_API_KEY, base_url=NEWSDATA_API_BASE_URL)
    analyzer = SentimentAnalyzer()
    current_date = datetime(2025, 7, 20) 
    
    query_event = "Kochi metro expansion" 
    start_date_obj = current_date - timedelta(days=60)
    
    start_date_str = start_date_obj.strftime('%Y-%m-%d')
    end_date_str = current_date.strftime('%Y-%m-%d')

    print(f"--- Starting News Data Collection for '{query_event}' ({start_date_str} to {end_date_str}) ---")

    news_df = collector.fetch_articles(
        query=query_event,
        from_date=start_date_str,
        to_date=end_date_str,
        language="en",
        country="in", 
        page_limit=5, 
        max_articles=50 
    )

    if news_df.empty:
        print("No news data collected. Exiting.")
        return

    print(f"\n--- Collected {len(news_df)} articles ---")
    print(news_df[['date', 'title', 'source', 'category']].head())

    print("\n--- Performing Sentiment Analysis ---")
    news_df_with_sentiment = analyzer.add_sentiment_columns(news_df, text_column="description")

    print("\n--- Sample Articles with Sentiment ---")
    print(news_df_with_sentiment[['date', 'title', 'sentiment_polarity', 'sentiment_subjectivity']].head())

    print("\n--- Basic Daily Sentiment Trend ---")
    news_df_with_sentiment['date_only'] = news_df_with_sentiment['date'].dt.date
    daily_sentiment = news_df_with_sentiment.groupby('date_only')['sentiment_polarity'].mean().reset_index()
    print(daily_sentiment.sort_values('date_only').tail(7)) 

    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    
    output_filename = f"{query_event.replace(' ', '_').lower()}_news_sentiment.csv"
    output_path = os.path.join(output_dir, output_filename)
    news_df_with_sentiment.to_csv(output_path, index=False)
    print(f"\nProcessed data saved to {output_path}")

if __name__ == "__main__":
    main()
