"""Generate Japanese WAV audio with the local VOICEVOX engine."""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "http://127.0.0.1:50021"


def request(path, data=None, content_type=None):
    headers = {}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(BASE + path, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=180) as response:
        return response.read()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Generate Japanese speech using VOICEVOX")
    parser.add_argument("text", nargs="?", help="Japanese text to speak")
    parser.add_argument("--speaker", type=int, default=3, help="VOICEVOX style ID")
    parser.add_argument("--output", default="voicevox/output.wav", help="WAV output path")
    parser.add_argument("--list-voices", action="store_true", help="List available speakers and styles")
    args = parser.parse_args()

    if args.list_voices:
        for speaker in json.loads(request("/speakers")):
            for style in speaker["styles"]:
                print(f"{style['id']:4}  {speaker['name']} / {style['name']}")
        return
    if not args.text:
        parser.error("provide Japanese text or --list-voices")

    started = time.perf_counter()
    query_path = "/audio_query?" + urllib.parse.urlencode(
        {"text": args.text, "speaker": args.speaker}
    )
    query = request(query_path, data=b"")
    wav = request(
        "/synthesis?" + urllib.parse.urlencode({"speaker": args.speaker}),
        data=query,
        content_type="application/json",
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(wav)
    print(f"Saved {output} ({len(args.text)} characters, {time.perf_counter() - started:.2f} s)")


if __name__ == "__main__":
    main()
