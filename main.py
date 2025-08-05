from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load your personal profile data
with open("profile_data.txt", "r", encoding="utf-8") as f:
    personal_context = f.read()

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Define FastAPI app
app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

#Request model for incoming JSON
class ChatRequest(BaseModel):
    question: str

#POST endpoint to handle chat questions
@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    question = payload.question
    chat = model.start_chat(history=[])

    prompt = f"""Answer the following question based on Luka's profile:

{personal_context}

Question: {question}
"""

    response = chat.send_message(prompt)
    return {"answer": response.text}
