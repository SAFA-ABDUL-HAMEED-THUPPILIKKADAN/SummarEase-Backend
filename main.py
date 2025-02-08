import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import chardet


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


# @app.post("/summarize/")
# async def summarize_text(request: TextRequest):
#     try:
#         model = genai.GenerativeModel("gemini-pro")
#         response = model.generate_content(request.text)
#         return {"summary": response.text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/summarize/")
# async def summarize_file(file: UploadFile = File(...)):
#     try:
#         # Read the file content
#         content = await file.read()
#         text = content.decode("utf-8")  # Decode assuming it's a text file

#         # Generate summary using Gemini AI
#         model = genai.GenerativeModel("gemini-pro")
#         response = model.generate_content(text)

#         return {"summary": response.text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize/")
async def summarize_file(file: UploadFile = File(...)):
    try:
        content = await file.read()

        # Detect file encoding
        detected_encoding = chardet.detect(content)['encoding']
        if not detected_encoding:
            detected_encoding = "utf-8"  # Fallback to UTF-8

        # Decode using detected encoding
        # Ignore undecodable characters
        text = content.decode(detected_encoding, errors="ignore")

        # Generate summary using Gemini AI
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(text)

        return {"summary": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
