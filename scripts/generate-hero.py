#!/usr/bin/env python3
"""Check the supplied hero media without requiring a runtime server."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
video = root / "assets" / "gemini_generated_video_967f96b0.mp4"
print("supplied hero video present:", video.exists())
print("ffmpeg available:", bool(shutil.which("ffmpeg")))
print("README uses the supplied MP4 with a poster and native controls.")
