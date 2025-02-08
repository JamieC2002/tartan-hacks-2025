import base64
import glob
import subprocess
import openai
import moviepy as mp 
import os
import requests
from io import BytesIO
import string, secrets

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

# ✅ **FFmpeg Extract Frames**
def extract_frames_from_video(mp4_path, output_folder="temp_frames", fps=1):
    """Extracts frames from a video at a given FPS using FFmpeg."""
    os.makedirs(output_folder, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-i", mp4_path,
        "-vf", f"fps={fps}",
        os.path.join(output_folder, "frame_%04d.jpg"),
        "-y"
    ]
    subprocess.run(cmd, check=True)
    return output_folder


# ✅ **Base64 Encode Image for OpenAI**
def encode_image(image_path):
    """Encodes an image in Base64 format for OpenAI API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# ✅ **Extract Keywords from Image Frames using OpenAI**
def extract_keywords_from_frames(mp4_path):
    """Extracts frames from a video and processes them for keyword extraction."""

    print(f"Extracting frames from {mp4_path}...")
    frame_output_folder = extract_frames_from_video(mp4_path)

    frames = sorted(glob.glob(os.path.join(frame_output_folder, "*.jpg")))
    if not frames:
        print("No frames extracted.")
        return []

    print(f"Extracted {len(frames)} frames.")

    # **Prepare images for OpenAI API**
    image_list = [
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(frame)}"}}
        for frame in frames
    ]

    # **Prompt for OpenAI**
    prompt = """
        ### Task:
        You are given a snapshots of a video, represented by frames.
        Your goal is to extract **only the most relevant, precise, and meaningful keywords** that accurately represent the advertisement's content.

        ### Instructions:

        1. **Understand the Advertisement:**  
        - Analyze the given frames to identify the key topics, themes, and core messages.

        2. **Extract Only Relevant Keywords (No Phrases):**  
        - Focus on **single words only** that **directly describe** the advertised product, service, or theme.  
        - Do not include multi-word phrases.  
        - Example of correct extraction: `["dishwasher", "cleaning", "technology"]`  
        - Example of incorrect extraction (Do Not Do This): `["water-saving technology", "environmentally conscious households"]`  

        3. **Exclude Unnecessary Words:**  
        - Remove **filler words, generic adjectives**, and **irrelevant** terms.  
        - Do not include **phrases** like `"run faster", "play longer"`.  

        4. **Strict Output Format (No Extra Text):**  
        - Return **only** a single **comma-separated string of keywords** (no extra text, no labels, no white-spaces).  
        - The output **must be formatted exactly like this**:  
            ```
            keyword1,keyword2,keyword3,keyword4
            ```
        - Do not return a list, JSON, or extra formatting.  

        ### Example Output (Extracted Keywords):  
        EcoClean,dishwasher,water-saving,cleaning,spotless,environmentally,technology
        
        ### Additional Requirements:
        -  Return at least 5 but no more than 10 keywords.
        -  Ensure all extracted keywords are directly relevant to the product, service, or theme of the ad.
    """

    print("Sending frames to OpenAI for keyword extraction...")
    
    try:
        response = client.chat.completions.create(
           model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt}
                    ] + image_list,
                }
            ],
            max_tokens=300,
        )
        keywords = response.choices[0].message.content
    except Exception as e:
        print(f"Error during keyword extraction: {e}")
        keywords = ""

    # **Clean up extracted frames**
    for frame in frames:
        os.remove(frame)
    os.rmdir(frame_output_folder)

    return keywords.split(",")

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
    def clean_and_extract_keywords(keywords):
        import re
        # Remove dashes (-), newlines (\n), and extra spaces
        cleaned_text = re.sub(r"[-,\n]", " ", keywords)  # Replace unwanted characters with spaces
        
        # Split into a list using whitespace and remove empty elements
        keyword_list = [word.strip() for word in cleaned_text.split() if word.strip()]
        keyword_set = set(keyword_list)
        return keyword_set
        
    
    try:
        # Prompt OpenAI's GPT model to extract relevant keywords from the text
        prompt = f"""
        ### Task:
        You are given a transcribed text version of an advertisement. 
        Your goal is to extract **only the most relevant, precise, and meaningful keywords** that accurately represent the advertisement's content.

        ### Instructions:

        1. **Understand the Advertisement:**  
        - Analyze the transcribed text to identify the key topics, themes, and core messages.

        2. **Extract Only Relevant Keywords (No Phrases):**  
        - Focus on **single words only** that **directly describe** the advertised product, service, or theme.  
        - Do not include multi-word phrases.  
        - Example of correct extraction: `["dishwasher", "cleaning", "technology"]`  
        - Example of incorrect extraction (Do Not Do This): `["water-saving technology", "environmentally conscious households"]`  

        3. **Exclude Unnecessary Words:**  
        - Remove **filler words, generic adjectives**, and **irrelevant** terms.  
        - Do not include **phrases** like `"run faster", "play longer"`.  

        4. **Strict Output Format (No Extra Text):**  
        - Return **only** a single **comma-separated string of keywords** (no extra text, no labels).  
        - The output **must be formatted exactly like this**:  
            ```
            keyword1,keyword2,keyword3,keyword4
            ```
        - Do not return a list, JSON, or extra formatting.  

        ### Example Input (Transcribed Advertisement):
        "Introducing the all-new EcoClean dishwasher—built with advanced water-saving technology and a powerful cleaning system. 
        EcoClean ensures spotless dishes while using 50% less water, making it the perfect choice for environmentally conscious households."

        ### Example Output (Extracted Keywords) (Do Not Change Format):  
        EcoClean,dishwasher,water-saving,cleaning,spotless,environmentally,technology
        
        ### Additional Requirements:
        -  Return at least 5 but no more than 15 keywords per advertisement.
        -  Ensure all extracted keywords are directly relevant to the product, service, or theme of the ad.
        
        Below is the transcribed text version of the advertisement:
        {text}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",  # You can use "gpt-3.5-turbo" or other chat-based models
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )
        
        # The API will return choices with a "message" field that contains the output
        keywords = response.choices[0].message.content.strip()
        print(f"OpenAi Results: {keywords}")
        # Convert the keywords into a list format by splitting them
        keyword_list = clean_and_extract_keywords(keywords)
        return sorted([keyword.strip().lower() for keyword in keyword_list])
    
    except Exception as e:
        print(f"Error during keyword extraction: {e}")
        return []
   
     
