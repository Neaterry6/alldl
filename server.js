const express = require("express");
const { exec } = require("child_process");
const cors = require("cors");

const app = express();
app.use(cors());

app.get("/api/download", async (req, res) => {
    const videoUrl = req.query.url;

    if (!videoUrl) {
        return res.status(400).json({ error: "Please provide a video URL." });
    }

    try {
        // Run yt-dlp to download the video
        exec(`yt-dlp -f best -o 'downloads/video.mp4' ${videoUrl}`, (error, stdout, stderr) => {
            if (error) {
                console.error("Download error:", stderr);
                return res.status(500).json({ error: "Failed to download video." });
            }
            res.json({ message: "Video downloaded successfully!", path: "downloads/video.mp4" });
        });
    } catch (err) {
        console.error("Server error:", err);
        res.status(500).json({ error: "Internal server error." });
    }
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`Video Downloader API running at http://localhost:${PORT}`))
