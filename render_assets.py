"""Deterministic profile strip using the established orbit/blackline tokens."""
from pathlib import Path
import argparse
from html import escape

ROOT = Path(__file__).resolve().parent
WORDS = [("CODE", 54), ("DESIGN", 405), ("BUILD", 836)]


def render():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="188" viewBox="0 0 1200 188" role="img" aria-labelledby="title desc">
  <title id="title">Code, design and build</title>
  <desc id="desc">Murathan's selected projects, using the established black, white, blue and orange visual language.</desc>
  <style>
    text{font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;fill:#fff}
    .meta{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:12px;letter-spacing:2px;fill:#aaa}
    .word{font-size:64px;font-weight:300;letter-spacing:8px}
    .flow{stroke-dasharray:3 12;animation:current 6s linear infinite}
    @keyframes current{to{stroke-dashoffset:-60}}
    @media(prefers-reduced-motion:reduce){.flow{animation:none}}
  </style>
  <rect width="1200" height="188" fill="#000"/>
  <path d="M20 44V20H44M1156 20H1180V44M1180 144V168H1156M44 168H20V144" fill="none" stroke="#fff" stroke-opacity=".35"/>
  <text x="54" y="52" class="meta">SELECTED PROJECTS</text>
''' + "".join(f'  <text x="{x}" y="111" class="word">{escape(word)}</text>\n' for word, x in WORDS) + '''  <path d="M54 139H1146" stroke="#fff" stroke-opacity=".16" fill="none"/>
  <path d="M54 139H1146" stroke="#4a8dff" stroke-opacity=".8" class="flow" fill="none"/>
  <circle cx="54" cy="139" r="3" fill="#6fb0ff"/>
  <circle cx="405" cy="139" r="3" fill="#fff"/>
  <circle cx="836" cy="139" r="3" fill="#ff8a1f"/>
</svg>
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "assets/project-strip.svg"
    content = render()
    if args.check:
        if target.read_bytes() != content.encode("utf-8"):
            raise SystemExit("Profile strip is stale; run render_assets.py")
        print("Profile strip matches its deterministic source")
    else:
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(content.encode("utf-8"))
