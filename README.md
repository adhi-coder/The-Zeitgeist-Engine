# The-Zeitgeist-Engine

Project Overview
The Zeitgeist Engine is a Python-powered application designed to uncover the "mood of the times" – the zeitgeist – by analyzing historical news sentiment. It fetches news articles, performs sentiment analysis (determining positive, negative, or neutral tones), and helps visualize how public sentiment shifts around major events or trends.

This interactive tool provides a unique lens into past public perception. For instance, it's currently configured to analyze news related to "Kochi metro expansion" in India, offering insights into local sentiment over a recent period.

Key Features
Interactive Web Interface: A user-friendly frontend built with Streamlit allows dynamic input of search queries and date ranges.
News Data Collection: Gathers relevant news articles for specific topics (like "Kochi metro expansion") and historical dates from NewsData.io.
Sentiment Analysis: Reads news article descriptions (or content) to determine their polarity (positive/negative/neutral tone) and subjectivity (objective/subjective tone).
Pandas Data Processing: Organizes all collected news and sentiment scores into clean, structured tables (DataFrames) for analysis.
Sentiment Trend Visualization: Generates interactive line plots of average daily sentiment, making it easy to spot emotional highs and lows over time.
Clean & Modular Code: Organized into distinct Python modules (news_collector.py, sentiment_analyzer.py, app.py) for clarity, maintainability, and future expansion.

How It Works (Behind the Scenes)
Frontend (Streamlit): app.py provides the web interface for users to input their search criteria.
Grabs News: The NewsCollector module (in news_collector.py) connects to the NewsData.io API, fetches articles based on the user's input, and structures the raw data.
Feels the News: The SentimentAnalyzer module (in sentiment_analyzer.py) uses TextBlob to process the text of the news articles, calculating polarity and subjectivity scores for each.
Processes & Visualizes: The app.py script then takes this processed data, generates the interactive sentiment trend plot, and displays key articles.
Saves Everything: All processed data, including sentiment scores, is saved to a CSV file in the data/ folder for persistent storage and deeper offline analysis.

