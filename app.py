from flask import Flask, render_template, request
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon if needed
nltk.download('vader_lexicon')

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('data.csv')

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_intricate(text):
    """
    Analyze the sentiment of the given text using VADER and classify it into:
    'ecstatic', 'excited', 'happy', 'neutral', 'melancholic', 'sad', or 'depressed'
    """
    if not isinstance(text, str):
        text = ""
    # Remove non-ASCII characters
    text = text.encode('ascii', errors='ignore').decode('ascii')
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.8:
        return 'ecstatic'
    elif compound >= 0.6:
        return 'excited'
    elif compound >= 0.3:
        return 'happy'
    elif compound > -0.1:
        return 'neutral'
    elif compound > -0.35:
        return 'off'
    elif compound > -0.6:
        return 'melancholic'
    elif compound > -0.8:
        return 'sad'
    else:
        return 'depressed'

def filter_by_mood(dataframe, mood):
    """
    Filter the DataFrame based on the mood category using the 'valence' column.
    For positive moods (ecstatic, excited, happy): select songs with valence >= mean.
    For negative moods (melancholic, sad, depressed): select songs with valence < mean.
    For neutral mood: no filtering is applied.
    """
    if 'valence' in dataframe.columns:
        mean_valence = dataframe['valence'].mean()
        if mood in ['ecstatic', 'excited', 'happy']:
            return dataframe[dataframe['valence'] >= mean_valence]
        elif mood in ['melancholic', 'sad', 'depressed']:
            return dataframe[dataframe['valence'] < mean_valence]
    return dataframe

def filter_by_keywords(dataframe, user_input):
    """
    Further filter the DataFrame based on keywords in the user input.
    For example:
      - "dance": filter for above-average danceability.
      - "energetic": filter for above-average energy.
      - "acoustic" or "chill": filter for above-average acousticness.
    """
    user_input = user_input.lower()
    keyword_filters = {
        'dance': ('danceability', 'high'),
        'energetic': ('energy', 'high'),
        'acoustic': ('acousticness', 'high'),
        'chill': ('acousticness', 'high')
    }
    for keyword, (column, condition) in keyword_filters.items():
        if keyword in user_input and column in dataframe.columns:
            mean_val = dataframe[column].mean()
            if condition == 'high':
                dataframe = dataframe[dataframe[column] >= mean_val]
            else:
                dataframe = dataframe[dataframe[column] < mean_val]
    return dataframe

def generate_playlist(filtered_df, num_songs=50):
    """
    Generate a playlist by randomly sampling 'num_songs' from the filtered DataFrame.
    """
    if filtered_df.empty:
        return pd.DataFrame()
    num_songs = min(num_songs, len(filtered_df))
    return filtered_df.sample(n=num_songs)

@app.route('/', methods=['GET', 'POST'])
def home():
    playlist = None
    detected_mood = None
    if request.method == 'POST':
        user_input = request.form['mood_description']
        # Analyze sentiment to determine the mood category
        detected_mood = analyze_sentiment_intricate(user_input)
        # Filter by mood using the 'valence' column
        filtered_df = filter_by_mood(df, detected_mood)
        # Further filter using keywords
        filtered_df = filter_by_keywords(filtered_df, user_input)
        # Fallback: if no songs match, use the full dataset
        if filtered_df.empty:
            filtered_df = df
        # Generate the playlist with 50 songs
        playlist = generate_playlist(filtered_df, num_songs=50)
    # On a GET request, playlist and detected_mood remain None
    return render_template('index.html', playlist=playlist, mood=detected_mood)

if __name__ == '__main__':
    app.run(debug=True)

