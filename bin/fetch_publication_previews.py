#!/usr/bin/env python3
"""
Optional helper: fetch og:image URLs from paper links in papers.bib and save
normalized PNGs to assets/img/publication_preview/.

Usage:
  python3 bin/fetch_publication_previews.py [--dry-run]

Requires: requests (pip install requests). ImageMagick `convert` optional for resize.
Does not edit papers.bib — add preview={filename.png} manually after review.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print("Install requests: pip install requests", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "_bibliography" / "papers.bib"
OUT = ROOT / "assets" / "img" / "publication_preview"
PREVIEW_SIZE = "400x280"


def parse_bib(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    entries = []
    blocks = re.split(r"\n(?=@\w+\{)", text)
    for block in blocks:
        m = re.match(r"@\w+\{([^,]+),", block)
        if not m:
            continue
        key = m.group(1).strip()
        if "preview=" in block:
            continue
        url = None
        for field in ("html", "pdf", "eprint"):
            fm = re.search(rf"{field}\s*=\s*\{{([^}}]+)\}}", block)
            if fm:
                url = fm.group(1).strip()
                break
        if url and not url.startswith("http"):
            if field == "eprint":
                url = f"https://arxiv.org/abs/{url}"
        if url:
            entries.append({"key": key, "url": url})
    return entries


def og_image(url: str, session: requests.Session) -> str | None:
    try:
        r = session.get(url, timeout=20, headers={"User-Agent": "ai-folio-preview-fetch"})
        r.raise_for_status()
    except requests.RequestException:
        return None
    for pat in (
        r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)',
        r'<meta\s+content=["\']([^"\']+)["\']\s+property=["\']og:image',
    ):
        m = re.search(pat, r.text, re.I)
        if m:
            return urljoin(url, m.group(1))
    return None


def resize(src: Path, dest: Path) -> None:
    subprocess.run(
        ["convert", str(src), "-resize", PREVIEW_SIZE + "^", "-gravity", "center", "-extent", PREVIEW_SIZE, str(dest)],
        check=False,
        capture_output=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    for entry in parse_bib(BIB):
        img_url = og_image(entry["url"], session)
        out = OUT / f"{entry['key']}.png"
        print(f"{entry['key']}: {img_url or 'no og:image'} -> {out.name}")
        if args.dry_run or not img_url:
            continue
        try:
            data = session.get(img_url, timeout=30).content
            tmp = OUT / f".{entry['key']}.tmp"
            tmp.write_bytes(data)
            if subprocess.run(["which", "convert"], capture_output=True).returncode == 0:
                resize(tmp, out)
                tmp.unlink(missing_ok=True)
            else:
                tmp.rename(out)
        except requests.RequestException as e:
            print(f"  failed: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
