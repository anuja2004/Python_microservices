from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("AIzaSyBI170vlVKhHS7SGmngHi-neBAH2g3ccs4")

if not GEMINI_API_KEY:
    raise RuntimeError("❌ Missing Gemini API Key in .env!")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Initialize FastAPI app
app = FastAPI(title="Chatbot Microservice")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chatbot(request: ChatRequest):
    """Handles user queries and returns AI response."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([request.message])
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
