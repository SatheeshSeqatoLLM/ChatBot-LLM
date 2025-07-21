
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import ollama

# Create the FastAPI app
app = FastAPI()

# Define the request model for type checking
# We can specify a default model to use
class Prompt(BaseModel):
    text: str
    model: str = "gemma:2b"

# --- API Endpoint ---
@app.post("/chat-bot")
def generate(prompt: Prompt):
    """
    Receives a prompt and returns a response from the local Ollama service.
    This is the endpoint you will trigger from Postman.
    """
    try:
        # Forward the request to Ollama
        response = ollama.chat(
            model=prompt.model,
            messages=[{"role": "user", "content": prompt.text}]
        )
        # Return the content of the message from Ollama's response
        return {"response": response["message"]["content"]}
    except Exception as e:
        # Return an error if Ollama is not running or another issue occurs
        return {"error": f"An error occurred with Ollama: {e}"}

# --- Main entry point to run the server ---
if __name__ == "__main__":
    # This makes the server accessible on your local network
    uvicorn.run(app, host="0.0.0.0", port=8000)
