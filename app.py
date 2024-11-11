from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

CLIENT_ID = "your client id"
CLIENT_SECRET = "your secret key"

# Function to get an access token from Spotify
def get_spotify_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    return auth_response.json().get("access_token")

def get_song_for_mood(mood):
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Define mood-based audio features
    mood_features = {
        "Happy": {
            "energy": {"value": (0.7, 0.85), "weight": 0.8},
            "valence": {"value": (0.7, 0.95), "weight": 1.0},
            "danceability": {"value": (0.6, 0.9), "weight": 0.7},
            "tempo": {"value": (100, 140), "weight": 0.6},
            "acousticness": {"value": (0.1, 0.4), "weight": 0.5},
            "instrumentalness": {"value": (0.0, 0.4), "weight": 0.3},
            "loudness": {"value": (-10, -5), "weight": 0.4},
            "speechiness": {"value": (0.0, 0.3), "weight": 0.2}
        },
        "Sad": {
            "energy": {"value": (0.1, 0.4), "weight": 0.8},
            "valence": {"value": (0.1, 0.4), "weight": 1.0},
            "danceability": {"value": (0.2, 0.5), "weight": 0.6},
            "tempo": {"value": (50, 80), "weight": 0.7},
            "acousticness": {"value": (0.5, 0.9), "weight": 0.8},
            "instrumentalness": {"value": (0.0, 0.7), "weight": 0.4},
            "loudness": {"value": (-15, -8), "weight": 0.5},
            "speechiness": {"value": (0.0, 0.4), "weight": 0.3}
        },
        "Energetic": {
            "energy": {"value": (0.8, 1.0), "weight": 1.0},
            "valence": {"value": (0.6, 0.9), "weight": 0.7},
            "danceability": {"value": (0.7, 1.0), "weight": 0.9},
            "tempo": {"value": (120, 180), "weight": 0.8},
            "acousticness": {"value": (0.0, 0.3), "weight": 0.6},
            "instrumentalness": {"value": (0.0, 0.5), "weight": 0.3},
            "loudness": {"value": (-7, -2), "weight": 0.7},
            "speechiness": {"value": (0.0, 0.4), "weight": 0.2}
        },
        "Relaxed": {
            "energy": {"value": (0.2, 0.5), "weight": 0.9},
            "valence": {"value": (0.3, 0.6), "weight": 0.7},
            "danceability": {"value": (0.3, 0.6), "weight": 0.5},
            "tempo": {"value": (60, 100), "weight": 0.6},
            "acousticness": {"value": (0.5, 0.9), "weight": 0.8},
            "instrumentalness": {"value": (0.2, 0.8), "weight": 0.6},
            "loudness": {"value": (-15, -8), "weight": 0.5},
            "speechiness": {"value": (0.0, 0.3), "weight": 0.3}
        }
    }

    # Get the audio features for the selected mood
    features = mood_features.get(mood, {
        "energy": 0.5, "valence": 0.5, "danceability": 0.5, "tempo": 100, "acousticness": 0.5
    })
    
    # Construct the recommendations API URL with additional audio features
    recommendations_url = (
        "https://api.spotify.com/v1/recommendations"
        f"?limit=1&seed_genres=pop&energy={features['energy']}"
        f"&valence={features['valence']}&danceability={features['danceability']}"
        f"&tempo={features['tempo']}&acousticness={features['acousticness']}")
    
    # Make the request to the Spotify API
    response = requests.get(recommendations_url, headers=headers)
    
    if response.status_code == 200:
        track = response.json()["tracks"][0]
        return {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "url": track["external_urls"]["spotify"],
            "image": track["album"]["images"][0]["url"]
        }
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_song', methods=['POST'])
def get_song():
    mood = request.form.get('mood')
    song = get_song_for_mood(mood)
    if not song:
        return jsonify({"error": "Could not fetch song recommendation."})
    return jsonify(song)

if __name__ == '__main__':
    app.run(host='0.0.0.0')