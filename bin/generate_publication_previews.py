#!/usr/bin/env python3
"""
Generate publication thumbnails for al-folio (preview={...} in papers.bib).

Uses only the `pdf={...}` field from each BibTeX entry (http(s) URL or site path like `/files/thesis.pdf`).
By default, extracts the first embedded figure image in the PDF (PyMuPDF).
Falls back to rendering a full page (first figure page, else page 1/2) if extraction fails.

Set EXTRACT_EMBEDDED_FIGURES = False (or pass --full-page) to restore page-only thumbnails.

Usage:
  python3 bin/generate_publication_previews.py [--dry-run] [--force] [--clear] [--update-bib]
  python3 bin/generate_publication_previews.py --keys bonev2025fourcastnet3

Requires: network for downloads. For PDF rendering, one of:
  pdftoppm (poppler-utils), or gs (ghostscript).
Optional: `pip install pymupdf` (recommended — detects figure pages)
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
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "_bibliography" / "papers.bib"
OUT = ROOT / "assets" / "img" / "publication_preview"
MANIFEST = ROOT / "_data" / "generated_previews.yml"
# Square canvas; image fitted inside (letterboxed). Matches publication list CSS.
PREVIEW_MAX = "240x240"
UA = "ai-folio-preview-generator/1.0"
# Ignore tiny icons/logos when scanning for figure pages.
MIN_FIGURE_WIDTH = 120
MIN_FIGURE_HEIGHT = 80
MIN_FIGURE_PIXELS = MIN_FIGURE_WIDTH * MIN_FIGURE_HEIGHT
MAX_PAGES_SCAN = 12

# Experimental: first embedded figure as thumbnail. Set False to revert to full-page renders.
EXTRACT_EMBEDDED_FIGURES = True


def _http_get(url: str, timeout: int = 60) -> bytes:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _which(cmd: str) -> str | None:
    return shutil.which(cmd)


def _convert_cmd() -> list[str] | None:
    for cmd in ("magick", "convert"):
        if _which(cmd):
            return [cmd]
    return None


def resize_png(src: Path, dest: Path) -> None:
    """Fit image inside square PREVIEW_MAX; letterbox if aspect ratio differs."""
    conv = _convert_cmd()
    if not conv:
        shutil.copy2(src, dest)
        return
    subprocess.run(
        [
            *conv,
            str(src),
            "-resize",
            f"{PREVIEW_MAX}>",
            "-background",
            "white",
            "-alpha",
            "remove",
            "-gravity",
            "center",
            "-extent",
            PREVIEW_MAX,
            str(dest),
        ],
        check=True,
        capture_output=True,
    )


def parse_field(block: str, name: str) -> str | None:
    m = re.search(rf"{name}\s*=\s*\{{([^}}]+)\}}", block)
    return m.group(1).strip() if m else None


def resolve_pdf(block: str) -> str | Path | None:
    """Return PDF URL string or local Path from the bib entry's pdf= field only."""
    pdf = parse_field(block, "pdf")
    if not pdf:
        return None
    if pdf.startswith(("http://", "https://")):
        return pdf
    if pdf.startswith("/"):
        local = ROOT / pdf.lstrip("/")
        return local if local.is_file() else None
    return None


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
        out_png = OUT / f"{key}.png"
        if only_missing and out_png.is_file():
            continue
        pdf = resolve_pdf(block)
        if not pdf:
            continue
        entries.append({"key": key, "pdf": pdf})
    return entries


def bib_keys(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return {m.group(1).strip() for m in re.finditer(r"@\w+\{([^,]+),", text)}


def write_manifest() -> None:
    valid = bib_keys(BIB)
    keys = sorted(p.stem for p in OUT.glob("*.png") if p.stem in valid)
    MANIFEST.write_text(
        "# Updated by bin/generate_publication_previews.py\nkeys:\n"
        + "".join(f"  - {k}\n" for k in keys),
        encoding="utf-8",
    )
    print(f"Manifest: {len(keys)} previews in {MANIFEST.relative_to(ROOT)}")


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


def _figure_qualifies(width: int, height: int) -> bool:
    return (
        width >= MIN_FIGURE_WIDTH
        and height >= MIN_FIGURE_HEIGHT
        and width * height >= MIN_FIGURE_PIXELS
    )


def _have_pymupdf() -> bool:
    try:
        import fitz  # noqa: F401

        return True
    except ImportError:
        return False


def _pixmap_to_png(pix, dest: Path) -> None:
    import fitz  # PyMuPDF

    if pix.n - pix.alpha >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    elif pix.alpha:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    pix.save(str(dest))


def _save_figure_pixmap(doc, page, xref: int, dest: Path) -> bool:
    import fitz  # PyMuPDF

    try:
        pix = fitz.Pixmap(doc, xref)
        if not _figure_qualifies(pix.width, pix.height):
            return False
        _pixmap_to_png(pix, dest)
        return True
    except Exception:
        rects = page.get_image_rects(xref)
        if not rects:
            return False
        clip = rects[0]
        if clip.width < MIN_FIGURE_WIDTH or clip.height < MIN_FIGURE_HEIGHT:
            return False
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip, alpha=False)
        _pixmap_to_png(pix, dest)
        return dest.is_file()


