import requests
from sentiment_analysis import analyze_sentiment
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from bs4 import BeautifulSoup
from functools import lru_cache

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

API_KEY = "35f64a2bff0b439b8f29c739a4fbe3ce"  # Replace with your actual API Key

def extract_topics(text, num_topics=3):
    """Extract main topics from text"""
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    # Filter out stopwords and keep only words with length > 2
    filtered_tokens = [token for token in tokens if token.isalnum() and token not in stop_words and len(token) > 2]
    
    # Count word frequencies
    word_freq = Counter(filtered_tokens)
    
    # Get most common words as topics
    topics = [word.capitalize() for word, _ in word_freq.most_common(num_topics)]
    
    # If we don't have enough topics, add some default ones based on the company
    if len(topics) < num_topics:
        default_topics = ["Technology", "Business", "Innovation", "Market", "Investment", "Electric Vehicles", "Autonomous Driving"]
        for topic in default_topics:
            if topic not in topics:
                topics.append(topic)
            if len(topics) >= num_topics:
                break
    
    return topics[:num_topics]

def fetch_news(company_name):
    url = f"https://newsapi.org/v2/everything"
    params = {
        "q": company_name,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY,
        "pageSize": 20  # Increased to ensure we get 10 valid articles
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get("status") != "ok":
            # If API returns an error, use sample data
            return get_sample_articles(company_name)
        
        articles = []
        company_lower = company_name.lower()
        
        for article in data.get("articles", [])[:20]:
            title = article.get("title", "")
            summary = article.get("description", "No summary available")
            link = article.get("url", "")
            
            # Skip articles with empty titles or summaries
            if not title or not summary or summary == "No summary available":
                continue
            
            # Check if the article is actually about the company
            combined_text = f"{title.lower()} {summary.lower()}"
            if company_lower not in combined_text:
                # Skip articles that don't mention the company
                continue
                
            # Analyze full text for better sentiment accuracy
            full_text = f"{title}. {summary}"
            sentiment = analyze_sentiment(full_text, company_name)
            
            # Extract topics from title and summary
            topics = extract_topics(combined_text)
            
            articles.append({
                "title": title,
                "summary": summary,
                "link": link,
                "sentiment": sentiment,
                "topics": topics
            })
            
            # Stop after finding 10 relevant articles
            if len(articles) >= 10:
                break
        
        # If no valid articles were found, use sample data
        if not articles:
            return get_sample_articles(company_name)
            
        return articles
        
    except Exception as e:
        print(f"Error fetching news: {e}")
        # Return sample data if API fails
        return get_sample_articles(company_name)

def get_sample_articles(company_name):
    """Generate more realistic sample articles"""
    # Increase to 10 articles per company
    # Add more industry categories
    # Improve topic diversity
    
    # Create company-specific sample articles based on industry
    company_lower = company_name.lower()
    
    # Aerospace companies
    if any(name in company_lower for name in ['boeing', 'airbus', 'lockheed', 'northrop']):
        articles = [
            {
                "title": f"{company_name} Secures New Aircraft Order from Major Airline",
                "summary": f"{company_name} has announced a significant new order for commercial aircraft from a major international airline. The deal, valued at several billion dollars, includes both firm orders and options for additional aircraft.",
                "link": "https://example.com/article1",
                "sentiment": analyze_sentiment(f"{company_name} has announced a significant new order for commercial aircraft from a major international airline. The deal, valued at several billion dollars, includes both firm orders and options for additional aircraft.", company_name),
                "topics": ["Orders", "Airlines", "Commercial"]
            },
            {
                "title": f"{company_name} Addresses Manufacturing Quality Concerns",
                "summary": f"{company_name} executives have outlined steps being taken to address quality control issues in their manufacturing process following regulatory scrutiny. The company has implemented new inspection protocols and training programs.",
                "link": "https://example.com/article2",
                "sentiment": analyze_sentiment(f"{company_name} executives have outlined steps being taken to address quality control issues in their manufacturing process following regulatory scrutiny. The company has implemented new inspection protocols and training programs.", company_name),
                "topics": ["Manufacturing", "Quality", "Regulation"]
            },
            {
                "title": f"{company_name} Reports Quarterly Financial Results",
                "summary": f"{company_name} reported mixed financial results for the latest quarter. While revenue exceeded expectations due to strong defense sector performance, commercial aviation deliveries fell short of projections.",
                "link": "https://example.com/article3",
                "sentiment": analyze_sentiment(f"{company_name} reported mixed financial results for the latest quarter. While revenue exceeded expectations due to strong defense sector performance, commercial aviation deliveries fell short of projections.", company_name),
                "topics": ["Financial", "Defense", "Commercial"]
            },
            {
                "title": f"{company_name} Unveils New Aircraft Technology",
                "summary": f"{company_name} has revealed new fuel-efficient technology for its next generation of aircraft. The innovations are expected to reduce fuel consumption by up to 20% compared to current models, potentially giving the company a competitive advantage.",
                "link": "https://example.com/article4",
                "sentiment": analyze_sentiment(f"{company_name} has revealed new fuel-efficient technology for its next generation of aircraft. The innovations are expected to reduce fuel consumption by up to 20% compared to current models, potentially giving the company a competitive advantage.", company_name),
                "topics": ["Technology", "Innovation", "Efficiency"]
            },
            {
                "title": f"{company_name} Faces Delivery Delays for Key Programs",
                "summary": f"{company_name} has acknowledged delays in delivery schedules for several key aircraft programs. The company cited supply chain issues and technical challenges as the primary factors affecting production timelines.",
                "link": "https://example.com/article5",
                "sentiment": analyze_sentiment(f"{company_name} has acknowledged delays in delivery schedules for several key aircraft programs. The company cited supply chain issues and technical challenges as the primary factors affecting production timelines.", company_name),
                "topics": ["Delivery", "Production", "Supply Chain"]
            }
        ]
    
    # Tech companies
    elif any(name in company_lower for name in ['apple', 'microsoft', 'google', 'amazon', 'meta', 'facebook', 'tesla', 'nvidia']):
        articles = [
            {
                "title": f"{company_name} Launches New Product Line to Strong Consumer Response",
                "summary": f"{company_name} has introduced its latest product lineup at a special event, with pre-orders exceeding analyst expectations. The new devices feature significant performance improvements and several innovative features.",
                "link": "https://example.com/article1",
                "sentiment": analyze_sentiment(f"{company_name} has introduced its latest product lineup at a special event, with pre-orders exceeding analyst expectations. The new devices feature significant performance improvements and several innovative features.", company_name),
                "topics": ["Product", "Innovation", "Consumer"]
            },
            {
                "title": f"{company_name} Reports Record Quarterly Revenue",
                "summary": f"{company_name} announced record-breaking revenue for the latest quarter, driven by strong growth in its core business segments. The company also raised its full-year guidance, signaling confidence in continued momentum.",
                "link": "https://example.com/article2",
                "sentiment": analyze_sentiment(f"{company_name} announced record-breaking revenue for the latest quarter, driven by strong growth in its core business segments. The company also raised its full-year guidance, signaling confidence in continued momentum.", company_name),
                "topics": ["Financial", "Revenue", "Growth"]
            },
            {
                "title": f"{company_name} Faces Regulatory Scrutiny Over Market Practices",
                "summary": f"Regulators are investigating {company_name}'s business practices related to market competition. The inquiry focuses on whether the company has used its market position to disadvantage competitors in key business areas.",
                "link": "https://example.com/article3",
                "sentiment": analyze_sentiment(f"Regulators are investigating {company_name}'s business practices related to market competition. The inquiry focuses on whether the company has used its market position to disadvantage competitors in key business areas.", company_name),
                "topics": ["Regulation", "Competition", "Legal"]
            },
            {
                "title": f"{company_name} Expands AI Research Initiatives",
                "summary": f"{company_name} is significantly increasing its investment in artificial intelligence research, including opening a new dedicated AI lab and hiring top researchers from academia. The company views AI as central to its future product strategy.",
                "link": "https://example.com/article4",
                "sentiment": analyze_sentiment(f"{company_name} is significantly increasing its investment in artificial intelligence research, including opening a new dedicated AI lab and hiring top researchers from academia. The company views AI as central to its future product strategy.", company_name),
                "topics": ["AI", "Research", "Innovation"]
            },
            {
                "title": f"{company_name} Addresses Employee Concerns About Return-to-Office Policy",
                "summary": f"{company_name} executives have responded to internal pushback regarding the company's return-to-office mandate. While maintaining that in-person collaboration is essential, the company has introduced more flexible options for certain roles.",
                "link": "https://example.com/article5",
                "sentiment": analyze_sentiment(f"{company_name} executives have responded to internal pushback regarding the company's return-to-office mandate. While maintaining that in-person collaboration is essential, the company has introduced more flexible options for certain roles.", company_name),
                "topics": ["Workplace", "Policy", "Employees"]
            }
        ]
    
    # Oil and energy companies
    elif any(name in company_lower for name in ['exxon', 'chevron', 'shell', 'bp', 'total', 'conocophillips']):
        articles = [
            {
                "title": f"{company_name} Announces Major New Oil Discovery",
                "summary": f"{company_name} has confirmed a significant oil discovery in offshore exploration that could yield billions of barrels of recoverable oil. The company plans to begin development planning while conducting further assessment of the field's potential.",
                "link": "https://example.com/article1",
                "sentiment": analyze_sentiment(f"{company_name} has confirmed a significant oil discovery in offshore exploration that could yield billions of barrels of recoverable oil. The company plans to begin development planning while conducting further assessment of the field's potential.", company_name),
                "topics": ["Discovery", "Exploration", "Production"]
            },
            {
                "title": f"{company_name} Expands Renewable Energy Portfolio",
                "summary": f"{company_name} is increasing its investments in renewable energy with the acquisition of several solar and wind projects. The move is part of the company's strategy to diversify its energy portfolio and reduce its carbon footprint.",
                "link": "https://example.com/article2",
                "sentiment": analyze_sentiment(f"{company_name} is increasing its investments in renewable energy with the acquisition of several solar and wind projects. The move is part of the company's strategy to diversify its energy portfolio and reduce its carbon footprint.", company_name),
                "topics": ["Renewable", "Investment", "Strategy"]
            },
            {
                "title": f"{company_name} Faces Environmental Protests at Annual Meeting",
                "summary": f"Climate activists disrupted {company_name}'s annual shareholder meeting, demanding faster action on reducing emissions and transitioning away from fossil fuels. The company's CEO defended its current climate strategy while acknowledging the need for energy transition.",
                "link": "https://example.com/article3",
                "sentiment": analyze_sentiment(f"Climate activists disrupted {company_name}'s annual shareholder meeting, demanding faster action on reducing emissions and transitioning away from fossil fuels. The company's CEO defended its current climate strategy while acknowledging the need for energy transition.", company_name),
                "topics": ["Climate", "Activism", "Shareholders"]
            },
            {
                "title": f"{company_name} Reports Strong Quarterly Profits on Higher Oil Prices",
                "summary": f"{company_name} posted better-than-expected quarterly earnings, benefiting from higher global oil prices and increased production volumes. The company announced it would increase shareholder returns through dividends and share buybacks.",
                "link": "https://example.com/article4",
                "sentiment": analyze_sentiment(f"{company_name} posted better-than-expected quarterly earnings, benefiting from higher global oil prices and increased production volumes. The company announced it would increase shareholder returns through dividends and share buybacks.", company_name),
                "topics": ["Financial", "Earnings", "Oil Prices"]
            },
            {
                "title": f"{company_name} Invests in Carbon Capture Technology",
                "summary": f"{company_name} has announced a major investment in carbon capture and storage technology aimed at reducing emissions from its operations. The project represents one of the largest industrial carbon capture initiatives to date.",
                "link": "https://example.com/article5",
                "sentiment": analyze_sentiment(f"{company_name} has announced a major investment in carbon capture and storage technology aimed at reducing emissions from its operations. The project represents one of the largest industrial carbon capture initiatives to date.", company_name),
                "topics": ["Carbon Capture", "Technology", "Emissions"]
            }
        ]
    
    # Default articles for other companies
    else:
        articles = [
            {
                "title": f"{company_name} Reports Quarterly Earnings Above Expectations",
                "summary": f"{company_name} exceeded analyst expectations with strong revenue growth in the latest quarter. The company's performance was driven by increased market share and successful product launches, leading to a 15% increase in stock price.",
                "link": "https://example.com/article1",
                "sentiment": analyze_sentiment(f"{company_name} exceeded analyst expectations with strong revenue growth in the latest quarter. The company's performance was driven by increased market share and successful product launches, leading to a 15% increase in stock price.", company_name),
                "topics": ["Earnings", "Growth", "Financial"]
            },
            {
                "title": f"{company_name} Announces Strategic Restructuring Plan",
                "summary": f"{company_name} has unveiled a comprehensive restructuring initiative aimed at streamlining operations and reducing costs. The plan includes workforce adjustments and consolidation of certain business units to improve overall efficiency.",
                "link": "https://example.com/article2",
                "sentiment": analyze_sentiment(f"{company_name} has unveiled a comprehensive restructuring initiative aimed at streamlining operations and reducing costs. The plan includes workforce adjustments and consolidation of certain business units to improve overall efficiency.", company_name),
                "topics": ["Restructuring", "Strategy", "Operations"]
            },
            {
                "title": f"{company_name} Expands into New International Markets",
                "summary": f"{company_name} has announced plans to enter several new international markets as part of its global expansion strategy. The company will establish regional headquarters and distribution networks to support the growth initiative.",
                "link": "https://example.com/article3",
                "sentiment": analyze_sentiment(f"{company_name} has announced plans to enter several new international markets as part of its global expansion strategy. The company will establish regional headquarters and distribution networks to support the growth initiative.", company_name),
                "topics": ["Expansion", "International", "Strategy"]
            },
            {
                "title": f"{company_name} Faces Challenges in Competitive Market Environment",
                "summary": f"{company_name} is navigating an increasingly competitive market landscape as new entrants and changing consumer preferences impact its core business. Analysts have expressed concerns about the company's ability to maintain market share.",
                "link": "https://example.com/article4",
                "sentiment": analyze_sentiment(f"{company_name} is navigating an increasingly competitive market landscape as new entrants and changing consumer preferences impact its core business. Analysts have expressed concerns about the company's ability to maintain market share.", company_name),
                "topics": ["Competition", "Market", "Challenges"]
            },
            {
                "title": f"{company_name} Launches New Sustainability Initiative",
                "summary": f"{company_name} has introduced a comprehensive sustainability program with specific targets for reducing environmental impact across its operations. The initiative includes commitments to renewable energy, waste reduction, and sustainable sourcing.",
                "link": "https://example.com/article5",
                "sentiment": analyze_sentiment(f"{company_name} has introduced a comprehensive sustainability program with specific targets for reducing environmental impact across its operations. The initiative includes commitments to renewable energy, waste reduction, and sustainable sourcing.", company_name),
                "topics": ["Sustainability", "Environment", "Corporate Responsibility"]
            }
        ]
    
    return articles

def scrape_news_from_web(company_name):
    """Scrape news from non-JS websites"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    news_sources = [
        {
            'url': f'https://www.reuters.com/search/news?blob={company_name}',
            'title_selector': '.search-result-title',
            'summary_selector': '.search-result-summary'
        },
        {
            'url': f'https://finance.yahoo.com/quote/{company_name}/news',
            'title_selector': 'h3.Mb\\(5px\\)',
            'summary_selector': 'p.Fz\\(14px\\)'
        },
        {
            'url': f'https://www.marketwatch.com/search?q={company_name}&ts=0&tab=Articles',
            'title_selector': '.article__headline',
            'summary_selector': '.article__summary'
        }
    ]
    
    articles = []
    for source in news_sources:
        try:
            response = requests.get(source['url'], headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            titles = soup.select(source['title_selector'])
            summaries = soup.select(source['summary_selector'])
            
            for title, summary in zip(titles, summaries):
                if len(articles) >= 10:
                    break
                    
                articles.append({
                    'title': title.text.strip(),
                    'summary': summary.text.strip(),
                    'link': title.find('a')['href'] if title.find('a') else '',
                    'source': source['url']
                })
                
        except Exception as e:
            logger.error(f"Error scraping {source['url']}: {e}")
            continue
    
    return articles[:10]

@lru_cache(maxsize=100)
def fetch_cached_news(company_name):
    return fetch_news(company_name)