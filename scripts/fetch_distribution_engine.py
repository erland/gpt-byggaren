#!/usr/bin/env python3
"""Fetch the original GPT Byggaren engine from a public GitHub Release.

First try the installed plugin version, then latest ONLY if that release or
asset is absent. Never silently substitute a different implementation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import urllib.error
import urllib.request
import zipfile

REPO = "erland/gpt-byggaren"
ASSET = "distribution-engine.zip"
API = f"https://api.github.com/repos/{REPO}/releases"
MAX_SIZE = 30 * 1024 * 1024

class MissingReleaseOrAsset(Exception):
    pass

def get_json(url):
    req = urllib.request.Request(url, headers={"Accept":"application/vnd.github+json",
                                               "User-Agent":"gpt-byggaren-engine-resolver"})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise MissingReleaseOrAsset(url) from exc
        raise

def fetch_metadata(version):
    tag = "v" + version.removeprefix("v")
    info = get_json(f"{API}/tags/{tag}")
    asset = next((a for a in info.get("assets", []) if a.get("name") == ASSET), None)
    if asset is None:
        raise MissingReleaseOrAsset(f"{tag} has no {ASSET}")
    return info, asset

def safe_unpack(archive, target):
    with zipfile.ZipFile(archive) as zf:
        for member in zf.infolist():
            path = Path(member.filename)
            if path.is_absolute() or ".." in path.parts or member.is_dir() and not path.parts:
                raise ValueError("Unsafe ZIP path")
            if (member.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("ZIP symlink is forbidden")
        zf.extractall(target)
    required = ["scripts/build_distributions.py", "scripts/install_distribution_engine.py",
                "scripts/lib/project_model.py", "templates"]
    if any(not (target / name).exists() for name in required):
        raise ValueError("Downloaded archive lacks required canonical engine files")

def install(version, destination):
    if not version or not version.strip():
        raise ValueError("Plugin version is required; never infer a mutable version")
    try:
        release, asset = fetch_metadata(version)
        selection = "matching"
    except MissingReleaseOrAsset:
        release = get_json(f"{API}/latest")
        asset = next((a for a in release.get("assets", []) if a.get("name") == ASSET), None)
        if asset is None:
            raise MissingReleaseOrAsset("Latest release also lacks distribution-engine.zip")
        selection = "latest-fallback"
    digest = asset.get("digest", "")
    if not digest.startswith("sha256:") or len(digest) != 71:
        raise ValueError("Release asset has no SHA-256 digest")
    url = asset["browser_download_url"]
    prefix = f"https://github.com/{REPO}/releases/download/"
    if not url.startswith(prefix) or not url.endswith("/" + ASSET):
        raise ValueError("Unexpected GitHub release asset URL")
    req = urllib.request.Request(url, headers={"User-Agent":"gpt-byggaren-engine-resolver"})
    archive = destination.parent / (destination.name + ".download.zip")
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        total = 0
        hasher = hashlib.sha256()
        with urllib.request.urlopen(req, timeout=40) as response, archive.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_SIZE:
                    raise ValueError("Engine exceeds size limit")
                hasher.update(chunk)
                output.write(chunk)
        if hasher.hexdigest() != digest.removeprefix("sha256:"):
            raise ValueError("Release asset SHA-256 mismatch")
        if destination.exists():
            raise FileExistsError(f"Destination already exists: {destination}")
        destination.mkdir()
        try:
            safe_unpack(archive, destination)
        except Exception:
            shutil.rmtree(destination)
            raise
    finally:
        archive.unlink(missing_ok=True)
    return {"selected": selection, "tag": release["tag_name"], "sha256": hasher.hexdigest()}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-version", required=True, help="Version from installed plugin VERSION or plugin.json")
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(install(args.plugin_version, args.destination), indent=2))

if __name__ == "__main__":
    main()
