import whisper
import json
import os
import json
import jsonKeywordExtractor as jke


# Load Whisper model (using 'base' model - you can change to 'tiny', 'small', 'medium', or 'large' for better accuracy)
model = whisper.load_model("base")

# Path to the audio file
audio_file = os.path.join("Input", "Mid.mp3")

print("Transcribing audio file...")
result = model.transcribe(audio_file, fp16=False)

with open("Output/output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

# Create Output directory if it doesn't exist
output_dir = "Output"
os.makedirs(output_dir, exist_ok=True)

# Extract keywords from the audio file
print("Saving keywords to file...")
jke.saveKeywordsToFile(output_dir + "/output.json", output_dir + "/outputKWE.json")

## Generate Video based on keywords