def generate_random_string(length=12):
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(secrets.choice(characters) for _ in range(length))


# ✅ **Extract Keywords from Video (Frames + Audio)**
def extract_keywords_from_video(mp4_path):
    """Extracts frames and audio from video, transcribes text, and extracts keywords."""
    
    print(f"Processing video: {mp4_path}")

    # **Extract Frames and Analyze**

    # **Extract Audio and Transcribe**
    audio_file_path = extract_audio_from_mp4(mp4_path, "extracted_audio.wav")
    transcription = transcribe_audio(audio_file_path)

    if transcription:
        print(f"Transcription Result: {transcription}")
        text_keywords = extract_keywords_from_text(transcription)
        print(f"=====Extracted Keywords from Audio: {text_keywords}")
    else:
        text_keywords = ""
        
    frame_keywords = extract_keywords_from_frames(mp4_path)
    print(f"=====Extracted Keywords from Frames: {frame_keywords}")


    # **Combine Keywords from Text & Images**
    final_keywords = set(frame_keywords + text_keywords.split(","))
    print("=====Final Extracted Keywords: ",",".join(final_keywords))

    # **Cleanup**
    os.remove("extracted_audio.wav")

    return final_keywords

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
# The code snippet `if __name__ == "__main__":` is a common Python idiom that
# allows a script to be executed as the main program only if it is run directly,
# not when it is imported as a module in another script.
# if __name__ == "__main__":
#     transcribed_text = transcribe_audio("../audio1378004054.m4a")
#     print(f"Transcribed Text: {transcribed_text}")

import cv2
import numpy as np
from PIL import Image

def preprocess_image(photo_url):
    image_file_path = "downloaded_image"
    image_file_path = download_video_from_url(photo_url, image_file_path)

    if not image_file_path:
        print("Image download failed.")
        return

    image = cv2.imread(image_file_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    print("image:", image)
    _, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)  # Convert to black & white
    print("binary_img:", binary_image)
    return binary_image

import pytesseract

def extract_text(photo_url):
    preprocessed_img = preprocess_image(photo_url)
    print("preprocessed_img:", preprocessed_img)
    text = pytesseract.image_to_string(preprocessed_img)
    return text

def filter_relevant_words(text, keywords):
    words = text.lower().split()
    relevant_words = [word for word in words if word in keywords]
    return relevant_words

def extract_keywords_from_picture(photo_url):
    """Processes an image, extracts text, and filters relevant words."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Give me a comma-separated string of keywords extracted from this image. Output that and nothing else."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": photo_url
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    keywords = response.choices[0].message.content
    print(response.choices[0].message.content)
    return keywords.split(", ")

    
if __name__ == "__main__":
    video_path = "/Users/jamie_chen/Desktop/tartan-hacks/tartan-hacks-2025/backend/ffmpeg/cola.mp4"  # Replace with your video file path
    keywords = extract_keywords_from_video(video_path)
    print("\n🚀 **Final Keywords:**", keywords)
