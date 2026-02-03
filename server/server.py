from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from datetime import datetime

load_dotenv()


# app instance
app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = "Input"
REFERENCE_IMAGES_FOLDER = "Input/reference_images"
ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav", "m4a"}
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_AUDIO_SIZE = 100 * 1024 * 1024  # 100MB

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REFERENCE_IMAGES_FOLDER, exist_ok=True)


def allowed_audio_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS
    )


def allowed_image_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    )


@app.route("/api/home", methods=["GET"])
def home():
    return jsonify({"message": "Hello, World!"})


@app.route("/api/create", methods=["POST"])
def create():
    try:
        # Extract video description from form data
        video_description = request.form.get("videoDescription", "")

        # Extract audio file
        if "audioFile" not in request.files:
            return jsonify({"error": "Audio file is required"}), 400

        audio_file = request.files["audioFile"]

        if audio_file.filename == "":
            return jsonify({"error": "No audio file selected"}), 400

        if not allowed_audio_file(audio_file.filename):
            return jsonify(
                {"error": "Invalid audio file type. Allowed: MP3, WAV, M4A"}
            ), 400

        # Check file size
        audio_file.seek(0, os.SEEK_END)
        file_size = audio_file.tell()
        audio_file.seek(0)

        if file_size > MAX_AUDIO_SIZE:
            return jsonify(
                {
                    "error": f"Audio file exceeds 100MB limit. Current size: {file_size / 1024 / 1024:.2f}MB"
                }
            ), 400

        # Save audio file
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        audio_filename = secure_filename(audio_file.filename)
        audio_name, audio_ext = os.path.splitext(audio_filename)
        saved_audio_filename = f"{audio_name}_{timestamp}{audio_ext}"
        audio_path = os.path.join(UPLOAD_FOLDER, saved_audio_filename)
        audio_file.save(audio_path)

        # Extract and save reference images
        reference_images = request.files.getlist("referenceImages")
        saved_image_paths = []

        for idx, image_file in enumerate(reference_images):
            if image_file.filename == "":
                continue

            if not allowed_image_file(image_file.filename):
                continue  # Skip invalid image files

            # Save reference image
            image_filename = secure_filename(image_file.filename)
            image_name, image_ext = os.path.splitext(image_filename)
            saved_image_filename = f"{image_name}_{timestamp}_{idx}{image_ext}"
            image_path = os.path.join(REFERENCE_IMAGES_FOLDER, saved_image_filename)
            image_file.save(image_path)
            saved_image_paths.append(image_path)

        # Prepare response data
        response_data = {
            "message": "Video creation request received successfully!",
            "videoDescription": video_description,
            "audioFile": {
                "filename": saved_audio_filename,
                "path": audio_path,
                "size": file_size,
            },
            "referenceImages": [
                {"filename": os.path.basename(path), "path": path}
                for path in saved_image_paths
            ],
            "timestamp": timestamp,
        }

        print("Video creation request received:")
        print(f"  Description: {video_description}")
        print(f"  Audio file: {audio_path}")
        print(f"  Reference images: {len(saved_image_paths)}")

        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error processing video creation request: {str(e)}")
        return jsonify({"error": f"Server error: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT"))
