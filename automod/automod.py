import time
import spacy
from afinn import Afinn
from better_profanity import profanity

# Load spaCy (lightweight)
nlp = spacy.blank("en")

# Load Afinn sentiment analyzer
afinn = Afinn()

# List of extreme words
extreme_words = {"kill", "murder", "bomb", "shoot", "die", "threaten",
                 "racist", "terrorist", "nazi", "genocide", "lynch"}

def analyze_message(text):
    start_time = time.perf_counter()  # Start timer

    # Step 1: Tokenize and preprocess using spaCy
    doc = nlp(text)
    cleaned_text = " ".join([token.text.lower() for token in doc])  # Convert to lowercase

    # Step 2: Check for extreme content
    if any(word in cleaned_text for word in extreme_words):
        return "Fail (Extreme Content Detected)"

    # Step 3: Count profanity words (ALLOW some profanity)
    profane_words = [word for word in cleaned_text.split() if profanity.contains_profanity(word)]
    if len(profane_words) > 3:  # Allow light profanity but block excessive use
        return "Fail (Excessive Profanity Detected)"

    # Step 4: Sentiment analysis with Afinn
    sentiment_score = afinn.score(cleaned_text)

    # Step 5: Classify sentiment
    if sentiment_score < -8:
        return "Fail (Highly Negative Sentiment)"

    end_time = time.perf_counter()  # End timer
    execution_time = end_time - start_time  # Calculate time
    return f"Pass (Execution Time: {execution_time:.6f} seconds)"

# Test the speed
test_text = "This is a f***ing terrible idea, I'm gonna shoot someone!"
print(analyze_message(test_text))
