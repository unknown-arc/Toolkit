import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from typing import Optional
import logging
import shutil

from video_summarizer import VideoSummarizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

app = FastAPI(
    title="Video Summarizer App",
    description="Desktop application for summarizing video content",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class SummaryResponse(BaseModel):
    status: str
    summary: str
    duration: str
    processing_time: float
    word_count: int
    transcript: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/summarize", response_model=SummaryResponse)
async def summarize_video(
    file: UploadFile = File(...),
    summary_length: int = 3,
    use_ai: bool = True
):
    """
    Summarize a video from file upload
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload MP4, AVI, MOV, MKV, or WEBM files.")
        
        # Validate file size (100MB limit)
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > 100 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size must be less than 100MB")
        
        summarizer = VideoSummarizer()
        
        # Save uploaded file temporarily
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        try:
            result = summarizer.summarize_video(
                video_path=file_path,
                summary_length=summary_length,
                use_ai=use_ai
            )
            
            return SummaryResponse(
                status="success",
                summary=result["summary"],
                duration=result["duration"],
                processing_time=result["processing_time"],
                word_count=result["word_count"],
                transcript=result.get("transcript", "")
            )
            
        finally:
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

# Run the app directly
if __name__ == "__main__":
    # Disable reload for Electron compatibility
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)