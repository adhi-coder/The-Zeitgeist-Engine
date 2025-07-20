# The Zeitgeist Engine: Historical News Sentiment & Event Impact

---

## Project Overview

**The Zeitgeist Engine** is a Python application that helps us understand the "mood of the times" – the *zeitgeist* – by analyzing **historical news sentiment**. It fetches news articles, figures out their emotional tone (positive, negative, neutral), and visually shows how public feeling shifts around major **events or trends**.

Think of it as a way to peek into the past and see how events impacted public perception. For example, it's currently set up to analyze news about "Kochi metro expansion" in India, giving us insights into local sentiment from the last couple of months (up to July 20, 2025).

---

## Key Features

* **Interactive Web Interface:** A user-friendly frontend built with Streamlit allows you to easily search for news topics and select date ranges.
* **News Data Collection:** Gathers relevant articles for your chosen topic from NewsData.io.
* **Sentiment Analysis:** Reads news descriptions and calculates their **polarity** (how positive/negative) and **subjectivity** (how objective/subjective).
* **Data Processing with Pandas:** Organizes all the collected news and sentiment scores into clean, easy-to-use tables.
* **Sentiment Trend Visualization:** Generates interactive line plots showing the average daily sentiment, helping you quickly spot emotional highs and lows.
* **Clean Code:** Structured into clear, separate modules (`news_collector.py`, `sentiment_analyzer.py`, `app.py`) for readability and easy future growth.

---

## How It Works 

1.  **Your Input:** You use the Streamlit web interface (`app.py`) to tell the engine what news topic you're interested in and for what dates.
2.  **Grabs News:** The `NewsCollector` module reaches out to the NewsData.io API, fetches the articles, and puts them into a raw data table.
3.  **Feels the News:** The `SentimentAnalyzer` module then takes these articles, uses `TextBlob` to read their descriptions, and assigns sentiment scores.
4.  **Shows & Saves:** `app.py` takes the analyzed data, creates the interactive sentiment trend chart, displays top articles, and saves all the processed data into a CSV file in the `data/` folder for you.

---
