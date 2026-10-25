"""Download and verify the official VOICEVOX Engine Windows release."""

import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

VERSION = "0.26.0"
BASE_URL = f"https://github.com/VOICEVOX/voicevox_engine/releases/download/{VERSION}"
ASSETS = {
    "cuda": [
        (f"voicevox_engine-windows-nvidia-{VERSION}.7z.001", "75110cdaad8b764f0e48197848440c82f3d74bcc48f61672f76f22d3deeb24ff"),
        (f"voicevox_engine-windows-nvidia-{VERSION}.7z.002", "424b0825c35bac1ce102a2ea5c621899989a09d910a97998ec70e97b9691df4a"),
    ],
    "cpu": [
        (f"voicevox_engine-windows-cpu-{VERSION}.7z.001", "8684e1aa6b856c9fb51720552b4f2d5068e094bc3d0b104467dee20b76f99992"),
    ],
}


def detect_edition():
    try:
        result = subprocess.run(["nvidia-smi", "-L"], stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, timeout=5, check=False)
        return "cuda" if result.returncode == 0 else "cpu"
    except (OSError, subprocess.TimeoutExpired):
        return "cpu"


def installed(destination):
    return (destination / "run.exe").is_file() and (destination / "engine_manifest.json").is_file() and (destination / "model").is_dir()


def download(url, destination, expected_hash):
    request = urllib.request.Request(url, headers={"User-Agent": "Supreme-Nihongo-Installer/1.0"})
    digest = hashlib.sha256()
    received = 0
    with urllib.request.urlopen(request, timeout=120) as source, destination.open("wb") as target:
        while True:
            chunk = source.read(1024 * 1024)
            if not chunk:
                break
            target.write(chunk)
            digest.update(chunk)
            received += len(chunk)
            if received % (128 * 1024 * 1024) < len(chunk):
                print(f"  {received / 1024**3:.1f} GiB received", flush=True)
    if digest.hexdigest() != expected_hash:
        raise ValueError(f"SHA-256 mismatch for {destination.name}; installation stopped")
    print(f"Verified SHA-256: {destination.name}", flush=True)


def install(root, edition, base_url=BASE_URL, assets=ASSETS):
    if sys.platform != "win32":
        raise RuntimeError("This installer supports Windows only")
    if edition == "auto":
        edition = detect_edition()
    package_name = "windows-nvidia" if edition == "cuda" else "windows-cpu"
    engine_root = root / "engine"
    destination = engine_root / package_name
    print(f"Selected VOICEVOX edition: {edition}", flush=True)

    if installed(destination):
        print(f"VOICEVOX Engine is already installed at {destination}", flush=True)
        return destination
    if destination.exists():
        raise RuntimeError(f"Incomplete installation at {destination}; move it aside before retrying")

    root.mkdir(parents=True, exist_ok=True)
    required = 11 * 1024**3 if edition == "cuda" else 7 * 1024**3
    free = shutil.disk_usage(root).free
    if free < required:
        raise RuntimeError(f"At least {required // 1024**3} GiB of free disk space is required")

    engine_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".install-", dir=engine_root) as temporary:
        stage = Path(temporary)
        parts = []
        for name, expected_hash in assets[edition]:
            path = stage / name
            print(f"Downloading official VOICEVOX asset: {name}", flush=True)
            download(f"{base_url}/{name}", path, expected_hash)
            parts.append(path)

        archive = stage / "voicevox-engine.7z"
        with archive.open("wb") as combined:
            for part in parts:
                with part.open("rb") as source:
                    shutil.copyfileobj(source, combined, length=1024 * 1024)

        extracted = stage / "extracted"
        extracted.mkdir()
        print("Extracting verified archive...", flush=True)
        subprocess.run(["tar.exe", "-xf", str(archive), "-C", str(extracted)], check=True)
        payload = extracted / package_name
        if not installed(payload):
            raise RuntimeError("The archive does not contain the expected VOICEVOX Engine files")
        payload.rename(destination)
    print(f"VOICEVOX Engine {VERSION} installed at {destination}", flush=True)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--edition", choices=("auto", "cuda", "cpu"), default="auto")
    args = parser.parse_args()
    install(Path(__file__).resolve().parent, args.edition)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Installation failed: {exc}", file=sys.stderr)
        sys.exit(1)
