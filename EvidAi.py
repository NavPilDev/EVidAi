import whisper
import json
import os
import json
import jsonKeywordExtractor as jke


# Load Whisper model (using 'base' model - you can change to 'tiny', 'small', 'medium', or 'large' for better accuracy)
model = whisper.load_model("base")

# Path to the audio file
audio_file = os.path.join("Input", "Parikrama.m4a")

print("Transcribing audio file...")
result = model.transcribe(audio_file, fp16=False)
print(result["text"])

# Create Output directory if it doesn't exist
output_dir = "Output"
os.makedirs(output_dir, exist_ok=True)

jke.saveKeywordsToFile(output_dir + "/output.json", output_dir + "/outputKWE.json")
# print(f"Transcription saved to {output_file}")
# print(f"Transcribed text: {result['text']}")
