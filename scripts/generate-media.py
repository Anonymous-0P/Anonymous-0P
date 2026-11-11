#!/usr/bin/env python3
"""Generate synthetic, valid PNG artwork without third-party dependencies."""
from pathlib import Path
import struct
import zlib

W = H = 512
OUT = Path(__file__).resolve().parents[1] / "assets"


def png(path: Path, pixels: list[list[tuple[int, int, int, int]]]) -> None:
    raw = b"".join(b"\0" + bytes(v for px in row for v in px) for row in pixels)

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    data = b"\x89PNG\r\n\x1a\n"
    data += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0))
    data += chunk(b"IDAT", zlib.compress(raw, 9))
    data += chunk(b"IEND", b"")
    path.write_bytes(data)


def render(kind: str) -> list[list[tuple[int, int, int, int]]]:
    pixels = []
    for y in range(H):
        row = []
        for x in range(W):
            glow = max(0, 1 - (((x - 256) ** 2 + (y - 240) ** 2) ** 0.5) / 420)
            r = int(13 + 36 * glow)
            g = int(14 + 24 * glow)
            b = int(22 + 72 * glow)
            if kind == "pointing":
                r += int(18 * max(0, 1 - abs(x - 330) / 180))
            row.append((min(r, 255), min(g, 255), min(b, 255), 255))
        pixels.append(row)

    def rect(x0, y0, x1, y1, color):
        for y in range(max(0, y0), min(H, y1)):
            for x in range(max(0, x0), min(W, x1)):
                pixels[y][x] = color

    def circle(cx, cy, radius, color):
        rr = radius * radius
        for y in range(max(0, cy - radius), min(H, cy + radius)):
            for x in range(max(0, cx - radius), min(W, cx + radius)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= rr:
                    pixels[y][x] = color

    circle(256, 236, 142, (32, 33, 56, 255))
    circle(256, 205, 58, (167, 139, 250, 255))
    rect(160, 280, 352, 410, (34, 211, 238, 255))
    if kind == "pointing":
        rect(350, 260, 440, 286, (244, 114, 182, 255))
        circle(444, 273, 17, (244, 114, 182, 255))
    circle(256, 236, 144, (34, 211, 238, 255))
    circle(256, 236, 140, (21, 22, 39, 255))
    return pixels


for name, kind in (("portrait.png", "portrait"), ("pointing.png", "pointing")):
    png(OUT / name, render(kind))
    print("generated", OUT / name)
