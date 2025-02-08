from openai import OpenAI
import openai
import moviepy as mp 
import os
import requests
from io import BytesIO

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to download video from a URL
def download_video_from_url(url, output_path):
    try:
        # Fetch the video content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        
        # Save the video content to a file
        with open(output_path, 'wb') as file:
            file.write(response.content)
        
        return output_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading video: {e}")
        return None

# Function to extract audio from an MP4 file
def extract_audio_from_mp4(mp4_file_path, output_audio_path):
    video = mp.VideoFileClip(mp4_file_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path)

# Function to transcribe audio using OpenAI Whisper
def transcribe_audio(audio_file_path):
    client = OpenAI()
    try:
        with open(audio_file_path, 'rb') as audio_file:
            # Use Whisper API to transcribe the audio
            response = client.audio.transcriptions.create(
                model="whisper-1",  # Whisper model
                file=audio_file
            )
            return response.text  # Extract transcribed text from the response
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

def extract_keywords_from_text(text):
    client = OpenAI()
    try:
        # Prompt OpenAI's GPT model to extract relevant keywords from the text
        prompt = f"Extract the most relevant keywords or key phrases from the following text:\n\n{text}\n\nKeywords:"
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use "gpt-3.5-turbo" or other chat-based models
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # The API will return choices with a "message" field that contains the output
        keywords = response.choices[0].message.content.strip()
        
        # Convert the keywords into a list format by splitting them
        keyword_list = keywords.split(',')
        return [keyword.strip() for keyword in keyword_list]
    
    except Exception as e:
        print(f"Error during keyword extraction: {e}")
        return []
    

# Main function to download video, extract audio, transcribe and get keywords
# PARAM[out] list of relevant keywords extracted from video
# def main(video_url, keywords):
#     # Step 1: Download the video from the URL
#     video_file_path = "downloaded_video.mp4"  # Path to save the downloaded video
#     print(f"Downloading video from {video_url}...")
#     video_file_path = download_video_from_url(video_url, video_file_path)

#     if not video_file_path:
#         print("Video download failed.")
#         return

#     print(f"Downloaded video: {video_file_path}")

#     audio_file_path = "extracted_audio.wav"  # Path to save extracted audio

#     # Step 2: Extract audio from the MP4 file
#     print(f"Extracting audio from {video_file_path}...")
#     extract_audio_from_mp4(video_file_path, audio_file_path)

#     # Step 3: Transcribe audio using OpenAI Whisper
#     print(f"Transcribing audio from {audio_file_path}...")
#     transcription = transcribe_audio(audio_file_path)

#     if transcription:
#         print("Transcription Result:\n", transcription)
        
#         # Step 4: Extract keywords from the transcription
#         print("Extracting keywords...")
#         keywords = extract_keywords_from_text(transcription)
#         print("Extracted Keywords:", keywords)
#     else:
#         print("Transcription failed.")

#     # Clean up extracted audio file and video
#     if os.path.exists(audio_file_path):
#         os.remove(audio_file_path)
#     if os.path.exists(video_file_path):
#         os.remove(video_file_path)

# # Testing usage
# if __name__ == "__main__":
#     video_url = "https://hiloblobstorage.blob.core.windows.net/tartanads/IMG_4213.mp4" #url here
#     keywords = []
#     main(video_url, keywords)

def main(photo_url, keywords):
    """Processes an image, extracts text, and filters relevant words."""
    print(f"Processing image: {photo_url}")

    text = extract_text(photo_url)
    if not text:
        print("No text extracted from image.")
        return

    print("\nExtracted Text:")
    print(text)

    relevant_words = filter_relevant_words(text, keywords)
    
    print("\nRelevant Words:")
    print(relevant_words if relevant_words else "No relevant words found.")

if __name__ == "__main__":
    photo_url = photo_url = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fsimple-veganista.com%2Fgreen-vegetables%2F&psig=AOvVaw3RyN9Kc6vex4ivitMIzsoM&ust=1739101275790000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCLiq3p__s4sDFQAAAAAdAAAAABAg"  #photo url
    keywords = []
    main(photo_url, keywords)

import cv2
import numpy as np
from PIL import Image

def preprocess_image(photo_url):
    image = cv2.imread(photo_url, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    _, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)  # Convert to black & white
    return binary_image

import pytesseract

def extract_text(photo_url):
    preprocessed_img = preprocess_image(photo_url)
    text = pytesseract.image_to_string(preprocessed_img)
    return text

def filter_relevant_words(text, keywords):
    words = text.lower().split()
    relevant_words = [word for word in words if word in keywords]
    return relevant_words


