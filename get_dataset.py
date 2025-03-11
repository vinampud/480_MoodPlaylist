import spotipy
from spotipy.oauth2 import SpotifyOAuth
from textblob import TextBlob
import sys

# Spotify credentials from your developer dashboard
# (Be sure to keep these private and secure)
SPOTIPY_CLIENT_ID = '6c95e04130fa4e948f0fc9175a0ace72'
SPOTIPY_CLIENT_SECRET = '09aaf5c2188e4276ab308f2842909c87'
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

# For this project, we need permission to create private playlists.
scope = "playlist-modify-private"

# ------------------------------------------------------------------------------
# Auth Manager: Authorization Code Flow (User-based authentication)
# ------------------------------------------------------------------------------
auth_manager = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope,
    cache_path=".cache-user"  # Where the user's token is stored
)

# Create a Spotipy client with user-based authentication
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_sentiment(text):
    """Determine mood from user input using TextBlob."""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return "happy"
    elif polarity < -0.1:
        return "sad"
    else:
        return "neutral"

def get_recommendations_for_mood(mood):
    """
    For a given mood, define parameters (seed genres and target audio features)
    and retrieve recommended tracks.
    """
    # Define mood-based parameters.
    # For "happy" mood, we now use only "pop" to avoid issues with invalid genres.
    mood_params = {
        "happy": {
            "seed_genres": ["pop"],
            "target_valence": 0.8,
            "target_energy": 0.7,
            "target_danceability": 0.7
        },
        "sad": {
            "seed_genres": ["acoustic", "folk"],
            "target_valence": 0.2,
            "target_energy": 0.3,
            "target_danceability": 0.3
        },
        "neutral": {
            "seed_genres": ["indie", "chill"],
            "target_valence": 0.5,
            "target_energy": 0.5,
            "target_danceability": 0.5
        }
    }
    params = mood_params.get(mood, mood_params["neutral"])

    # Debug: print the parameters to confirm the correct values are used
    print("Using recommendation parameters:", params)

    recommendations = sp.recommendations(
        seed_genres=params["seed_genres"],
        limit=20,
        target_valence=params["target_valence"],
        target_energy=params["target_energy"],
        target_danceability=params["target_danceability"],
    )
    return recommendations

def create_playlist_for_mood(mood, tracks):
    """
    Create a new private playlist in your account with the recommended tracks.
    """
    user = sp.current_user()
    user_id = user["id"]
    playlist_name = f"{mood.capitalize()} Mood Playlist"
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    playlist_id = playlist["id"]

    # Extract track URIs from the recommended tracks
    track_uris = [track["uri"] for track in tracks if track.get("uri")]
    if track_uris:
        sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=track_uris)
        print(f"\nCreated playlist '{playlist_name}' with {len(track_uris)} tracks.")
    else:
        print("No tracks to add.")
    return playlist_id

if __name__ == "__main__":
    # When you run this for the first time, Spotipy will open a browser window for authentication.
    user_input = input("Enter your mood description: ")
    mood = get_sentiment(user_input)
    print(f"\nDetected Mood: {mood}")

    recs = get_recommendations_for_mood(mood)
    if recs and recs.get("tracks"):
        print("\nRecommended Tracks:")
        for track in recs["tracks"]:
            artists = ", ".join(artist["name"] for artist in track["artists"])
            print(f"- {track['name']} by {artists}")
        # Create a new playlist with these recommended tracks
        create_playlist_for_mood(mood, recs["tracks"])
    else:
        print("No recommendations found for this mood.")
