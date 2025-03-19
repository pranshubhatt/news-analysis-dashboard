import pytest
from news_scraper import fetch_news, extract_topics, scrape_news_from_web
from sentiment_analysis import analyze_sentiment
from text_to_speech import generate_tts, cleanup_audio_file
import os

def test_fetch_news():
    articles = fetch_news("Apple")
    assert len(articles) > 0
    assert all(isinstance(a, dict) for a in articles)

def test_sentiment_analysis():
    text = "Company reports excellent quarterly results"
    sentiment = analyze_sentiment(text)
    assert sentiment in ["Positive", "Negative", "Neutral"]

def test_audio_generation():
    text = "Test audio"
    audio_file = generate_tts(text)
    assert os.path.exists(audio_file)
    cleanup_audio_file(audio_file)
    assert not os.path.exists(audio_file)

def test_web_scraping():
    articles = scrape_news_from_web("Apple")
    assert len(articles) > 0
    assert all(isinstance(a, dict) for a in articles)
    assert all('title' in a and 'summary' in a for a in articles)

def test_topic_extraction():
    text = "Apple launches new iPhone with advanced AI capabilities"
    topics = extract_topics(text)
    assert len(topics) > 0
    assert all(isinstance(t, str) for t in topics)

def test_hindi_tts():
    text = "टेस्ला की खबरें"
    audio_file = generate_tts(text, "hi")
    assert os.path.exists(audio_file)
    cleanup_audio_file(audio_file)
    assert not os.path.exists(audio_file) 