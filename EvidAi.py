from google import genai
from dotenv import load_dotenv
from pexelsapi.pexels import Pexels
import os
import requests

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
pexel = Pexels(os.getenv("PEXELS_API_KEY"))


print("Enter Video Title:")
video_title = input()

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     contents="",
# )

# print(response.text)

## Pexels API
# https://api.pexels.com/v1/ for images
# https://api.pexels.com/videos/ for videos

search_photos = pexel.search_photos(
    query=video_title, orientation="", size="", color="", locale="", page=1, per_page=15
)

# Get the first photo from search results
first_photo = search_photos["photos"][0]
photo_url = first_photo["src"]["original"]  # or 'large', 'large2x', etc.

# Create Output directory if it doesn't exist
output_dir = "Output"
os.makedirs(output_dir, exist_ok=True)

# Download the photo
response = requests.get(photo_url)
if response.status_code == 200:
    file_extension = os.path.splitext(photo_url.split("?")[0])[1] or ".jpg"
    filename = f"{first_photo['id']}{file_extension}"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "wb") as f:
        f.write(response.content)
    print(f"Photo downloaded to {filepath}")
