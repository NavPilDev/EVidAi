from google import genai
from dotenv import load_dotenv
from pexelsapi.pexels import Pexels
import os

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

first_photo_id = search_photos["photos"][0]["id"]
# Get the photo URL
get_photo = pexel.get_photo(first_photo_id)
print(get_photo)
