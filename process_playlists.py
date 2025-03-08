import pandas as pd
import re

# Load MPD dataset (replace with actual file path)
df = pd.read_json("mpd_sample.json")  # MPD is in JSON format

# Example mood keyword mapping
mood_keywords = {
    "happy": ["happy", "joy", "dance", "party", "fun"],
    "sad": ["sad", "cry", "heartbreak", "alone"],
    "chill": ["chill", "lofi", "relax", "study"],
    "energetic": ["workout", "power", "motivation", "hype"]
}

# Function to assign a mood based on playlist title
def classify_mood(title):
    title = title.lower()
    for mood, keywords in mood_keywords.items():
        if any(re.search(rf"\b{kw}\b", title) for kw in keywords):
            return mood
    return "neutral"  # Default if no mood match is found

# Apply NLP mood classification
df["mood"] = df["name"].apply(classify_mood)

# Check results
print(df[["name", "mood"]].head())