def find_first_figure(pdf: Path) -> tuple[int, int] | None:
    """Return (page_1based, image_xref) for the first sizeable embedded figure, or None."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return None

    doc = fitz.open(pdf)
    try:
        limit = min(MAX_PAGES_SCAN, doc.page_count)
        for pno in range(limit):
            page = doc[pno]
            for img in page.get_images(full=True):
                xref = img[0]
                try:
                    pix = fitz.Pixmap(doc, xref)
                    if _figure_qualifies(pix.width, pix.height):
                        return pno + 1, xref
                except Exception:
                    rects = page.get_image_rects(xref)
                    if rects and _figure_qualifies(int(rects[0].width), int(rects[0].height)):
                        return pno + 1, xref
                    continue
    finally:
        doc.close()
    return None


def extract_first_figure(pdf: Path, dest: Path) -> tuple[int, int] | None:
    """Save the first sizeable embedded image to dest. Returns (page_1based, xref) or None."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return None

    doc = fitz.open(pdf)
    try:
        limit = min(MAX_PAGES_SCAN, doc.page_count)
        for pno in range(limit):
            page = doc[pno]
            for img in page.get_images(full=True):
                xref = img[0]
                if _save_figure_pixmap(doc, page, xref, dest):
                    return pno + 1, xref
    finally:
        doc.close()
    return None


def first_page_with_figure(pdf: Path) -> int | None:
    """Return 1-based page index of the first page with a sizeable embedded image, or None."""
    hit = find_first_figure(pdf)
    return hit[0] if hit else None


def choose_thumbnail_page(pdf_path: Path, tmpdir: Path) -> tuple[int, str]:
    """Pick page to render. Returns (page_number, reason_tag)."""
    figure_page = first_page_with_figure(pdf_path)
    if figure_page is not None:
        return figure_page, "figure-page"

    for page in (1, 2):
        page_png = tmpdir / f"probe{page}.png"
        if not render_pdf_page(pdf_path, page, page_png):
            continue
        if page == 1 and page_mostly_blank(page_png):
            continue
        return page, "first-page"

    return 1, "first-page-fallback"


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


def generate_preview(entry: dict, out: Path, dry_run: bool, *, full_page: bool = False) -> str:
    """Returns method name or empty string on failure."""
    pdf_src = entry["pdf"]
    if dry_run:
        mode = "full-page" if full_page else "figure-then-page-fallback"
        print(f"  would process pdf={pdf_src!r} ({mode})")
        return "dry-run"

    with tempfile.TemporaryDirectory(prefix="folio-preview-") as tmp:
        tmpdir = Path(tmp)
        raw = tmpdir / "raw.png"
        pdf_path = tmpdir / "paper.pdf"

        if isinstance(pdf_src, Path):
            print(f"  local PDF {pdf_src.relative_to(ROOT)}")
            shutil.copy2(pdf_src, pdf_path)
        else:
            print("  downloading PDF …")
            if not download_pdf(pdf_src, pdf_path):
                return ""

        use_figures = EXTRACT_EMBEDDED_FIGURES and not full_page
        if use_figures:
            fig = extract_first_figure(pdf_path, raw)
            if fig:
                page, xref = fig
                resize_png(raw, out)
                return f"figure-p{page}-xref{xref}"

        page, reason = choose_thumbnail_page(pdf_path, tmpdir)
        page_png = tmpdir / "thumb.png"
        if render_pdf_page(pdf_path, page, page_png):
            shutil.copy2(page_png, raw)
            resize_png(raw, out)
            tag = "page-fallback" if use_figures else reason
            return f"{tag}-{page}"

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
    parser.add_argument("--force", action="store_true", help="regenerate even if {key}.png already exists")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="delete all PNGs in publication_preview/ and the manifest, then regenerate",
    )
    parser.add_argument("--update-bib", action="store_true", help="add preview={key}.png to papers.bib")
    parser.add_argument("--keys", nargs="*", help="only these bib keys")
    parser.add_argument(
        "--full-page",
        action="store_true",
        help="render full PDF pages only (revert embedded-figure extraction)",
    )
    args = parser.parse_args()
    if not _which("pdftoppm") and not _which("gs"):
        print("Warning: no pdftoppm or gs — PDF thumbnails will not work.", file=sys.stderr)
    if EXTRACT_EMBEDDED_FIGURES and not args.full_page and not _have_pymupdf():
        print("Warning: pymupdf not installed — figure extraction disabled, using page fallback.", file=sys.stderr)

    OUT.mkdir(parents=True, exist_ok=True)
    if args.clear:
        removed = 0
        for key in bib_keys(BIB):
            png = OUT / f"{key}.png"
            if png.is_file():
                png.unlink()
                removed += 1
        MANIFEST.unlink(missing_ok=True)
        print(f"Cleared {removed} auto-generated preview(s) and manifest (manual PNGs kept).")
        args.force = True

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
            generate_preview(entry, out, dry_run=True, full_page=args.full_page)
            continue
        method = generate_preview(entry, out, dry_run=False, full_page=args.full_page)
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
