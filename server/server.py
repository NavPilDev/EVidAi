from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv
from datetime import datetime
import uuid
from moviepy import VideoFileClip
from PIL import Image
from typing import List, Optional

load_dotenv()

# app instance
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


def secure_filename(filename: str) -> str:
    """Secure filename by removing path components"""
    return os.path.basename(filename).replace(" ", "_")


def allowed_audio_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS
    )


def allowed_image_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    )


# ====================
# Dummy MongoDB Functions
# ====================


def save_project(project_data: dict) -> str:
    """Save or update a project in the in-memory storage"""
    project_id = project_data.get("id")
    if not project_id:
        project_id = str(uuid.uuid4())
        project_data["id"] = project_id

    projects_db[project_id] = project_data
    return project_id


def get_all_projects() -> List[dict]:
    """Get all projects from storage"""
    return list(projects_db.values())


def get_project_by_id(project_id: str) -> Optional[dict]:
    """Get a single project by ID"""
    return projects_db.get(project_id)


# ====================
# Thumbnail Extraction
# ====================


def extract_video_thumbnail(video_path: str, project_id: str) -> Optional[str]:
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


# ====================
# API Routes
# ====================


@app.get("/api/home")
async def home():
    return {"message": "Hello, World!"}


@app.get("/api/projects")
async def get_projects():
    """Get all projects"""
    try:
        projects = get_all_projects()

        # Format projects for list view
        formatted_projects = []
        for project in projects:
            formatted_projects.append(
                {
                    "id": project.get("id"),
                    "title": project.get("title", "Untitled Project"),
                    "thumbnailUrl": project.get("thumbnailUrl"),
                    "lastEdited": project.get("lastEdited"),
                    "createdAt": project.get("createdAt"),
                }
            )

        # Sort by last edited time (most recent first)
        formatted_projects.sort(key=lambda x: x.get("lastEdited", ""), reverse=True)

        return {"projects": formatted_projects}
    except Exception as e:
        print(f"Error fetching projects: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {e}")


@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """Get a single project by ID"""
    try:
        project = get_project_by_id(project_id)

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        return project
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {e}")


@app.get("/api/thumbnails/{filename}")
async def get_thumbnail(filename: str):
    """Serve thumbnail images"""
    try:
        thumbnail_path = os.path.join(THUMBNAILS_FOLDER, filename)
        if not os.path.exists(thumbnail_path):
            raise HTTPException(status_code=404, detail="Thumbnail not found")
        return FileResponse(thumbnail_path)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error serving thumbnail: {str(e)}")
        raise HTTPException(status_code=404, detail="Thumbnail not found")


@app.post("/api/create")
async def create(
    videoDescription: str = Form(""),
    audioFile: UploadFile = File(...),
    referenceImages: List[UploadFile] = File(default=[]),
):
    """Create a new video project"""
    try:
        # Validate audio file
        if not audioFile.filename:
            raise HTTPException(status_code=400, detail="No audio file selected")

        if not allowed_audio_file(audioFile.filename):
            raise HTTPException(
                status_code=400,
                detail="Invalid audio file type. Allowed: MP3, WAV, M4A",
            )

        # Check file size
        file_content = await audioFile.read()
        file_size = len(file_content)

        if file_size > MAX_AUDIO_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Audio file exceeds 100MB limit. Current size: {file_size / 1024 / 1024:.2f}MB",
            )

        # Save audio file
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        audio_filename = secure_filename(audioFile.filename)
        audio_name, audio_ext = os.path.splitext(audio_filename)
        saved_audio_filename = f"{audio_name}_{timestamp}{audio_ext}"
        audio_path = os.path.join(UPLOAD_FOLDER, saved_audio_filename)

        # Save audio file
        with open(audio_path, "wb") as f:
            f.write(file_content)

        # Extract and save reference images
        saved_image_paths = []

        if referenceImages and len(referenceImages) > 0:
            for idx, image_file in enumerate(referenceImages):
                if not image_file.filename:
                    continue

                if not allowed_image_file(image_file.filename):
                    continue  # Skip invalid image files

                # Save reference image
                image_filename = secure_filename(image_file.filename)
                image_name, image_ext = os.path.splitext(image_filename)
                saved_image_filename = f"{image_name}_{timestamp}_{idx}{image_ext}"
                image_path = os.path.join(REFERENCE_IMAGES_FOLDER, saved_image_filename)

                # Read and save image file
                image_content = await image_file.read()
                with open(image_path, "wb") as f:
                    f.write(image_content)
                saved_image_paths.append(image_path)

        # Generate unique project ID
        project_id = str(uuid.uuid4())

        # Create project title from description or audio filename
        project_title = (
            videoDescription.strip() if videoDescription.strip() else audio_name
        )
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
            "description": videoDescription,
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
            "videoDescription": videoDescription,
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
        print(f"  Description: {videoDescription}")
        print(f"  Audio file: {audio_path}")
        print(f"  Reference images: {len(saved_image_paths)}")

        return response_data

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing video creation request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {e}")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    print(f"Starting FastAPI server on port {port}")
    uvicorn.run(app, host="127.0.0.1", port=port, reload=True)
