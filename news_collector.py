import requests
import os
from datetime import datetime, timedelta
import pandas as pd
import time

class NewsCollector:
    def __init__(self, api_key: str, base_url: str = "https://newsdata.io/api/1/"):
        self.api_key = api_key
        self.base_url = base_url

    def _make_request(self, endpoint: str, params: dict) -> dict:
        params["apikey"] = self.api_key 
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=15) 
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 429:
                print("Rate limit hit. Please wait before making more requests.")
            return {}
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}. Check internet connection or base URL.")
            return {}
        except requests.exceptions.Timeout:
            print("Request timed out after 15 seconds.")
            return {}
        except requests.exceptions.RequestException as e:
            print(f"An unexpected error occurred: {e}")
            return {}

    def fetch_articles(
        self,
        query: str,
        from_date: str, 
        to_date: str,  
        language: str = "en",
        country: str = "in", 
        page_limit: int = 5,
        max_articles: int = 50 
    ) -> pd.DataFrame:
        all_articles = []
        next_page = None 
        endpoint = "archive" 
        page_counter = 0
        while page_counter < page_limit and len(all_articles) < max_articles:
            params = {
                "q": query,
                "language": language,
                "country": country,
                "from": from_date, 
                "to": to_date
            }
            if next_page:
                params["page"] = next_page
            data = self._make_request(endpoint, params)
            
            if not data or data.get("status") != "success":
                print(f"Failed to fetch data: {data.get('message', 'Unknown error')}")
                break

            articles_batch = data.get("results", []) 
            if not articles_batch:
                print("No more articles found in batch.")
                break
            
            all_articles.extend(articles_batch)
            total_results = data.get("totalResults", 0) 
            
            print(f"Fetched {len(all_articles)} articles for query '{query}' (page token: {next_page if next_page else 'initial'})")

            next_page = data.get("nextPage") 
            if not next_page:
                print("No more pages available.")
                break
            
            page_counter += 1
            time.sleep(6)
            
        if not all_articles:
            print(f"No articles found for query '{query}' in the specified date range.")
            return pd.DataFrame()

        df = pd.DataFrame(all_articles)
        required_columns = ["pubDate", "title", "description", "content", "link", "source_name", "category"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = None 

        df = df[required_columns]
        df.rename(columns={"pubDate": "date", "link": "url", "source_name": "source"}, inplace=True)
        df["date"] = pd.to_datetime(df["date"], errors='coerce') 
        df.dropna(subset=['date'], inplace=True)

        return df

if __name__ == "__main__":
    collector = NewsCollector(api_key="pub_9d23f45a6e8b4e32b9a7c1234567890a1b2")
    current_date = datetime(2025, 7, 20) 
    thirty_days_ago = current_date - timedelta(days=30)
    
    query = "Artificial Intelligence India"
    
    print(f"Fetching articles for '{query}' from {thirty_days_ago.strftime('%Y-%m-%d')} to {current_date.strftime('%Y-%m-%d')}")
    articles_df = collector.fetch_articles(
        query=query,
        from_date=thirty_days_ago.strftime('%Y-%m-%d'),
        to_date=current_date.strftime('%Y-%m-%d'),
        language="en",
        country="in", 
        page_limit=3, 
        max_articles=30 
    )

    if not articles_df.empty:
        print("\n--- Sample Fetched Articles ---")
        print(articles_df.head())
        print(f"\nTotal articles fetched: {len(articles_df)}")
        os.makedirs("data", exist_ok=True)
        articles_df.to_csv("data/raw_news_data.csv", index=False)
        print("Raw data saved to data/raw_news_data.csv")
    else:
        print("No articles fetched or DataFrame is empty. Check API key, query, or date range.")
