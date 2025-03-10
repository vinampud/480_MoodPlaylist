import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from textblob import TextBlob

# Spotify credentials
SPOTIPY_CLIENT_ID = '5788ee2c162e49f18dfb1a782f299918'
SPOTIPY_CLIENT_SECRET = 'b29d2f0a542d4c778f36308f704b3162'

# Authentication
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)
weezer = sp.search(q='weezer', limit=2)
print(weezer['tracks'][0])
results = sp.recommendations(
    seed_genres=sp.recommendation_genre_seeds(),
    limit=15
)

print(results)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from textblob import TextBlob


def get_sentiment(text):
    """Determine sentiment of user input."""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "happy"
    elif polarity < 0:
        return "sad"
    else:
        return "neutral"

def get_spotify_recommendations(mood):
    """Fetch songs from Spotify based on mood using audio features."""
    
    mood_params = {
        "happy": {"valence": 0.8, "energy": 0.7, "danceability": 0.6},
        "sad": {"valence": 0.2, "energy": 0.3, "danceability": 0.3},
        "neutral": {"valence": 0.5, "energy": 0.5, "danceability": 0.5}
    }
    
    params = mood_params.get(mood, {"valence": 0.5, "energy": 0.5, "danceability": 0.5})  # Default to neutral
    
    # Map mood to genres
    mood_genres = {
        "happy": ["pop", "dance", "electronic"],
        "sad": ["classical", "acoustic", "folk"],
        "neutral": ["jazz", "blues", "hip_hop"]
    }
    
    seed_genres = mood_genres.get(mood, ["pop", "rock"])
    
    results = sp.recommendations(
        seed_genres=seed_genres,
        target_valence=params["valence"],
        target_energy=params["energy"],
        target_danceability=params["danceability"],
        limit=15
    )
    
    # Print recommended tracks
    print(f"🎶 Recommended songs for mood '{mood}':")
    for track in results["tracks"]:
        print(f"- {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")

if __name__ == "__main__":
    user_input = input("Enter your mood description: ")
    mood = get_sentiment(user_input)
    
    print(f"Detected Mood: {mood}")
    
    get_spotify_recommendations(mood)
