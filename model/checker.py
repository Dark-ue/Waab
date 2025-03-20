from transformers import pipeline
from profanity_check import predict

class AIModeration:
    def __init__(self):
        """Initialize AI models"""
        self.sentiment_model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

    def detect_profanity(self, text: str) -> bool:
        """Checks if a message contains profanity."""
        return bool(predict([text])[0])  # True if profanity detected

    def analyze_text(self, text: str) -> dict:
        """Analyzes text for sentiment and profanity."""
        sentiment = self.sentiment_model(text)[0]["label"]
        profanity = self.detect_profanity(text)

        return {
            "text": text,
            "sentiment": sentiment,
            "profanity": profanity
        }