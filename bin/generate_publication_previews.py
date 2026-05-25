#!/usr/bin/env python3
"""
Generate publication thumbnails for al-folio (preview={...} in papers.bib).

Tries, in order:
  1. PDF first page (arxiv / pdf= / eprint=) via pdftoppm or Ghostscript
  2. PDF page 2 if page 1 looks mostly blank
  3. Largest embedded figure on pages 1–2 (PyMuPDF), if installed
  4. Open Graph image from html= / abs page

Usage:
  python3 bin/generate_publication_previews.py [--dry-run] [--force] [--update-bib]
  python3 bin/generate_publication_previews.py --keys bonev2025fourcastnet3

Requires: network for downloads. For PDF rendering, one of:
  pdftoppm (poppler-utils), or gs (ghostscript).
Optional: pip install pymupdf requests
Image resize: ImageMagick `convert` or `magick` (optional; copies raw PNG if missing).

Runs automatically in GitHub Actions before `jekyll build` (see .github/workflows/deploy.yml).
Locally: `python3 bin/generate_publication_previews.py`
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "_bibliography" / "papers.bib"
OUT = ROOT / "assets" / "img" / "publication_preview"
MANIFEST = ROOT / "_data" / "generated_previews.yml"
PREVIEW_SIZE = "400x280"
UA = "ai-folio-preview-generator/1.0"


def _http_get(url: str, timeout: int = 60) -> bytes:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _http_get_text(url: str, timeout: int = 20) -> str:
    return _http_get(url, timeout=timeout).decode("utf-8", errors="replace")


def _which(cmd: str) -> str | None:
    return shutil.which(cmd)


def _convert_cmd() -> list[str] | None:
    for cmd in ("magick", "convert"):
        if _which(cmd):
            return [cmd]
    return None


def resize_png(src: Path, dest: Path) -> None:
    conv = _convert_cmd()
    if not conv:
        shutil.copy2(src, dest)
        return
    subprocess.run(
        [
            *conv,
            str(src),
            "-resize",
            f"{PREVIEW_SIZE}^",
            "-gravity",
            "center",
            "-extent",
            PREVIEW_SIZE,
            str(dest),
        ],
        check=True,
        capture_output=True,
    )


def parse_field(block: str, name: str) -> str | None:
    m = re.search(rf"{name}\s*=\s*\{{([^}}]+)\}}", block)
    return m.group(1).strip() if m else None


def arxiv_id_from_block(block: str) -> str | None:
    eprint = parse_field(block, "eprint")
    if eprint:
        return eprint.split("v")[0]
    note = parse_field(block, "note") or ""
    m = re.search(r"arXiv[:\s]+([\d.]+)", note, re.I)
    return m.group(1) if m else None


def resolve_urls(block: str) -> dict[str, str | None]:
    pdf = parse_field(block, "pdf")
    html = parse_field(block, "html")
    aid = arxiv_id_from_block(block)

    if aid:
        arxiv_pdf = f"https://arxiv.org/pdf/{aid}.pdf"
        arxiv_abs = f"https://arxiv.org/abs/{aid}"
        if not pdf or "arxiv.org" in pdf:
            pdf = arxiv_pdf
        if not html:
            html = arxiv_abs

    if pdf and pdf.startswith("/"):
        pdf = None
    if pdf and not pdf.startswith("http"):
        pdf = None

    if html and "arxiv.org/abs/" in html and not pdf:
        aid2 = html.rstrip("/").split("/")[-1].split("v")[0]
        pdf = f"https://arxiv.org/pdf/{aid2}.pdf"

    return {"pdf": pdf, "html": html}


def parse_bib(path: Path, only_missing: bool, keys: set[str] | None) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    entries = []
    for block in re.split(r"\n(?=@\w+\{)", text):
        m = re.match(r"@\w+\{([^,]+),", block)
        if not m:
            continue
        key = m.group(1).strip()
        if keys and key not in keys:
            continue
        custom = parse_field(block, "preview")
        if custom and custom != f"{key}.png":
            continue
        out_png = OUT / f"{key}.png"
        if only_missing and out_png.is_file():
            continue
        urls = resolve_urls(block)
        if not urls["pdf"] and not urls["html"]:
            continue
        entries.append({"key": key, "block": block, **urls})
    return entries


def write_manifest() -> None:
    keys = sorted(p.stem for p in OUT.glob("*.png") if not p.name.startswith("."))
    MANIFEST.write_text(
        "# Updated by bin/generate_publication_previews.py\nkeys:\n"
        + "".join(f"  - {k}\n" for k in keys),
        encoding="utf-8",
    )
    print(f"Manifest: {len(keys)} previews in {MANIFEST.relative_to(ROOT)}")


def og_image(page_url: str) -> str | None:
    try:
        html = _http_get_text(page_url)
    except OSError:
        return None
    for pat in (
        r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)',
        r'<meta\s+content=["\']([^"\']+)["\']\s+property=["\']og:image',
        r'<meta\s+name=["\']twitter:image["\']\s+content=["\']([^"\']+)',
    ):
        m = re.search(pat, html, re.I)
        if m:
            return urljoin(page_url, m.group(1))
    return None


def download_pdf(url: str, dest: Path) -> bool:
    try:
        data = _http_get(url, timeout=120)
    except OSError as e:
        print(f"    pdf download failed: {e}", file=sys.stderr)
        return False
    if not data.startswith(b"%PDF"):
        print("    response is not a PDF", file=sys.stderr)
        return False
    dest.write_bytes(data)
    return True


def render_pdf_page(pdf: Path, page: int, out_png: Path) -> bool:
    """Render one PDF page to PNG using pdftoppm or ghostscript."""
    if _which("pdftoppm"):
        prefix = out_png.with_suffix("")
        r = subprocess.run(
            [
                "pdftoppm",
                "-png",
                "-f",
                str(page),
                "-l",
                str(page),
                "-r",
                "150",
                str(pdf),
                str(prefix),
            ],
            capture_output=True,
        )
        if r.returncode != 0:
            return False
        # pdftoppm names: prefix-1.png or prefix-01.png depending on version
        candidates = sorted(prefix.parent.glob(prefix.name + "*.png"))
        if not candidates:
            return False
        shutil.move(candidates[0], out_png)
        for c in candidates[1:]:
            c.unlink(missing_ok=True)
        return True

    gs = _which("gs")
    if gs:
        r = subprocess.run(
            [
                gs,
                "-dNOPAUSE",
                "-dBATCH",
                "-dSAFER",
                "-sDEVICE=png16m",
                f"-dFirstPage={page}",
                f"-dLastPage={page}",
                "-r150",
                f"-sOutputFile={out_png}",
                str(pdf),
            ],
            capture_output=True,
        )
        return r.returncode == 0 and out_png.is_file()

    print("    install poppler-utils (pdftoppm) or ghostscript", file=sys.stderr)
    return False


def page_mostly_blank(png: Path, threshold: float = 0.92) -> bool:
    conv = _convert_cmd()
    if not conv:
        return False
    r = subprocess.run(
        [*conv, str(png), "-colorspace", "Gray", "-format", "%[mean]", "info:"],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return False
    try:
        # mean is 0–65535 for Q16; high mean ≈ white page
        mean = float(r.stdout.strip()) / 65535.0
        return mean >= threshold
    except ValueError:
        return False


def extract_largest_figure(pdf: Path, max_pages: int, out_png: Path) -> bool:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return False

    doc = fitz.open(pdf)
    best = None
    best_area = 0
    for pno in range(min(max_pages, doc.page_count)):
        for img in doc[pno].get_images(full=True):
            xref = img[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 3:
                    continue
                area = pix.width * pix.height
                if area > best_area and pix.width >= 200 and pix.height >= 120:
                    best_area = area
                    best = pix
            except Exception:
                continue
    doc.close()
    if not best:
        return False
    best.save(str(out_png))
    return True


def generate_preview(entry: dict, out: Path, dry_run: bool) -> str:
    """Returns method name or empty string on failure."""
    key = entry["key"]
    if dry_run:
        print(f"  would try pdf={entry['pdf']!r} html={entry['html']!r}")
        return "dry-run"

    with tempfile.TemporaryDirectory(prefix="folio-preview-") as tmp:
        tmpdir = Path(tmp)
        raw = tmpdir / "raw.png"

        if entry["pdf"]:
            pdf_path = tmpdir / "paper.pdf"
            print(f"  downloading PDF …")
            if download_pdf(entry["pdf"], pdf_path):
                for page in (1, 2):
                    page_png = tmpdir / f"page{page}.png"
                    if not render_pdf_page(pdf_path, page, page_png):
                        continue
                    if page == 2 and not page_mostly_blank(tmpdir / "page1.png"):
                        break
                    if page == 1 and page_mostly_blank(page_png):
                        continue
                    shutil.copy2(page_png, raw)
                    resize_png(raw, out)
                    return f"pdf-page-{page}"

                fig_png = tmpdir / "figure.png"
                if extract_largest_figure(pdf_path, 2, fig_png):
                    resize_png(fig_png, out)
                    return "pdf-figure"

        if entry["html"]:
            img_url = og_image(entry["html"])
            if img_url:
                print(f"  og:image {img_url[:80]}…")
                try:
                    data = _http_get(img_url)
                    tmp = tmpdir / "og.bin"
                    tmp.write_bytes(data)
                    # normalize extension
                    if data[:8] == b"\x89PNG\r\n\x1a\n":
                        shutil.copy2(tmp, raw)
                    else:
                        # try convert for jpeg/webp
                        conv = _convert_cmd()
                        if conv:
                            subprocess.run([*conv, str(tmp), str(raw)], check=True, capture_output=True)
                        else:
                            shutil.copy2(tmp, raw)
                    resize_png(raw, out)
                    return "og-image"
                except OSError as e:
                    print(f"    og fetch failed: {e}", file=sys.stderr)

    return ""


def update_bib_preview(path: Path, key: str, filename: str) -> bool:
    text = path.read_text(encoding="utf-8")
    pattern = rf"@\w+\{{{re.escape(key)},.*?\n\}}"
    m = re.search(pattern, text, re.S)
    if not m:
        return False
    block = m.group(0)
    if "preview=" in block:
        return False
    lines = block.splitlines()
    lines.insert(-1, f"  preview={{{filename}}},")
    new_block = "\n".join(lines) + "\n"
    path.write_text(text[: m.start()] + new_block + text[m.end() :], encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="print planned actions only")
    parser.add_argument("--force", action="store_true", help="regenerate even if preview= is set")
    parser.add_argument("--update-bib", action="store_true", help="add preview={key}.png to papers.bib")
    parser.add_argument("--keys", nargs="*", help="only these bib keys")
    args = parser.parse_args()

    if not _which("pdftoppm") and not _which("gs"):
        print("Warning: no pdftoppm or gs — PDF thumbnails will not work.", file=sys.stderr)

    OUT.mkdir(parents=True, exist_ok=True)
    key_set = set(args.keys) if args.keys else None
    entries = parse_bib(BIB, only_missing=not args.force, keys=key_set)

    if not entries:
        print("No entries to process.")
        if not args.dry_run:
            write_manifest()
        return

    ok = 0
    for entry in entries:
        out = OUT / f"{entry['key']}.png"
        print(f"{entry['key']} -> {out.name}")
        if args.dry_run:
            generate_preview(entry, out, dry_run=True)
            continue
        method = generate_preview(entry, out, dry_run=False)
        if method and out.is_file():
            ok += 1
            print(f"  ok ({method})")
            if args.update_bib:
                fname = f"{entry['key']}.png"
                if update_bib_preview(BIB, entry["key"], fname):
                    print(f"  added preview={{{fname}}} to papers.bib")
        else:
            print("  skipped (no thumbnail source)")

    print(f"\nDone: {ok}/{len(entries)} thumbnails in {OUT.relative_to(ROOT)}")
    if not args.dry_run:
        write_manifest()


if __name__ == "__main__":
    main()
