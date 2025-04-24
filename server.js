const express = require("express");
const { exec } = require("child_process");
const cors = require("cors");
const fs = require("fs");

const app = express();
app.use(cors());

app.get("/api/download", async (req, res) => {
    const videoUrl = req.query.url;
    const filePath = "video.mp4";

    if (!videoUrl) {
        return res.status(400).json({ error: "Please provide a video URL." });
    }

    try {
        // Download video
        exec(`yt-dlp -f best -o '${filePath}' ${videoUrl}`, (error, stdout, stderr) => {
            if (error) {
                console.error("Download error:", stderr);
                return res.status(500).json({ error: "Failed to download video." });
            }

            // Stream video back to user
            res.download(filePath, (err) => {
                if (err) {
                    console.error("Error sending file:", err);
                    res.status(500).json({ error: "Failed to send video file." });
                }
                // Delete file after sending to avoid storage issues
                fs.unlinkSync(filePath);
            });
        });
    } catch (err) {
        console.error("Server error:", err);
        res.status(500).json({ error: "Internal server error." });
    }
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`Video Downloader API running at http://localhost:${PORT}`));
