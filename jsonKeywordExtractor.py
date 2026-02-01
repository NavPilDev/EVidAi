import json
import nltk
import string
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data if not already present
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

STOPWORDS = set(stopwords.words("english"))


def extractKeywords(json_data):
    """
    Extract keywords from each sentence/segment in the JSON data.
    Returns a list of dictionaries with segment info and extracted keywords.
    """
    with open(json_data, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []

    for segment in data["segments"]:
        text = segment["text"].strip()

        # Tokenize the text
        tokens = word_tokenize(text.lower())

        # Filter out stopwords, punctuation, and short words
        candidate_keywords = [
            word
            for word in tokens
            if word not in STOPWORDS
            and word not in string.punctuation
            and len(word) > 2
            and word.isalnum()
        ]

        # Score keywords by frequency and length
        word_freq = Counter(candidate_keywords)

        # Calculate scores: frequency * length (longer, more frequent words score higher)
        keyword_scores = {word: (freq * len(word)) for word, freq in word_freq.items()}

        # Sort by score (descending) and select top 5
        sorted_keywords = sorted(
            keyword_scores.items(), key=lambda x: x[1], reverse=True
        )

        # Extract top 3-5 keywords (prefer 5, but at least 3 if available)
        top_keywords = [word for word, score in sorted_keywords[:5]]

        # Ensure we have at least 3 keywords if available, but not more than 5
        if len(top_keywords) < 3 and len(candidate_keywords) >= 3:
            # If we have fewer than 3, take up to 3 from candidates
            top_keywords = list(dict.fromkeys(candidate_keywords))[:3]
        elif len(top_keywords) > 5:
            top_keywords = top_keywords[:5]

        # Create result entry with segment info and keywords
        result_entry = {
            "id": segment["id"],
            "start": segment["start"],
            "end": segment["end"],
            "text": text,
            "keywords": top_keywords,
        }

        results.append(result_entry)

    return results


def saveKeywordsToFile(json_data, output_path):
    """
    Extract keywords from JSON data and save to output file.
    """
    keywords_data = extractKeywords(json_data)

    output_data = {
        "source_file": json_data,
        "total_segments": len(keywords_data),
        "segments_with_keywords": keywords_data,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Keywords extracted and saved to {output_path}")
    return output_data


if __name__ == "__main__":
    saveKeywordsToFile("Output/output.json", "Output/outputKWE.json")
