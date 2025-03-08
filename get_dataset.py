import kagglehub
import json
import os
from textblob import TextBlob

# Download dataset
dataset_path = kagglehub.dataset_download("himanshuwagh/spotify-million")
print(dataset_path)

# Define the slice file to use
slice_file = os.path.join(dataset_path, "data/mpd.slice.0-999.json")
print(slice_file)

# # Load JSON data
with open(slice_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract playlists
playlists = data["playlists"]

# Display an example playlist
print(json.dumps(playlists[0], indent=2))

print(data.keys())  # Should show ['info', 'playlists']
print(playlists[0].keys())  # Shows available fields for each playlist

def find_playlists_by_keyword(keyword, playlists):
    """Search playlists by keyword in title."""
    return [pl for pl in playlists if keyword.lower() in pl["name"].lower()]


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
    
def recommend_playlist(user_input, playlists):
    mood = get_sentiment(user_input)
    matched_playlists = find_playlists_by_keyword(mood, playlists)
    
    if matched_playlists:
        chosen_playlist = matched_playlists[0]  # Select the first match
        print(f"Recommended Playlist: {chosen_playlist['name']}")
        for track in chosen_playlist["tracks"][:10]:  # Show top 10 tracks
            print(f"{track['artist_name']} - {track['track_name']}")
    else:
        print("No matching playlist found.")


if __name__ == "__main__":
    user_input = input("Enter your mood description: ")
    recommend_playlist(user_input, playlists)