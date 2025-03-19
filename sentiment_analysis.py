from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK resources
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Company-specific sentiment modifiers
COMPANY_SENTIMENT = {
    # All companies now have zero bias
    'apple': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'microsoft': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'google': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'amazon': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'meta': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'facebook': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'tesla': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'nvidia': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'exxonmobil': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'exxon': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'shell': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'bp': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'boeing': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'twitter': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'x': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'disney': {'pos_boost': 0.0, 'neg_boost': 0.0},
    'netflix': {'pos_boost': 0.0, 'neg_boost': 0.0}
}

# Industry-specific keywords that indicate sentiment
INDUSTRY_KEYWORDS = {
    # Tech industry
    'innovation': 0.3,
    'breakthrough': 0.4,
    'revolutionary': 0.4,
    'cutting-edge': 0.3,
    'patent': 0.2,
    'lawsuit': -0.3,
    'security breach': -0.4,
    'data leak': -0.4,
    'privacy': -0.2,
    'antitrust': -0.3,
    'ai': 0.3,
    'artificial intelligence': 0.3,
    'machine learning': 0.3,
    
    # Oil and manufacturing
    'spill': -0.5,
    'pollution': -0.4,
    'emissions': -0.3,
    'climate': -0.2,
    'sustainable': 0.3,
    'renewable': 0.3,
    'crash': -0.5,
    'malfunction': -0.4,
    'recall': -0.4,
    'safety': -0.2,
    'green': 0.3,
    'clean energy': 0.4,
    
    # Financial terms
    'profit': 0.3,
    'growth': 0.3,
    'revenue': 0.2,
    'earnings': 0.2,
    'loss': -0.3,
    'debt': -0.3,
    'bankruptcy': -0.5,
    'downgrade': -0.4,
    'layoffs': -0.4,
    'restructuring': -0.2,
    'cost-cutting': -0.2,
    'dividend': 0.3,
    'investment': 0.2,
    'acquisition': 0.1,
    
    # General positive terms
    'success': 0.4,
    'successful': 0.4,
    'award': 0.3,
    'awarded': 0.3,
    'win': 0.3,
    'winning': 0.3,
    'exceed': 0.3,
    'exceeded': 0.3,
    'beat': 0.3,
    'positive': 0.3,
    'strong': 0.3,
    'strength': 0.3,
    'improve': 0.3,
    'improved': 0.3,
    'improvement': 0.3,
    
    # General negative terms
    'fail': -0.4,
    'failed': -0.4,
    'failure': -0.4,
    'issue': -0.3,
    'issues': -0.3,
    'problem': -0.3,
    'problems': -0.3,
    'concern': -0.3,
    'concerns': -0.3,
    'risk': -0.3,
    'risks': -0.3,
    'warning': -0.3,
    'decline': -0.3,
    'declined': -0.3,
    'drop': -0.3,
    'dropped': -0.3,
    'fall': -0.3,
    'fell': -0.3,
    'negative': -0.3,
    'weak': -0.3,
    'weakness': -0.3,
    'poor': -0.3,
    'worse': -0.4,
    'worst': -0.5,
    'scandal': -0.5,
    'controversy': -0.4,
    'controversial': -0.4,
    'investigation': -0.4,
    'probe': -0.4,
    'fine': -0.3,
    'penalty': -0.3,
    'sue': -0.4,
    'sued': -0.4,
    'lawsuit': -0.4
}

# Negation words that flip sentiment
NEGATION_WORDS = [
    'not', 'no', 'never', 'none', 'nobody', 'nothing', 'neither', 'nowhere', 
    'hardly', 'scarcely', 'barely', 'doesn\'t', 'isn\'t', 'wasn\'t', 'shouldn\'t',
    'wouldn\'t', 'couldn\'t', 'won\'t', 'can\'t', 'don\'t'
]

# Context modifiers - words that intensify or diminish sentiment
INTENSIFIERS = {
    'very': 1.5,
    'extremely': 2.0,
    'incredibly': 2.0,
    'really': 1.5,
    'particularly': 1.3,
    'especially': 1.3,
    'significantly': 1.5,
    'substantially': 1.5,
    'notably': 1.3,
    'highly': 1.5,
    'greatly': 1.5
}

