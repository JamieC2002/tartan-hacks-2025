import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Set your OpenAI API key
openai.api_key = "ask-proj-jn-QvLD1eVCRlpQ0ZMc0Skb0Wu5O7qblUQNGTNITj7B7arsFCgylsHTiZ8s2y8pcvrI4L0MDm0T3BlbkFJO5O1P190N3h82003aPuk5RbN4QCyGVsTJG9VzMB3O-d7qGOcLotjakNGsxl3IuH710tIk67VQA"

def get_embeddings(text_list):
    """Generate embeddings for a list of strings using OpenAI's API"""
    response = openai.Embedding.create(
        model="text-embedding-ada-002",  # You can also use "text-davinci-003" or other models
        input=text_list
    )
    embeddings = [embedding['embedding'] for embedding in response['data']]
    return embeddings

def calculate_similarity(list1, list2):
    """Calculate the cosine similarity between two lists of strings."""
    # Step 1: Get embeddings for both lists
    embeddings1 = get_embeddings(list1)
    embeddings2 = get_embeddings(list2)
    
    # Step 2: Compute cosine similarity between each pair of embeddings
    cosine_similarities = cosine_similarity(embeddings1, embeddings2)
    
    # Step 3: Calculate average similarity score
    average_similarity = np.mean(cosine_similarities)
    
    # Step 4: Return True if similarity is high (e.g., 0.8 or above), False otherwise
    return average_similarity > 0.8  # Adjust the threshold as needed

# Example usage:

