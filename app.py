import streamlit as st
import plotly.express as px
import pandas as pd
import os
from news_scraper import fetch_news
from comparative_analysis import comparative_analysis
from text_to_speech import generate_tts, cleanup_audio_file
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="News Analysis Dashboard", layout="wide")

# Add custom styling with improved topic badge visibility
st.markdown("""
    <style>
    .topic-badge {
        background-color: #4CAF50;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8em;
        margin-right: 5px;
        display: inline-block;
        font-weight: bold;
    }
    .common-topic {
        background-color: #4CAF50;
        color: white;
    }
    .unique-topic {
        background-color: #f44336;
        color: white;
    }
    .truncated-text {
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
    }
    </style>
""", unsafe_allow_html=True)

# Function to truncate text
def truncate_text(text, max_words=30):
    words = text.split()
    if len(words) <= max_words:
        return text, False
    return " ".join(words[:max_words]) + "...", True

st.title("🔍 News Summarization & Sentiment Analysis")

# Input section
col1, col2 = st.columns([3, 1])
with col1:
    company = st.text_input("Enter Company Name", placeholder="e.g., Tesla, Apple, Microsoft")
with col2:
    language = st.selectbox("Summary Audio Language", ["en", "hi"], index=0)

def validate_input(company_name: str) -> bool:
    """Validate user input"""
    if not company_name:
        return False
    if len(company_name) < 2:
        return False
    if not company_name.replace(" ", "").isalnum():
        return False
    return True

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_cached_news(company_name):
    return fetch_news(company_name)

def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logger.error(f"Error in {func.__name__}: {str(e)}")
    return wrapper

@handle_error
def analyze_company(company_name, language):
    """Analyze company news and generate results"""
    try:
        articles = fetch_cached_news(company_name)
        if not articles:
            return None
        
        # Perform analysis
        analysis_results = comparative_analysis(articles)
        
        # Get dominant sentiment first
        dominant_sentiment = max(analysis_results['Sentiment Distribution'].items(), key=lambda x: x[1])[0]
        
        # Generate summary based on language
        if language == "en":
            summary = f"Analysis summary for {company_name}. "
            summary += f"Based on {len(articles)} articles analyzed, "
            summary += f"the overall sentiment is {dominant_sentiment}. "
            summary += f"Key topics include {', '.join(analysis_results['Common Topics'][:3])}. "
            
            if "Final Sentiment Analysis" in analysis_results:
                summary += analysis_results["Final Sentiment Analysis"]
        else:
            # Hindi summary
            sentiment_in_hindi = {
                "Positive": "सकारात्मक",
                "Negative": "नकारात्मक",
                "Neutral": "तटस्थ"
            }.get(dominant_sentiment, "तटस्थ")
            
            summary = f"{company_name} की समाचार विश्लेषण। "
            summary += f"कुल {len(articles)} लेखों का विश्लेषण किया गया। "
            summary += f"समग्र भावना {sentiment_in_hindi} है। "
            
            # Convert topics to Hindi if possible, otherwise use English
            topics_str = ', '.join(analysis_results['Common Topics'][:2])
            summary += f"प्रमुख विषयों में {topics_str} शामिल हैं। "
            
            if "Final Sentiment Analysis" in analysis_results:
                if dominant_sentiment == "Positive":
                    summary += "यह कंपनी के लिए अनुकूल बाजार धारणा को दर्शाता है।"
                elif dominant_sentiment == "Negative":
                    summary += "यह निवेशक विश्वास पर प्रभाव डाल सकता है।"
                else:
                    summary += "यह स्थिर बाजार धारणा को दर्शाता है।"
        
        return {
            'articles': articles,
            'analysis': analysis_results,
            'summary': summary
        }
    except Exception as e:
        logger.error(f"Error in analyze_company: {str(e)}")
        raise

