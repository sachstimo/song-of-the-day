# Song of the Day

This project is a Flask web application that recommends a song based on your current mood. It uses the Spotify API to then fetch a suitable song recommendations and renders the output in a simple, clean HTML page showing both the song title & artist as well as the cover with an updated HTML background color based on the song cover.

## Webpage features

- Select a mood to get a song recommendation
- Displays the song name, artist, and album cover
- Updates the webpage background based on the cover image colors
- Provides a link to listen to the song on Spotify

## Setup

### Prerequisites

- Python 3.10
- Flask
- Requests
- Flask==2.0.2
- Werkzeug==2.0.3
- gunicorn (used for Flask production deployment)

> **Note:** Docker is not required to run the application, but highly recommended in order to run the webservice in a detached and stable container environment.

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
    - Copy the `Client ID` and `Client Secret` and replace the placeholders in [`app.py`](app.py)

**Using Flask:**

4. Run the application (from the project directory):
    ```sh
    python app.py
    ```

5. Open your browser and go to `http://localhost:5000`

**Using docker:**

4. Run the application (from the project directory):
    ```sh
    docker build -t docker build -t your_image_name .
    docker run -d -p 5000:5000
    ```

5. Open your browser and go to `http://localhost:5000` or deploy on a remote webserver or AWS EC2 instance. Make sure to allow TCP traffic on `port:5000` or use an [nginx reverse proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) to enable HTTPS re-routing.


## How to use

1. Select your mood from the dropdown menu.
2. Click the "Get Song" button.
3. The recommended song will be displayed along with the artist and album cover.
4. Click on the album cover to listen to the song on Spotify.

>**Note:** To avoid a `HTML Status Code 429: Too many requests` error due to the Spotify API request limit, a **cooldown of 4 seconds** between requests is implemented. This can be adjusted by tweaking the `request_interval` global variable.

## Project Structure

- [`app.py`](app.py): The main Flask application file.
- [`templates/index.html`](templates/index.html): The HTML template for the web interface.
- [`static/`](static/): The directory for static files such as CSS and images or your Favion to be displayed on the browser tab.
- [`requirements.txt`](requirements.txt): List of required Python packages.
- [`Dockerfile`](Dockerfile): Dockerfile for building the containerized.
- [`.dockerignore`](.dockerignore): file specifying which files and directories to ignore in the Docker build process.