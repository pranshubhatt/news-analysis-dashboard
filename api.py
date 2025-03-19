from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from news_scraper import fetch_news
from sentiment_analysis import analyze_sentiment
from text_to_speech import generate_tts

app = FastAPI()

class Article(BaseModel):
    title: str
    summary: str
    link: str
    sentiment: str
    topics: List[str]

class CompanyRequest(BaseModel):
    name: str
    language: str = "en"

class AnalysisResponse(BaseModel):
    sentiment: str
    confidence: float
    topics: List[str]
    summary: str

@app.post("/api/news")
async def get_news(request: CompanyRequest):
    """Fetch news articles for a company"""
    try:
        articles = fetch_news(request.name)
        return {"status": "success", "data": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
async def analyze_articles(request: CompanyRequest):
    """Analyze sentiment of articles"""
    try:
        articles = fetch_news(request.name)
        analyzed_articles = []
        for article in articles:
            sentiment = analyze_sentiment(f"{article['title']}. {article['summary']}")
            article["sentiment"] = sentiment
            analyzed_articles.append(article)
        return {"status": "success", "data": analyzed_articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tts")
async def generate_audio(text: str, language: str = "en"):
    """Generate text-to-speech audio"""
    try:
        audio_file = generate_tts(text, language)
        return {"status": "success", "audio_file": audio_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/companies")
async def get_supported_companies():
    """Get list of supported companies"""
    return {
        "status": "success",
        "data": {
            "tech": ["Apple", "Microsoft", "Google"],
            "aerospace": ["Boeing", "Airbus"],
            "energy": ["ExxonMobil", "Shell", "BP"]
        }
    }

@app.get("/api/topics/{company_name}")
async def get_company_topics(company_name: str):
    """Get trending topics for a company"""
    try:
        articles = fetch_news(company_name)
        topics = {}
        for article in articles:
            for topic in article['topics']:
                topics[topic] = topics.get(topic, 0) + 1
        return {"status": "success", "data": topics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)