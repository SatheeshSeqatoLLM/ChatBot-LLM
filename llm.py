import requests
import json

# The address of your local FastAPI server
API_SERVER_URL = "http://localhost:8000/chat-bot"

def get_conversational_response(prompt: str) -> str:
    """
    Gets a conversational response by calling the local FastAPI server.
    """
    try:
        # The server will use its default model ('gemma:2b')
        response = requests.post(API_SERVER_URL, json={"text": prompt})
        response.raise_for_status()
        
        data = response.json()
        if "error" in data:
            return f"Error from API server: {data['error']}"
        return data.get("response", "No response text found.")

    except requests.exceptions.RequestException as e:
        return f"Could not connect to the local API server. Is it running? Error: {e}"
    except json.JSONDecodeError:
        return "Error: Failed to decode JSON response from the API server."

def summarize_text(text: str) -> str:
    """Summarize a given text by calling the local FastAPI server."""
    prompt = f"Please summarize the following text in a few concise paragraphs:\n\n{text}"
    return get_conversational_response(prompt)