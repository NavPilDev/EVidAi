from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()


# app instance
app = Flask(__name__)
CORS(app)


@app.route("/api/home", methods=["GET"])
def home():
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT"))
