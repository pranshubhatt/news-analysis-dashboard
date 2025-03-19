---
title: News Analysis Dashboard
emoji: 📰
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: 1.24.0
app_file: app.py
pinned: false
---

# News Analysis and Sentiment Dashboard

## Features
- Real-time news analysis from multiple sources
- Advanced sentiment analysis using multiple models
- Interactive visualizations and insights
- Hindi text-to-speech support
- RESTful API integration

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables:
   ```env
   NEWS_API_KEY=your_api_key
   ```
4. Run the application:
   ```bash
   uvicorn api:app --reload
   streamlit run app.py
   ```

## API Documentation
### Endpoints
- `POST /api/news`: Fetch news articles
- `POST /api/analyze`: Perform sentiment analysis
- `POST /api/tts`: Generate text-to-speech
- `GET /api/companies`: Get supported companies
- `GET /api/topics/{company_name}`: Get trending topics

## Models Used
- Sentiment Analysis: VADER + TextBlob
- Topic Extraction: NLTK
- Text-to-Speech: gTTS

## Limitations
- News API rate limits
- BeautifulSoup scraping limitations
- Processing time for large articles

## License
MIT License

## Deployment

### Local Deployment
```bash
# Run with Docker
docker build -t news-analysis .
docker run -p 8501:8501 news-analysis

# Run without Docker
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
streamlit run app.py
```

### Hugging Face Spaces Deployment
1. Create new Space on Hugging Face
2. Select Streamlit as the SDK
3. Upload all files
4. Add repository secrets:
   - NEWS_API_KEY 

## Testing
```bash
# Run tests
pytest test_news_analysis.py
```

## Docker Deployment
```bash
# Build the Docker image
docker build -t news-analysis .

# Run the container
docker run -p 8501:8501 -p 8000:8000 news-analysis
```

## Environment Variables
Create a `.env` file with the following:
- NEWS_API_KEY: Your News API key
- ENVIRONMENT: production/development
- LOG_LEVEL: INFO/DEBUG
- CACHE_TTL: Cache duration in seconds
- MAX_ARTICLES: Maximum articles to fetch

## Hugging Face Deployment
1. Create a new Space on Hugging Face
2. Select Streamlit as the SDK
3. Add your NEWS_API_KEY to Space secrets
4. Push your code using the provided GitHub Action 