#!/usr/bin/env python3
"""Check optional hero media without requiring a runtime server."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
video = root / "assets" / "wave.mp4"
print("wave.mp4 present:", video.exists())
print("ffmpeg available:", bool(shutil.which("ffmpeg")))
print("hero.svg keeps its SVG portrait fallback until media is supplied.")
