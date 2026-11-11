#!/usr/bin/env python3
"""Validate SVG XML, viewBoxes, IDs, and local README references."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
files = ["hero.svg", "about-life.svg", "stack.svg", "id-dashboard.svg", "connect.svg"]
ok = True
for name in files:
    path = root / name
    try:
        tree = ET.parse(path)
        view_box = tree.getroot().get("viewBox", "")
        if len(view_box.split()) != 4:
            raise ValueError("viewBox must have four values")
        ids = re.findall(r'\bid="([^"]+)"', path.read_text(encoding="utf-8"))
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate IDs")
        print("PASS", name)
    except Exception as exc:
        ok = False
        print("FAIL", name, exc)

readme = (root / "README.md").read_text(encoding="utf-8")
for ref in re.findall(r"\]\(\./([^?)]+)", readme):
    if ref.startswith("profile-3d-contrib/"):
        continue
    if not (root / ref).exists():
        ok = False
        print("FAIL README reference", ref)
print("PASS README references" if ok else "FAIL README references")
sys.exit(0 if ok else 1)