if st.button("Analyze"):
    if company:
        with st.spinner("Analyzing news articles..."):
            results = analyze_company(company, language)
            if results:
                articles = results['articles']
                analysis_results = results['analysis']
                summary = results['summary']
                
                # Create tabs for better organization
                tab1, tab2, tab3 = st.tabs(["📰 News Articles", "📊 Analysis Dashboard", "🎵 Audio Summary"])
                
                with tab1:
                    # Display articles using native Streamlit components
                    for i, article in enumerate(articles):
                        with st.expander(f"**{article['title']}**", expanded=True):
                            # Truncate summary text
                            truncated_summary, is_truncated = truncate_text(article['summary'])
                            
                            # Display truncated summary
                            st.write(truncated_summary)
                            
                            # Add "Read More" button if truncated
                            if is_truncated:
                                if st.button(f"Read Full Summary", key=f"read_more_{i}"):
                                    st.write(article['summary'])
                            
                            # Display topics with improved badges
                            if "topics" in article and article["topics"]:
                                st.write("**Topics:**")
                                # Use a container instead of columns for better display
                                topic_html = ""
                                for topic in article["topics"]:
                                    topic_html += f'<span class="topic-badge">{topic}</span> '
                                st.markdown(topic_html, unsafe_allow_html=True)
                            
                            # Display sentiment with appropriate color
                            if article['sentiment'] == "Positive":
                                st.success(f"Sentiment: {article['sentiment']}")
                            elif article['sentiment'] == "Negative":
                                st.error(f"Sentiment: {article['sentiment']}")
                            else:
                                st.info(f"Sentiment: {article['sentiment']}")
                            
                            st.markdown(f"[Read Full Article]({article['link']})")
                        
                        # Add a small space between articles
                        st.write("")
                
                with tab2:
                    # Get analysis results
                    analysis_results = analysis_results
                    
                    # Create visualizations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Sentiment Distribution Pie Chart
                        sentiment_data = pd.DataFrame.from_dict(
                            analysis_results["Sentiment Distribution"], 
                            orient='index'
                        ).reset_index()
                        sentiment_data.columns = ['Sentiment', 'Count']
                        
                        # Use bar chart if more than 3 sentiment categories
                        if len(sentiment_data) > 3:
                            fig1 = px.bar(
                                sentiment_data,
                                x='Sentiment',
                                y='Count',
                                title='Sentiment Distribution',
                                color='Sentiment',
                                color_discrete_sequence=px.colors.qualitative.Set3
                            )
                        else:
                            fig1 = px.pie(
                                sentiment_data, 
                                values='Count', 
                                names='Sentiment',
                                title='Sentiment Distribution',
                                color_discrete_sequence=px.colors.qualitative.Set3
                            )
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        # Topics Bar Chart
                        topics = analysis_results["Common Topics"]
                        topic_data = pd.DataFrame({
                            'Topic': topics,
                            'Count': [1] * len(topics)  # Assign count of 1 to each topic
                        })
                        
                        fig2 = px.bar(
                            topic_data,
                            x='Topic',
                            y='Count',
                            title='Common Topics',
                            labels={'Count': 'Frequency'}
                        )
                        # Customize the layout to ensure topic names are visible
                        fig2.update_layout(
                            xaxis_title="Topic",
                            yaxis_title="Frequency",
                            xaxis={'categoryorder':'total descending'}
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    # Add Word Cloud for topics in a more compact way
                    st.subheader("📊 Topic Word Cloud")
                    
                    # Create word frequency dictionary for word cloud
                    word_freq = {}
                    for topic in topics:
                        word_freq[topic] = 10  # Give equal weight to all topics
                    
                    # Generate word cloud
                    if word_freq:
                        try:
                            # Create two columns to make the word cloud more compact
                            wc_col1, wc_col2 = st.columns([1, 1])
                            
                            with wc_col1:
                                # Create a more compact word cloud
                                wc = WordCloud(width=500, height=300, background_color='black', 
                                              colormap='viridis', max_words=100, 
                                              prefer_horizontal=1.0)
                                wc.generate_from_frequencies(word_freq)
                                
                                # Display word cloud with smaller figure size
                                fig, ax = plt.subplots(figsize=(6, 3))
                                ax.imshow(wc, interpolation='bilinear')
                                ax.axis('off')
                                st.pyplot(fig)
                        except Exception as e:
                            st.warning(f"Could not generate word cloud: {e}")
                    
                    # Display insights
                    st.subheader("📈 Coverage Insights")
                    for insight in analysis_results["Coverage Insights"]:
                        st.info(
                            f"**Comparison:** {insight['Comparison']}\n\n"
                            f"**Impact:** {insight['Impact']}"
                        )
                    
                    # Display Coverage Differences
                    if "Coverage Differences" in analysis_results:
                        st.subheader("📊 Coverage Differences")
                        for diff in analysis_results["Coverage Differences"]:
                            st.warning(
                                f"**Comparison:** {diff['Comparison']}\n\n"
                                f"**Impact:** {diff['Impact']}"
                            )
                    
                    # Display Topic Overlap
                    if "Topic Overlap" in analysis_results:
                        st.subheader("🔄 Topic Overlap Analysis")
                        
                        # Display common topics with improved visibility
                        if "Common Topics" in analysis_results["Topic Overlap"]:
                            st.write("**Common Topics Across Articles:**")
                            common_topics = analysis_results["Topic Overlap"]["Common Topics"]
                            if common_topics:
                                topic_html = ""
                                for topic in common_topics:
                                    topic_html += f'<span class="topic-badge common-topic">{topic}</span> '
                                st.markdown(topic_html, unsafe_allow_html=True)
                            else:
                                st.write("No common topics found.")
                        
                        # Display unique topics for each article with improved visibility
                        for key, topics in analysis_results["Topic Overlap"].items():
                            if key.startswith("Unique Topics") and topics:
                                st.write(f"**{key}:**")
                                topic_html = ""
                                for topic in topics:
                                    topic_html += f'<span class="topic-badge unique-topic">{topic}</span> '
                                st.markdown(topic_html, unsafe_allow_html=True)
                    
                    # Display Final Sentiment Analysis
                    if "Final Sentiment Analysis" in analysis_results:
                        st.subheader("📝 Final Sentiment Analysis")
                        st.success(analysis_results["Final Sentiment Analysis"])
                
                with tab3:
                    st.write("### Audio Summary")
                    st.write(summary)
                    
                    # Generate audio with error handling
                    try:
                        audio_file = generate_tts(summary, language)
                        if os.path.exists(audio_file):
                            st.audio(audio_file)
                            # Clean up after displaying
                            cleanup_audio_file(audio_file)
                        else:
                            st.error("Audio file could not be generated. Please try again.")
                    except Exception as e:
                        st.error(f"Error generating audio: {e}")
            else:
                st.error("No results found for the given company.")
    else:
        st.warning("Please enter a company name to analyze")
