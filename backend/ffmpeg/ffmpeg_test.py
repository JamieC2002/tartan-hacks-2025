import base64
import openai
import glob
import os

# Load OpenAI API key from environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]
client = openai.OpenAI()

# Function to encode an image in Base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Path to the directory containing frames
FRAME_DIR = "/Users/jamie_chen/Desktop/tartan-hacks/tartan-hacks-2025/backend/ffmpeg/skippy_frames/"
frames = sorted(glob.glob(os.path.join(FRAME_DIR, "*.jpg")))  # Get all JPG frames

ad_frames = "cola_frames"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRAME_DIR = os.path.join(BASE_DIR, f"{ad_frames}")
print(f"BASE_DIR: {BASE_DIR}")
print(f"FRAME_DIR: {FRAME_DIR}")

frames = sorted(glob.glob(os.path.join(FRAME_DIR, "*.jpg")))
print(f"# of Frames: {len(frames)}")

# Generate Base64 strings for all frames
image_list = [
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(frame)}"}}
    for frame in frames
]

prompt = f"""
        ### Task:
        You are given a snapshots of a video, represented by frames.
        Your goal is to extract **only the most relevant, precise, and meaningful keywords** that accurately represent the advertisement's content.

        ### Instructions:

        1. **Understand the Advertisement:**  
        - Analyze the given to identify the key topics, themes, and core messages.

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

        ### Example Output (Extracted Keywords) (Do Not Change Format):  
        EcoClean,dishwasher,water-saving,cleaning,spotless,environmentally,technology
        
        Additional Requirements:
        -  Return at least 5 but no more than 10 keywords.
        -  Ensure all extracted keywords are directly relevant to the product, service, or theme of the ad.
        """
        
# Make the OpenAI request with all images
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

# Print the response
print("\n📜 Description:\n", response.choices[0].message.content)
