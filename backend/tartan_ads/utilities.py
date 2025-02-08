import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# returns embedding vector of a string
# helper function used in calc similarity
def get_embedding(text):
    """Generate an embedding for a single string using OpenAI's API."""
    response = openai.embeddings.create(
        model="text-embedding-ada-002",  # Specify a valid embedding model
        input=text
    )
    # Extract the first and only embedding from the response
    embedding = response.data[0].embedding
    return embedding


# PARAM: 2 lists of strings (keywords)
# RETURN: single value outlining similarity
def calculate_similarity(text_list_1, text_list_2):
    """Calculate the cosine similarity between two concatenated strings from two lists of strings."""
    if not text_list_1 or not text_list_2:
        print("One or both of the text lists are empty.")
        return None

    # Concatenate each list into a single string
    concatenated_text_1 = " ".join(text_list_1)
    concatenated_text_2 = " ".join(text_list_2)

    # Step 1: Get embeddings for both concatenated strings
    embedding_1 = get_embedding(concatenated_text_1)
    embedding_2 = get_embedding(concatenated_text_2)

    # Check if embeddings were successfully retrieved
    if not embedding_1 or not embedding_2:
        print("Failed to retrieve embeddings.")
        return None

    # Step 2: Compute cosine similarity between the two embeddings
    similarity_score = cosine_similarity([embedding_1], [embedding_2])[0][0]

    # Step 3: Return the cosine similarity score
    return similarity_score
