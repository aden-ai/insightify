from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.chain import run_rag

# Initialize FastAPI app
app = FastAPI(title="Insightify Backend")

# Allow requests from Chrome Extension and local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "chrome-extension://*",  # Chrome extension
        "http://localhost:3000",  # Optional frontend testing
        "http://127.0.0.1:8000",  # Local FastAPI testing
        "*",  # Development convenience — restrict later in prod
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request schema
class TextRequest(BaseModel):
    text: str
    # ✅ FIXED: Added missing 'mode' field
    mode: str = "summary" 

# Simple health check route
@app.get("/")
async def root():
    return {"message": "Insightify backend is running!"}

# Main summarization endpoint
@app.post("/summarize")
async def summarize(
    data: TextRequest,
    authorization: str = Header(None)
):
    # ✅ FIXED: Using settings.backend_api_key for authorization check
    expected_key = settings.backend_api_key
    if authorization != f"Bearer {expected_key}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    text = data.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="No text provided.")

    try:
        # ✅ FIXED: data.mode now exists in the request body
        summary = run_rag(text, data.mode)
        return {"summary": summary}
    except Exception as e:
        # It's good practice to log the full exception here, but for the API response:
        raise HTTPException(status_code=500, detail=f"RAG Chain Error: {str(e)}")