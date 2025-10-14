from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
import yt_dlp
import os
import tempfile
from pathlib import Path

app = FastAPI(title="AllDownloader")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In prod, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = Path("/tmp")  # Vercel's writable temp dir
TEMP_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def root():
    # Serve static HTML from public/ (Vercel handles this automatically, but fallback)
    with open("public/index.html", "r") as f:
        return f.read()

@app.post("/download")
async def download_media(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    # yt-dlp options: best quality, no playlist, quick for serverless
    ydl_opts = {
        'format': 'best[height<=720]',  # Limit to 720p for speed
        'outtmpl': str(TEMP_DIR / '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,  # Reduce logs
    }
    
    filename = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info first
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            
            # Download (may take 5-10s; watch Vercel timeout)
            ydl.download([url])
            
            if os.path.exists(filename):
                return FileResponse(
                    path=filename,
                    filename=Path(filename).name,
                    media_type='application/octet-stream',
                    headers={'Content-Disposition': f'attachment; filename="{Path(filename).name}"'}
                )
            else:
                raise HTTPException(status_code=404, detail="Download failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        # Clean up temp file immediately (serverless is stateless)
        if filename and os.path.exists(filename):
            os.remove(filename)

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy"}
