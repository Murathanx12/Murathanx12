"""Deterministic profile strip using the established orbit/blackline tokens."""
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parent


def render():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="240" viewBox="0 0 1200 240" role="img" aria-labelledby="title desc">
  <title id="title">Check my portfolio: murathan.info</title>
  <desc id="desc">Visit Murathan's portfolio for engineering projects, robots and design work.</desc>
  <style>
    text{font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;fill:#fff}
    .word{font-size:60px;font-weight:300;letter-spacing:1px}
    .url{font-family:ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',monospace;font-size:44px;letter-spacing:2px;fill:#6fb0ff}
  </style>
  <rect width="1200" height="240" fill="#000"/>
  <path d="M20 48V20H48M1152 20H1180V48M1180 192V220H1152M48 220H20V192" fill="none" stroke="#fff" stroke-opacity=".35"/>
  <text x="64" y="109" class="word">Check my portfolio</text>
  <text x="68" y="169" class="url">murathan.info</text>
  <path d="M68 195H1132" stroke="#fff" stroke-opacity=".16" fill="none"/>
  <path d="M68 195H444" stroke="#4a8dff" stroke-opacity=".8" fill="none"/>
  <circle cx="444" cy="195" r="3" fill="#6fb0ff"/>
  <circle cx="1030" cy="111" r="50" fill="none" stroke="#fff" stroke-opacity=".16"/>
  <path d="M1008 133L1052 89M1018 89H1052V123" stroke="#fff" stroke-width="2" fill="none"/>
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