DIMINISHERS = {
    'somewhat': 0.7,
    'slightly': 0.6,
    'a bit': 0.6,
    'a little': 0.6,
    'kind of': 0.7,
    'sort of': 0.7,
    'rather': 0.8,
    'barely': 0.5,
    'hardly': 0.5,
    'scarcely': 0.5,
    'marginally': 0.7
}

# Headline-specific terms (headlines often use stronger language)
HEADLINE_BOOST = {
    'soar': 0.3,
    'soars': 0.3,
    'surge': 0.3,
    'surges': 0.3,
    'jump': 0.2,
    'jumps': 0.2,
    'plunge': -0.3,
    'plunges': -0.3,
    'crash': -0.3,
    'crashes': -0.3,
    'tumble': -0.2,
    'tumbles': -0.2,
    'slump': -0.2,
    'slumps': -0.2
}

def check_for_negation(text, window_size=3):
    """Check if a sentiment word is negated within a window of words"""
    words = text.lower().split()
    negated_indices = set()
    
    for i, word in enumerate(words):
        if word in NEGATION_WORDS or word.endswith("n't"):
            # Mark the next few words as negated
            for j in range(i+1, min(i+window_size+1, len(words))):
                negated_indices.add(j)
    
    return negated_indices

def analyze_sentence_sentiment(sentence, company_name=None):
    """Analyze sentiment at the sentence level with negation handling"""
    sentence = sentence.lower()
    words = word_tokenize(sentence)
    negated_indices = check_for_negation(sentence)
    
    # VADER analysis
    sid = SentimentIntensityAnalyzer()
    vader_score = sid.polarity_scores(sentence)['compound']
    
    # TextBlob analysis
    blob_score = TextBlob(sentence).sentiment.polarity
    
    # Keyword analysis with negation handling
    keyword_score = 0
    keyword_count = 0
    
    for i, word in enumerate(words):
        # Check for industry keywords
        for keyword, score in INDUSTRY_KEYWORDS.items():
            if keyword in sentence:
                # Apply negation if needed
                if any(i in negated_indices for i in range(sentence.find(keyword), sentence.find(keyword) + len(keyword))):
                    keyword_score -= score  # Flip the sentiment
                else:
                    keyword_score += score
                keyword_count += 1
        
        # Check for intensifiers and diminishers
        if i < len(words) - 1:  # Make sure there's a next word
            next_word = words[i+1]
            if word in INTENSIFIERS and next_word in INDUSTRY_KEYWORDS:
                keyword_score *= INTENSIFIERS[word]
            elif word in DIMINISHERS and next_word in INDUSTRY_KEYWORDS:
                keyword_score *= DIMINISHERS[word]
    
    # Normalize keyword score
    if keyword_count > 0:
        keyword_score = keyword_score / keyword_count
    
    # Combine scores
    combined_score = (vader_score * 0.5) + (blob_score * 0.3) + (keyword_score * 0.2)
    return combined_score

def analyze_sentiment(text, company_name=None):
    """Main sentiment analysis function with advanced features"""
    if not text or text == "No summary available":
        return "Neutral"
    
    try:
        # Split into title and body if there's a period after the first sentence
        parts = text.split('. ', 1)
        title = parts[0]
        body = parts[1] if len(parts) > 1 else ""
        
        # Clean the text
        title = title.lower()
        body = body.lower()
        
        # Analyze title (headlines often have stronger sentiment)
        title_score = analyze_sentence_sentiment(title, company_name)
        
        # Check for headline-specific terms
        for term, boost in HEADLINE_BOOST.items():
            if term in title:
                title_score += boost
        
        # Analyze body by sentences
        body_scores = []
        if body:
            sentences = sent_tokenize(body)
            for sentence in sentences:
                body_scores.append(analyze_sentence_sentiment(sentence, company_name))
        
        # Calculate final score
        if body_scores:
            # Title gets more weight (40%) than individual body sentences
            body_avg = sum(body_scores) / len(body_scores)
            final_score = (title_score * 0.4) + (body_avg * 0.6)
        else:
            final_score = title_score
        
        # Determine sentiment based on final score with balanced thresholds
        if final_score >= 0.15:
            return "Positive"
        elif final_score <= -0.15:
            return "Negative"
        else:
            return "Neutral"
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "Neutral"
