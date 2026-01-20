from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


import re

def get_video_id(url: str) -> str:
    patterns = [
        r"v=([^&]+)",
        r"youtu\.be/([^?&]+)",
        r"shorts/([^?&]+)",
        r"embed/([^?&]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube URL")


def fetch_and_print_transcript(video_url: str) -> str:
    transcript_text = ""

    try:
        video_id = get_video_id(video_url)

        yt_api = YouTubeTranscriptApi()

        transcript_list = yt_api.list(video_id)

        # 1️⃣ Try manually created transcripts first (any language)
        try:
            transcript = transcript_list.find_manually_created_transcript(
                [t.language_code for t in transcript_list]
            )
        except:
            # 2️⃣ Fallback to auto-generated transcripts (any language)
            transcript = transcript_list.find_generated_transcript(
                [t.language_code for t in transcript_list]
            )

        transcript_snippets = transcript.fetch()

        transcript_text = " ".join(chunk.text for chunk in transcript_snippets)

        if not transcript_text.strip():
            raise ValueError("Transcript is empty.")

        print(f"Transcript fetched successfully for video ID: {video_id}")

    except TranscriptsDisabled:
        raise ValueError("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise ValueError("No transcript available for this video.")
    except Exception as e:
        raise ValueError(f"Unexpected error: {e}")

    return transcript_text

# fetch_and_print_transcript("https://youtu.be/KeEHsuZ4Ja4?si=T3VNbfNsB_gmmExn")

def create_vector_store(text: str):
    # Optimized for FREE Gemini tier
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
   )


    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def ingest(video_url: str):
    text = fetch_and_print_transcript(video_url)
    create_vector_store(text)

if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    ingest(url)
    print("Video processed successfully!")
