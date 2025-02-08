import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing from the .env file")

genai.configure(api_key=API_KEY)

# FastAPI instance
app = FastAPI()

# Request model

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods, including OPTIONS
    allow_headers=["*"],  # Allow all headers
)


class TextRequest(BaseModel):
    text: str


@app.post("/summarize/")
async def summarize_text(request: TextRequest):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(request.text)
        return {"summary": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
