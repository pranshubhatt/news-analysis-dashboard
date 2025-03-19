from gtts import gTTS
from textblob import TextBlob
import os
import time
import tempfile

def generate_tts(text, language="en"):
    """
    Generate text-to-speech audio file with automatic cleanup
    
    Args:
        text (str): Text to convert to speech
        language (str): Language code (default: 'en')
        
    Returns:
        str: Path to the generated audio file
    """
    if not text:
        raise ValueError("Text cannot be empty")
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            audio_path = temp_file.name
            
        # Generate audio
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(audio_path)
        
        return audio_path
            
    except Exception as e:
        print(f"Error generating text-to-speech: {e}")
        raise

def cleanup_audio_file(file_path):
    """Clean up audio file after use"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error cleaning up audio file: {e}")

def analyze_sentiment(text):
    if not text or text == "No summary available":
        return {"label": "Neutral", "score": 0.0}
    
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity
    
    # Determine sentiment label
    if polarity > 0.3:
        label = "Very Positive"
    elif polarity > 0:
        label = "Slightly Positive"
    elif polarity < -0.3:
        label = "Very Negative"
    elif polarity < 0:
        label = "Slightly Negative"
    else:
        label = "Neutral"
    
    return {
        "label": label,
        "score": polarity,
        "subjectivity": subjectivity
    }

summary_text = "टेस्ला की खबरों में सकारात्मक और नकारात्मक दोनों पहलू हैं।"
generate_tts(summary_text)
