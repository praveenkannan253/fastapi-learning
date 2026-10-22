from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests


load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

app=FastAPI()

class PromptRequest(BaseModel):
    prompt: str
    tone: str = "neutral"  # extra field for business logic

@app.post("/genai")
def generate_text(request: PromptRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    
    tone_prefix = {
        "friendly": "Respond in a casual and warm tone.",
        "formal": "Respond in a professional and concise tone.",
        "neutral": "Respond neutrally."
    }.get(request.tone.lower(), "Respond neutrally.")
    
    final_prompt = f"{tone_prefix}\n\nUser request: {request.prompt}"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": final_prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    data = response.json()
    generated_text = data["choices"][0]["message"]["content"]

    return {
        "tone_used": request.tone,
        "original_prompt": request.prompt,
        "final_prompt": final_prompt,
        "response": generated_text
    }