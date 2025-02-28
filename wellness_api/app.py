from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/podcasts', methods=['GET'])
def get_podcasts():
    with open("..\\data_scrapper\\spotify_podcasts.json", 'r', encoding='utf-8') as file:
        podcasts = json.load(file)
    return jsonify(podcasts)
@app.route('/blogs', methods=['GET'])
def get_blogs():
    with open("..\\data_scrapper\\irishlife_blogs.json", 'r', encoding='utf-8') as file:
        blogs = json.load(file)
    return jsonify(blogs)
@app.route('/')
def hello():
    return (
        """
        <h3>Welcome to the Wave API</h3>
        <p>Use <code>/podcasts</code> to get a list of available Spotify podcast episodes.</p>
        <p>Use <code>/blogs</code> to get a list of available blogs to read.</p>
        """
    )

if __name__ == '__main__':
    app.run(debug=True)