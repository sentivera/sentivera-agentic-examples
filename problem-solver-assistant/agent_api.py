from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

app = FastAPI()

class AgentInput(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_agent(data: AgentInput):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that solves problems step-by-step."},
            {"role": "user", "content": data.prompt}
        ],
        temperature=0.2
    )
    return {"response": response.choices[0].message.content}
