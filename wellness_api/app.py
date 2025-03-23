import os
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data_scrapper")

@app.route('/podcasts', methods=['GET'])
def get_podcasts():
    file_path = os.path.join(DATA_DIR, "spotify_podcasts.json")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            podcasts = json.load(file)
        return jsonify(podcasts)
    except FileNotFoundError:
        return jsonify({"error": "File not found", "path": file_path}), 500

@app.route('/blogs', methods=['GET'])
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
