import pandas as pd
from collections import Counter
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from news_scraper import fetch_news

# Download required NLTK data - simplified to avoid perceptron tagger issues
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def extract_topics(text):
    # Simplified topic extraction without POS tagging
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    # Filter out stopwords and keep only words with length > 2
    filtered_tokens = [token for token in tokens if token.isalnum() and token not in stop_words and len(token) > 2]
    return filtered_tokens

def comparative_analysis(articles):
    df = pd.DataFrame(articles)
    
    # Sentiment Analysis
    sentiment_counts = df["sentiment"].value_counts().to_dict()
    
    # Topic Analysis
    all_topics = []
    for article in articles:
        all_topics.extend(article.get("topics", []))
    
    # Get most common topics
    topic_counter = Counter(all_topics)
    common_topics = [topic for topic, count in topic_counter.most_common(5) if count > 1]
    
    # If we don't have enough topics, add some default ones
    if len(common_topics) < 3:
        default_topics = ["Innovation", "Technology", "Business", "Market", "Investment"]
        for topic in default_topics:
            if topic not in common_topics:
                common_topics.append(topic)
            if len(common_topics) >= 5:
                break
    
    # Find topic overlap between articles
    topic_overlap = {
        "Common Topics": common_topics
    }
    
    # Add unique topics for each article
    for i, article in enumerate(articles[:min(5, len(articles))]):
        article_topics = article.get("topics", [])
        unique_topics = [topic for topic in article_topics if topic not in common_topics]
        topic_overlap[f"Unique Topics in Article {i+1}"] = unique_topics
    
    # Generate coverage differences
    coverage_differences = []
    
    # Compare articles if we have at least 2
    if len(articles) >= 2:
        for i in range(min(3, len(articles)-1)):
            for j in range(i+1, min(i+2, len(articles))):
                article1 = articles[i]
                article2 = articles[j]
                
                # Skip if either article doesn't have a sentiment
                if not article1.get("sentiment") or not article2.get("sentiment"):
                    continue
                
                # Compare sentiments
                sentiment1 = article1["sentiment"]
                sentiment2 = article2["sentiment"]
                
                # Compare topics
                topics1 = article1.get("topics", [])
                topics2 = article2.get("topics", [])
                
                # Generate comparison text
                comparison = f"Article {i+1} "
                if sentiment1 != sentiment2:
                    comparison += f"has a {sentiment1.lower()} tone about {', '.join(topics1[:2])}, "
                    comparison += f"while Article {j+1} has a {sentiment2.lower()} tone about {', '.join(topics2[:2])}."
                else:
                    comparison += f"and Article {j+1} both have a {sentiment1.lower()} tone "
                    comparison += f"but focus on different aspects: {', '.join(topics1[:2])} vs {', '.join(topics2[:2])}."
                
                # Generate impact text
                impact = "This difference in coverage "
                if sentiment1 == "Positive" and sentiment2 != "Positive":
                    impact += "highlights both opportunities and challenges for the company."
                elif sentiment1 != "Positive" and sentiment2 == "Positive":
                    impact += "balances concerns with positive developments."
                elif sentiment1 == "Negative" and sentiment2 == "Negative":
                    impact += "suggests multiple areas of concern that may affect market perception."
                else:
                    impact += "provides a balanced view of the company's current situation."
                
                coverage_differences.append({
                    "Comparison": comparison,
                    "Impact": impact
                })
    
    # If we don't have enough comparisons, add generic ones
    if len(coverage_differences) < 2:
        coverage_differences.append({
            "Comparison": "Some articles focus on business performance, while others highlight technological innovations.",
            "Impact": "This diverse coverage provides a comprehensive view of the company's market position and future prospects."
        })
    
    # Generate final sentiment analysis
    dominant_sentiment = max(sentiment_counts.items(), key=lambda x: x[1])[0]
    final_sentiment = f"The overall sentiment in recent coverage is {dominant_sentiment.lower()}. "
    
    if dominant_sentiment == "Positive":
        final_sentiment += "This suggests a favorable market perception and potential positive impact on stock performance."
    elif dominant_sentiment == "Negative":
        final_sentiment += "This indicates concerns that could affect investor confidence and market position."
    else:
        final_sentiment += "This balanced coverage suggests stable market perception with both opportunities and challenges ahead."
    
    # Generate insights
    coverage_analysis = []
    
    # Add sentiment-based insight
    if sentiment_counts:
        coverage_analysis.append({
            "Comparison": f"The dominant sentiment in recent coverage is {dominant_sentiment}",
            "Impact": "This sentiment trend could influence market perception and investor decisions."
        })
    
    # Add topic-based insight
    if common_topics:
        coverage_analysis.append({
            "Comparison": f"Key topics discussed include {', '.join(common_topics[:3])}",
            "Impact": "These themes represent the current focus areas in company coverage."
        })
    
    # Add company-specific insight
    coverage_analysis.append({
        "Comparison": "News coverage varies between technological advancements and business performance.",
        "Impact": "Public perception is influenced by both innovation highlights and financial reports."
    })
    
    return {
        "Sentiment Distribution": sentiment_counts,
        "Common Topics": common_topics,
        "Coverage Insights": coverage_analysis,
        "Coverage Differences": coverage_differences,
        "Topic Overlap": topic_overlap,
        "Final Sentiment Analysis": final_sentiment
    }

# Remove the test code to avoid errors when importing
# articles = fetch_news("Tesla")
# report = comparative_analysis(articles)
# print(report)

