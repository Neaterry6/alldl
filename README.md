# AllDownloader API

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/alldownloader

A simple, universal media downloader API and web app. Paste a URL from YouTube, TikTok, Instagram, Twitter/X, and more—get the video/image/audio download instantly. Built with Python (FastAPI + yt-dlp) for the backend and a clean Tailwind-styled frontend.

- **API Endpoint**: `POST /download` – Returns the media file as a stream.
- **Website**: Simple form at root `/` for easy browser use.
- **Supported Sites**: 1000+ via yt-dlp (e.g., YouTube, Vimeo, TikTok, Instagram Reels/Stories, Facebook, Twitter videos).
- **Features**: Serverless-friendly, CORS-enabled, temp file cleanup, error handling.
- **Limits**: Downloads capped at 720p for speed; Vercel hobby timeout ~10s (fine for short clips).

## Quick Start

### Local Development
1. Clone or create the project:
   ```
   git clone <your-repo> alldownloader
   cd alldownloader
   ```
   
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run locally:
   ```
   vercel dev  # Or: uvicorn api.index:app --reload
   ```
   - Visit `http://localhost:3000` for the web form.
   - Test API: `curl -X POST "http://localhost:3000/download" -H "Content-Type: application/json" -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' --output rickroll.mp4`

### Deployment on Vercel (Recommended)
1. Push to GitHub.
2. Go to [vercel.com](https://vercel.com), import your repo.
3. Deploy – auto-detects Python/FastAPI. Live in seconds!
   - Website: `https://your-project.vercel.app`
   - API: `https://your-project.vercel.app/download`

Free tier works great; monitor bandwidth if scaling.

## Project Structure
```
alldownloader/
├── api/
│   └── index.py          # FastAPI backend (download logic)
├── public/
│   └── index.html        # Frontend: All-in-one HTML/JS/Tailwind
├── requirements.txt      # Python deps: fastapi, yt-dlp
├── vercel.json           # Optional: CORS/routing config
└── README.md             # This file
```

## How It Works
- **Backend (`api/index.py`)**: Validates URL, uses yt-dlp to extract/download media, serves as FileResponse. Cleans up temp files in `/tmp`.
- **Frontend (`public/index.html`)**: Tailwind-styled form. Submits URL via Fetch to `/download`, auto-triggers download on success.
- **Key Configs**:
  - yt-dlp: `'format': 'best[height<=720]'` for quick downloads.
  - CORS: Enabled for `*` (restrict in prod).
  - Temp Handling: Uses Vercel's `/tmp` dir; auto-delete after serve.

## API Reference
### `POST /download`
- **Body**: `{ "url": "https://example.com/video" }`
- **Response**: Binary file stream (e.g., MP4) with `Content-Disposition: attachment`.
- **Errors**: JSON `{ "detail": "Error message" }` (400/404/500).
- **Health**: `GET /health` → `{ "status": "healthy" }`

Example (Node.js):
```js
const response = await fetch('https://your-project.vercel.app/download', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: 'https://youtube.com/watch?v=...' })
});
const buffer = await response.arrayBuffer();
// Save buffer to file
```

## Customization
- **Add Auth**: Use FastAPI's `Depends` for API keys (e.g., via header `X-API-Key`).
- **Formats**: Tweak yt-dlp opts (e.g., `'format': 'bestaudio'` for audio-only).
- **Long Downloads**: For >10s videos, add async queue (Celery + Redis) or offload to a VPS.
- **More Sites**: yt-dlp auto-updates; run `pip install --upgrade yt-dlp` periodically.
- **Frontend Tweaks**: Edit Tailwind classes in `<script>` config. For advanced UI, add Next.js.

## Limitations & Legal
- **Timeouts/Bandwidth**: Vercel hobby: 10s exec, 100GB/month outbound. Upgrade for more.
- **ToS Compliance**: Respect platform terms (e.g., no bulk scraping). This is for personal use.
- **yt-dlp**: May break if sites change; check [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp) for updates.
- **Proxies**: For IP bans on heavy use, add `--proxy` to ydl_opts.

## Troubleshooting
- **Download Fails**: Check URL format; test with `yt-dlp <url>` locally.
- **CORS Errors**: Verify `vercel.json` headers.
- **Build Errors**: Ensure Python 3.12 in Vercel settings.
- Logs: Vercel dashboard > Functions > Logs.

## Contributing
Fork, PR, or open issues! Ideas: Add thumbnails, format selector, or S3 upload.

## License
MIT – Do what you want, but don't blame me if YouTube sues. 😎

Built with ❤️ using FastAPI, yt-dlp, Tailwind, and Vercel. Questions? Pialldownloaderer
