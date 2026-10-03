import os
import json
from pathlib import Path

DATA_FILE = Path("profile_views.json")
SVG_FILE = Path("profile-views.svg")

# Load current count
if DATA_FILE.exists():
    try:
        data = json.loads(DATA_FILE.read_text())
        views = int(data.get("views", 0))
    except Exception:
        views = 0
else:
    views = 0

# Increase count
views += 1

# Save count
DATA_FILE.write_text(
    json.dumps({"views": views}, indent=2)
)

# Stylish SVG
svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="420"
height="120"
viewBox="0 0 420 120">

<defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0d1117"/>
        <stop offset="100%" stop-color="#111827"/>
    </linearGradient>

    <linearGradient id="cyan" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00D9FF"/>
        <stop offset="100%" stop-color="#38BDF8"/>
    </linearGradient>

    <filter id="glow">
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feMerge>
            <feMergeNode in="blur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
</defs>

<rect
    x="2"
    y="2"
    width="416"
    height="116"
    rx="18"
    fill="url(#bg)"
    stroke="#00D9FF"
    stroke-opacity="0.35"
    stroke-width="2"
/>

<circle
    cx="55"
    cy="60"
    r="25"
    fill="#00D9FF"
    fill-opacity="0.08"
    stroke="#00D9FF"
    stroke-opacity="0.5"
    stroke-width="1.5"
/>

<text
    x="55"
    y="68"
    text-anchor="middle"
    font-family="Arial, sans-serif"
    font-size="25"
    fill="#00D9FF"
    filter="url(#glow)"
>◉</text>

<text
    x="95"
    y="45"
    font-family="Arial, sans-serif"
    font-size="12"
    font-weight="600"
    letter-spacing="2"
    fill="#8B949E"
>PROFILE VISITORS</text>

<text
    x="95"
    y="78"
    font-family="Arial, sans-serif"
    font-size="26"
    font-weight="700"
    fill="url(#cyan)"
>{views:,}</text>

<text
    x="95"
    y="98"
    font-family="Arial, sans-serif"
    font-size="10"
    fill="#6E7681"
>THANKS FOR VISITING 🚀</text>

</svg>
'''

SVG_FILE.write_text(svg, encoding="utf-8")

print(f"Profile views: {views}")
