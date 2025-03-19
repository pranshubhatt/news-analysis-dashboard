# News Analysis Dashboard - Technical Documentation

## Table of Contents
1. Project Overview
2. Features & Functionality
3. Technical Architecture
4. Implementation Details
5. API Documentation
6. Testing
7. Deployment Guide
8. Usage Guide
9. Limitations & Future Improvements

## 1. Project Overview

### Description
The News Analysis Dashboard is a web-based application that provides real-time news analysis and sentiment tracking for companies. It combines news aggregation, sentiment analysis, and text-to-speech capabilities to deliver comprehensive insights about company-related news.

### Key Features
- Real-time news fetching from multiple sources
- Advanced sentiment analysis using multiple models
- Comparative news analysis
- Bilingual support (English and Hindi)
- Interactive visualizations
- Text-to-speech capabilities
- RESTful API integration

## 2. Features & Functionality

### 2.1 News Aggregation
- Fetches news from NewsAPI
- Web scraping from Reuters, Yahoo Finance, and MarketWatch
- Industry-specific article categorization
- Automatic topic extraction
- Caching mechanism for improved performance

### 2.2 Sentiment Analysis
- Multi-model approach combining:
  - VADER sentiment analysis
  - TextBlob analysis
  - Industry-specific keyword analysis
- Context-aware analysis considering:
  - Negations
  - Intensifiers and diminishers
  - Industry-specific terminology
  - Headline-specific terms

### 2.3 Visualization & Analytics
- Sentiment distribution charts
- Topic frequency analysis
- Word cloud visualization
- Comparative analysis insights
- Coverage difference analysis

### 2.4 Text-to-Speech
- Supports English and Hindi
- Temporary file management
- Automatic cleanup
- Error handling

## 3. Technical Architecture

### 3.1 Components
- Frontend: Streamlit
- Backend: FastAPI
- Database: In-memory caching
- External APIs: NewsAPI
- Libraries: NLTK, TextBlob, gTTS

### 3.2 File Structure
```
news-analysis/
├── app.py                   # Streamlit frontend
├── api.py                   # FastAPI backend
├── news_scraper.py         # News fetching logic
├── sentiment_analysis.py    # Sentiment analysis
├── comparative_analysis.py  # Analysis functions
├── text_to_speech.py       # TTS functionality
├── utils.py                # Utility functions
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## 4. Implementation Details

### 4.1 News Scraping
```python
def fetch_news(company_name):
    """
    Fetches news articles using NewsAPI and web scraping
    - Uses NewsAPI for primary source
    - Falls back to web scraping if needed
    - Implements caching for performance
    - Filters relevant articles
    - Extracts topics and sentiment
    """

def scrape_news_from_web(company_name):
    """
    Scrapes news from:
    - Reuters
    - Yahoo Finance
    - MarketWatch
    Uses BeautifulSoup4 for parsing
    """
```

### 4.2 Sentiment Analysis Pipeline
```python
def analyze_sentiment(text, company_name):
    """
    Multi-level sentiment analysis:
    1. Text Preprocessing
       - Sentence splitting
       - Tokenization
       - Case normalization
    
    2. Analysis Methods
       - VADER scoring
       - TextBlob polarity
       - Keyword analysis
    
    3. Context Handling
       - Negation detection
       - Intensity modification
       - Industry context
    """
```

## 5. API Documentation

### 5.1 Endpoints

#### GET /api/companies
Returns supported companies list
```json
{
  "status": "success",
  "data": {
    "tech": ["Apple", "Microsoft", "Google"],
    "aerospace": ["Boeing", "Airbus"],
    "energy": ["ExxonMobil", "Shell", "BP"]
  }
}
```

#### POST /api/news
Fetches news articles for a company
```json
Request:
{
  "name": "company_name",
  "language": "en"
}

Response:
{
  "status": "success",
  "data": [
    {
      "title": "Article Title",
      "summary": "Article Summary",
      "sentiment": "Positive",
      "topics": ["Technology", "Innovation"]
    }
  ]
}
```

#### POST /api/analyze
Performs sentiment analysis
```json
Request:
{
  "name": "company_name",
  "language": "en"
}

Response:
{
  "status": "success",
  "data": {
    "sentiment": "Positive",
    "confidence": 0.85,
    "topics": ["Technology", "Innovation"],
    "summary": "Analysis summary text"
  }
}
```

## 6. Testing

### 6.1 Test Coverage
```python
# test_news_analysis.py
def test_fetch_news():
    """Tests news fetching functionality"""

def test_sentiment_analysis():
    """Tests sentiment analysis accuracy"""

def test_audio_generation():
    """Tests TTS generation and cleanup"""

def test_web_scraping():
    """Tests web scraping functionality"""
```

### 6.2 Running Tests
```bash
pytest test_news_analysis.py
```

## 7. Deployment Guide

### 7.1 Local Deployment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export NEWS_API_KEY=your_api_key

# Run application
streamlit run app.py
```

### 7.2 Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
EXPOSE 8000
CMD ["sh", "-c", "streamlit run app.py & uvicorn api:app --host 0.0.0.0 --port 8000"]
```

### 7.3 Hugging Face Deployment
1. Create new Space
2. Select Streamlit SDK
3. Configure environment variables:
   - NEWS_API_KEY
4. Upload project files
5. Select CPU basic hardware

## 8. Usage Guide

### 8.1 Basic Usage
1. Enter company name in the input field
2. Select language preference (English/Hindi)
3. Click "Analyze" button
4. View results in three tabs:
   - News Articles: Shows fetched articles with sentiment
   - Analysis Dashboard: Displays visualizations
   - Audio Summary: Provides TTS output

### 8.2 Advanced Features
- Topic filtering
- Sentiment comparison
- Audio generation in multiple languages
- Detailed analytics with visualizations

## 9. Limitations & Future Improvements

### 9.1 Current Limitations
- NewsAPI rate limits (100 requests/day)
- Web scraping restrictions on some websites
- Processing time for large articles
- Audio file temporary storage
- Limited language support

### 9.2 Future Improvements
- Additional news sources integration
- Enhanced sentiment analysis with deep learning
- Real-time updates and notifications
- Persistent storage for historical analysis
- User customization options
- Support for more languages
- Advanced visualization options