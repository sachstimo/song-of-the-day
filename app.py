from flask import Flask, jsonify, render_template, request
import requests
import random
import time
import csv

app = Flask(__name__)

CLIENT_ID = "your client id"
CLIENT_SECRET = "your secret key"

last_request_time = 0
request_interval = 3  # Minimum interval between requests in seconds

# Getting the Spotify access token
def get_spotify_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    return auth_response.json().get("access_token")

# Get a song recommendation based on the mood
def get_song_for_mood(mood):
    global last_request_time

    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Throttle requests: Ensure a delay between consecutive requests
    current_time = time.time()
    if current_time - last_request_time < request_interval:
        time.sleep(request_interval - (current_time - last_request_time))

    last_request_time = time.time()

    # Define mood-based audio features
    mood_features = {
        "Happy": {
            "energy": (0.7, 0.85),
            "valence": (0.7, 0.95),
            "danceability": (0.6, 0.9),
            "tempo": (100, 140),
            "acousticness": (0.1, 0.4),
            "instrumentalness": (0.0, 0.4),
            "loudness": (-10, -5),
            "speechiness": (0.0, 0.3),
            "seed_genres": ["pop", "party", "dance", "upbeat"]
        },
        "Sad": {
            "energy": (0.1, 0.4),
            "valence": (0.1, 0.4),
            "danceability": (0.2, 0.5),
            "tempo": (50, 80),
            "acousticness": (0.5, 0.9),
            "instrumentalness": (0.0, 0.7),
            "loudness": (-15, -8),
            "speechiness": (0.0, 0.4),
            "seed_genres": ["acoustic", "piano", "sad", "singer-songwriter"]
        },
        "Energetic": {
            "energy": (0.8, 1.0),
            "valence": (0.6, 0.9),
            "danceability": (0.7, 1.0),
            "tempo": (120, 180),
            "acousticness": (0.0, 0.3),
            "instrumentalness": (0.0, 0.5),
            "loudness": (-7, -2),
            "speechiness": (0.0, 0.4),
            "seed_genres": ["electronic", "dance", "workout", "rock"]
        },
        "Relaxed": {
            "energy": (0.2, 0.5),
            "valence": (0.3, 0.6),
            "danceability": (0.3, 0.6),
            "tempo": (60, 100),
            "acousticness": (0.5, 0.9),
            "instrumentalness": (0.2, 0.8),
            "loudness": (-15, -8),
            "speechiness": (0.0, 0.3),
            "seed_genres": ["chill", "ambient", "jazz", "lofi"]
        }
    }

    # Get the features and seed genres for the selected mood
    features = mood_features.get(mood)
    if not features:
        return None

    # Generate random values within the specified ranges
    target_energy = random.uniform(*features["energy"])
    target_valence = random.uniform(*features["valence"])
    target_danceability = random.uniform(*features["danceability"])
    target_tempo = random.uniform(*features["tempo"])
    target_acousticness = random.uniform(*features["acousticness"])
    target_instrumentalness = random.uniform(*features["instrumentalness"])
    target_loudness = random.uniform(*features["loudness"])
    target_speechiness = random.uniform(*features["speechiness"])
    seed_genres = ",".join(features["seed_genres"])

    # Spotify API request URL
    recommendations_url = (
        f"https://api.spotify.com/v1/recommendations?limit=1&seed_genres={seed_genres}"
        f"&target_energy={target_energy}&target_valence={target_valence}"
        f"&target_danceability={target_danceability}&target_tempo={target_tempo}"
        f"&target_acousticness={target_acousticness}&target_instrumentalness={target_instrumentalness}"
        f"&target_loudness={target_loudness}&target_speechiness={target_speechiness}"
    )

    # Making the API request
    response = requests.get(recommendations_url, headers=headers)
    if response.status_code == 200:
        track = response.json()["tracks"][0]
        return {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "url": track["external_urls"]["spotify"],
            "image": track["album"]["images"][0]["url"]
        }
    
    elif response.status_code == 429:
        # Handle Spotfy rate limit error
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            print(f"Rate limit exceeded. Please retry after {retry_after} seconds.")
            return {"error": f"Rate limit exceeded. Please try again after {retry_after} seconds."}
        else:
            print("Rate limit exceeded. Please try again later.")
            return {"error": "Rate limit exceeded. Please try again later."}
    else:
        print(f"Error: Could not fetch song recommendation. Status Code: {response.status_code}")
        return {"error": "Could not fetch song recommendation."}

# Load quotes for the quote page
def load_quotes_from_csv(filename):
    quotes = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            quotes.append({"quote": row["quote"], "author": row["author"]})
    return quotes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_song')
def song_page():
    return render_template('song.html')

@app.route('/get_song', methods=['POST'])
def get_song():
    data = request.get_json()
    mood = data.get('mood')
    if not mood:
        return jsonify({"error": "Please select a mood."})
    song = get_song_for_mood(mood)
    return jsonify(song)

@app.route('/get_quote', methods=['GET'])
def get_quote():
    quotes = load_quotes_from_csv('static/quotes.csv')
    selected_quote = random.choice(quotes)
    return render_template('quote.html', quote=selected_quote["quote"], author=selected_quote["author"])

if __name__ == '__main__':
    app.run(host='0.0.0.0')