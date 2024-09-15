from flask import Flask, request, jsonify
from pymongo import MongoClient
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MONGODB_URI = "mongodb+srv://josephsamuelm2021:Samenoch%4074@cluster0.itztqvl.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)
db = client["mptc"]
collection = db["songs"]

# Helper function to format song document
def format_song(song):
    return {
        "id": song.get("id"),
        "title": song.get("title"),
        "song": song.get("song")
    }

# CREATE: Add a new song
@app.route("/songs", methods=["POST"])
def add_song():
    data = request.json
    new_song = {
        "id": data.get("id"),
        "title": data.get("title"),
        "song": data.get("song")
    }
    collection.insert_one(new_song)
    return jsonify({"message": "Song added successfully"}), 201

# READ: Get all songs or a specific song by custom id
@app.route("/songs", methods=["GET"])
def get_songs():
    songs = collection.find()
    return jsonify([format_song(song) for song in songs]), 200

@app.route("/songs/<song_id>", methods=["GET"])
def get_song(song_id):
    song_id = int(song_id)
    song = collection.find_one({"id": song_id})
    if song:
        return jsonify(format_song(song)), 200
    else:
        return jsonify({"error": "Song not found"}), 404

# UPDATE: Update a song by custom id
@app.route("/songs/<song_id>", methods=["PUT"])
def update_song(song_id):
    data = request.json
    updated_song = {
        "title": data.get("title"),
        "song": data.get("song")
    }
    song_id = int(song_id)
    result = collection.update_one({"id": song_id}, {"$set": updated_song})
    
    if result.matched_count > 0:
        return jsonify({"message": "Song updated successfully"}), 200
    else:
        return jsonify({"error": "Song not found"}), 404

# DELETE: Delete a song by custom id
@app.route("/songs/<song_id>", methods=["DELETE"])
def delete_song(song_id):
    song_id = int(song_id)
    result = collection.delete_one({"id": song_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Song deleted successfully"}), 200
    else:
        return jsonify({"error": "Song not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)