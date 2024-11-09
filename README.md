# Song of the Day

This project is a Flask web application that recommends a song based on the user's mood. It uses the Spotify API to fetch song recommendations.

## Features

- Select a mood to get a song recommendation
- Displays the song name, artist, and album cover
- Provides a link to listen to the song on Spotify

## Setup

### Prerequisites

- Python 3.x
- Flask
- Requests

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/song-of-the-day.git
    cd song-of-the-day
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up your Spotify API credentials:

    - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
    - Create a new application
    - Copy the `Client ID` and `Client Secret` and replace the placeholders in `app.py`

4. Run the application:

    ```sh
    python app.py
    ```

5. Open your browser and go to `http://localhost:5000`

## Usage

1. Select your mood from the dropdown menu.
2. Click the "Get Song" button.
3. The recommended song will be displayed along with the artist and album cover.
4. Click on the album cover to listen to the song on Spotify.

## Project Structure

- `app.py`: The main Flask application file.
- `templates/index.html`: The HTML template for the web interface.
- `static/style.css`: The CSS file for styling the web interface.
- `requirements.txt`: The list of required Python packages.