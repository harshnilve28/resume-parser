from flask import Flask, request, jsonify
from db import insert_candidate
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/api/v1/candidate", methods=["POST"])
def create_candidate():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    if "candidate" not in data:
        return jsonify({"error": "Missing candidate data"}), 400

    try:
        insert_candidate(data)
        return jsonify({"message": "Inserted successfully"}), 201
    except Exception as e:
        logging.error(str(e))
        return jsonify({"error": "Database insertion failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
