from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
from moviepy import VideoFileClip
from PIL import Image

load_dotenv()


# app instance
app = Flask(__name__)
# Configure CORS to allow requests from the frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configuration
UPLOAD_FOLDER = "Input"
REFERENCE_IMAGES_FOLDER = "Input/reference_images"
OUTPUT_FOLDER = "Output"
THUMBNAILS_FOLDER = "Output/thumbnails"
ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav", "m4a"}
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_AUDIO_SIZE = 100 * 1024 * 1024  # 100MB

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REFERENCE_IMAGES_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(THUMBNAILS_FOLDER, exist_ok=True)

# In-memory storage to simulate MongoDB
# Structure: {project_id: {project_data}}
projects_db = {}


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


# ====================
# Dummy MongoDB Functions
# ====================

def save_project(project_data):
    """Save or update a project in the in-memory storage"""
    project_id = project_data.get("id")
    if not project_id:
        project_id = str(uuid.uuid4())
        project_data["id"] = project_id
    
    projects_db[project_id] = project_data
    return project_id


def get_all_projects():
    """Get all projects from storage"""
    return list(projects_db.values())


def get_project_by_id(project_id):
    """Get a single project by ID"""
    return projects_db.get(project_id)


# ====================
# Thumbnail Extraction
# ====================

def extract_video_thumbnail(video_path, project_id):
    """Extract first frame from video and save as thumbnail"""
    try:
        if not os.path.exists(video_path):
            return None
        
        # Load video and get first frame
        clip = VideoFileClip(video_path)
        frame = clip.get_frame(0)  # Get frame at 0 seconds
        
        # Convert numpy array to PIL Image
        thumbnail_image = Image.fromarray(frame)
        
        # Save thumbnail
        thumbnail_filename = f"thumbnail_{project_id}.jpg"
        thumbnail_path = os.path.join(THUMBNAILS_FOLDER, thumbnail_filename)
        thumbnail_image.save(thumbnail_path, "JPEG", quality=85)
        
        clip.close()
        
        return thumbnail_path
    except Exception as e:
        print(f"Error extracting thumbnail: {str(e)}")
        return None


@app.route("/api/home", methods=["GET"])
def home():
    return jsonify({"message": "Hello, World!"})


@app.route("/api/projects", methods=["GET"])
def get_projects():
    """Get all projects"""
    try:
        projects = get_all_projects()
        
        # Format projects for list view
        formatted_projects = []
        for project in projects:
            formatted_projects.append({
                "id": project.get("id"),
                "title": project.get("title", "Untitled Project"),
                "thumbnailUrl": project.get("thumbnailUrl"),
                "lastEdited": project.get("lastEdited"),
                "createdAt": project.get("createdAt"),
            })
        
        # Sort by last edited time (most recent first)
        formatted_projects.sort(key=lambda x: x.get("lastEdited", ""), reverse=True)
        
        return jsonify({"projects": formatted_projects}), 200
    except Exception as e:
        print(f"Error fetching projects: {str(e)}")
        return jsonify({"error": f"Server error: {e}"}), 500


@app.route("/api/projects/<project_id>", methods=["GET"])
def get_project(project_id):
    """Get a single project by ID"""
    try:
        project = get_project_by_id(project_id)
        
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        return jsonify(project), 200
    except Exception as e:
        print(f"Error fetching project: {str(e)}")
        return jsonify({"error": f"Server error: {e}"}), 500


@app.route("/api/thumbnails/<filename>", methods=["GET"])
def get_thumbnail(filename):
    """Serve thumbnail images"""
    try:
        return send_from_directory(THUMBNAILS_FOLDER, filename)
    except Exception as e:
        print(f"Error serving thumbnail: {str(e)}")
        return jsonify({"error": "Thumbnail not found"}), 404


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

        # Generate unique project ID
        project_id = str(uuid.uuid4())
        
        # Create project title from description or audio filename
        project_title = video_description.strip() if video_description.strip() else audio_name
        if not project_title:
            project_title = "Untitled Project"
        
        # For now, video path will be set when video is generated
        # Expected format: Output/result_{timestamp}.mp4
        expected_video_path = os.path.join(OUTPUT_FOLDER, f"result_{timestamp}.mp4")
        video_url = expected_video_path if os.path.exists(expected_video_path) else None
        
        # Try to extract thumbnail if video exists
        thumbnail_url = None
        if video_url and os.path.exists(video_url):
            thumbnail_path = extract_video_thumbnail(video_url, project_id)
            if thumbnail_path:
                # Return relative path for API access
                thumbnail_filename = os.path.basename(thumbnail_path)
                thumbnail_url = f"/api/thumbnails/{thumbnail_filename}"
        
        # Create project data
        now = datetime.now().isoformat()
        project_data = {
            "id": project_id,
            "title": project_title,
            "description": video_description,
            "thumbnailUrl": thumbnail_url,
            "videoUrl": video_url,
            "audioFile": {
                "filename": saved_audio_filename,
                "path": audio_path,
                "size": file_size,
            },
            "referenceImages": [
                {"filename": os.path.basename(path), "path": path}
                for path in saved_image_paths
            ],
            "createdAt": now,
            "lastEdited": now,
            "storyboard": {},
            "agentHistory": [],
            "timestamp": timestamp,
        }
        
        # Save project to storage
        save_project(project_data)

        # Prepare response data
        response_data = {
            "message": "Video creation request received successfully!",
            "projectId": project_id,
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
        print(f"  Project ID: {project_id}")
        print(f"  Description: {video_description}")
        print(f"  Audio file: {audio_path}")
        print(f"  Reference images: {len(saved_image_paths)}")

        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error processing video creation request: {str(e)}")
        return jsonify({"error": f"Server error: {e}"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"Starting server on port {port}")
    app.run(debug=True, host="127.0.0.1", port=port)
