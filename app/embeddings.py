# import openai
# import anthropic
# import numpy as np
# import time
# import os

# from flask import current_app
# from dotenv import load_dotenv

# load_dotenv()
# os.environ["ANTHROPIC_API_KEY"] = os.getenv("OPENAI_API_KEY")

# # Function to generate an embedding for the given text using OpenAI's API.
# def generate_embedding(text: str, max_retries: int = 3, delay: int = 2) -> np.ndarray:
#     client = anthropic.Anthropic(
#       api_key=os.environ["ANTHROPIC_API_KEY"]
#     )

#     for attempt in range(max_retries):
#         try:
#             response = client.embeddings.create(
#                 input=text,
#                 model="claude-3-opus-20240229"
#             )
#             return np.array(response["data"][0]["embedding"])
#         except Exception as e:
#             current_app.logger.error(f"An error occurred: {e}. Retrying {attempt + 1}/{max_retries}...")
#             time.sleep(delay)
#     raise RuntimeError("Failed to generate embedding after multiple attempts.")


import torch
import numpy as np
import time
import os

from transformers import AutoTokenizer, AutoModel
from flask import current_app
from dotenv import load_dotenv

load_dotenv()

# Choose a model suited for generating sentence embeddings.
# "sentence-transformers/all-MiniLM-L6-v2" is a popular and efficient option.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Load the tokenizer and model once at module level for efficiency.
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

def generate_embedding(text: str, max_retries: int = 3, delay: int = 2) -> np.ndarray:
    """
    Generates an embedding for the given text using a Hugging Face transformer model.
    
    Args:
        text (str): The input text to embed.
        max_retries (int): Maximum number of attempts if an error occurs.
        delay (int): Seconds to wait between retry attempts.
    
    Returns:
        np.ndarray: The generated embedding as a NumPy array.
        
    Raises:
        RuntimeError: If the embedding cannot be generated after max_retries.
    """
    for attempt in range(max_retries):
        try:
            # Tokenize the input text with truncation.
            inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            # Move inputs to the same device as the model.
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model(**inputs)
            
            # Extract token embeddings (last hidden state).
            token_embeddings = outputs.last_hidden_state  # Shape: (batch_size, sequence_length, hidden_size)
            
            # Perform mean pooling to get a single vector for the sentence.
            attention_mask = inputs["attention_mask"].unsqueeze(-1)  # Shape: (batch_size, sequence_length, 1)
            masked_embeddings = token_embeddings * attention_mask.float()
            summed = torch.sum(masked_embeddings, dim=1)
            summed_mask = torch.clamp(attention_mask.sum(dim=1), min=1e-9)
            mean_embedding = summed / summed_mask
            
            # Return the embedding as a 1D NumPy array.
            return mean_embedding.squeeze(0).cpu().numpy()
        
        except Exception as e:
            current_app.logger.error(f"An error occurred: {e}. Retrying {attempt + 1}/{max_retries}...")
            time.sleep(delay)
    
    raise RuntimeError("Failed to generate embedding after multiple attempts.")