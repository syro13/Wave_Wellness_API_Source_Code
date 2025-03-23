import os
from flask import Flask, jsonify, request, abort
import json
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.environ.get("WAVE_API_KEY")

# Auth decorator
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if not key or key != API_KEY:
            abort(401, description="Unauthorized: Invalid or missing API key")
        return f(*args, **kwargs)
    return decorated

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data_scrapper")

@app.route('/podcasts', methods=['GET'])
@require_api_key
def get_podcasts():
    file_path = os.path.join(DATA_DIR, "spotify_podcasts.json")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            podcasts = json.load(file)
        return jsonify(podcasts)
    except FileNotFoundError:
        return jsonify({"error": "File not found", "path": file_path}), 500

@app.route('/blogs', methods=['GET'])
@require_api_key
def get_blogs():
    file_path = os.path.join(DATA_DIR, "irishlife_blogs.json")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            blogs = json.load(file)
        return jsonify(blogs)
    except FileNotFoundError:
        return jsonify({"error": "File not found", "path": file_path}), 500

@app.route('/')
def hello():
    return """
    <h3>Welcome to the Wave API</h3>
    <p>Use <code>/podcasts</code> to get a list of available Spotify podcast episodes.</p>
    <p>Use <code>/blogs</code> to get a list of available blogs to read.</p>
    """

if __name__ == '__main__':
    app.run(debug=True)
