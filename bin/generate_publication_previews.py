#!/usr/bin/env python3
"""
Generate publication thumbnails for al-folio (preview={...} in papers.bib).

Uses only the `pdf={...}` field from each BibTeX entry (http(s) URL or site path like `/files/thesis.pdf`).
Picks the first page with a large on-page figure, else the first page with a
"Figure 1" caption, else the page with the largest embedded image, else page 1.
Renders every thumbnail to a fixed 200×280 canvas (letterboxed).

Usage:
  python3 bin/generate_publication_previews.py [--dry-run] [--force] [--clear] [--update-bib]
  python3 bin/generate_publication_previews.py --keys bonev2025fourcastnet3

Requires: network for downloads.
Recommended: `pip install pymupdf Pillow` (page picking + rendering).
Fallback rendering: pdftoppm (poppler-utils) or gs, plus ImageMagick for resize.

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
# Output size; matches publication list CSS.
PREVIEW_W = 200
PREVIEW_H = 280
PREVIEW_MAX = f"{PREVIEW_W}x{PREVIEW_H}"
UA = "ai-folio-preview-generator/1.0"
MAX_PAGES_SCAN = 24
# Figure must be a substantial part of the page (not logos/icons).
MIN_FIGURE_WIDTH_FRAC = 0.22
MIN_FIGURE_HEIGHT_FRAC = 0.12
MIN_FIGURE_AREA_FRAC = 0.04
BODY_MARGIN_Y = 0.07
FIGURE_ONE_RE = re.compile(r"\b(?:Figure|Fig\.?)\s+1\b", re.IGNORECASE)


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
    """Fit whole page inside PREVIEW_MAX; letterbox if aspect ratio differs."""
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


def _rect_in_body(rect, page_rect) -> bool:
    cy = (rect.y0 + rect.y1) / 2
    return BODY_MARGIN_Y * page_rect.height < cy < (1 - BODY_MARGIN_Y) * page_rect.height


def _iter_image_rects(page):
    seen: set[int] = set()
    for img in page.get_images(full=True):
        xref = img[0]
        if xref in seen:
            continue
        seen.add(xref)
        try:
            yield from page.get_image_rects(xref)
        except Exception:
            continue


def page_has_large_figure(page) -> bool:
    """True if the page draws a substantial figure in the body (not header/footer)."""
    pw, ph = page.rect.width, page.rect.height
    page_rect = page.rect
    for rect in _iter_image_rects(page):
        if not _rect_in_body(rect, page_rect):
            continue
        if (
            rect.width >= MIN_FIGURE_WIDTH_FRAC * pw
            and rect.height >= MIN_FIGURE_HEIGHT_FRAC * ph
            and rect.width * rect.height >= MIN_FIGURE_AREA_FRAC * pw * ph
        ):
            return True
    return False


def first_page_with_large_figure(doc) -> int | None:
    limit = min(MAX_PAGES_SCAN, doc.page_count)
    for pno in range(limit):
        if page_has_large_figure(doc[pno]):
            return pno + 1
    return None


def first_page_with_figure1_caption(doc) -> int | None:
    """First non-title page mentioning Figure 1 (helps vector-only PDFs)."""
    limit = min(MAX_PAGES_SCAN, doc.page_count)
    for pno in range(1, limit):
        if FIGURE_ONE_RE.search(doc[pno].get_text() or ""):
            return pno + 1
    return None


def page_with_largest_embedded_image(doc) -> int | None:
    limit = min(MAX_PAGES_SCAN, doc.page_count)
    best_page: int | None = None
    best_area = 0.0
    for pno in range(limit):
        page = doc[pno]
        page_area = page.rect.width * page.rect.height
        for rect in _iter_image_rects(page):
            area = rect.width * rect.height
            if area >= 0.02 * page_area and area > best_area:
                best_area = area
                best_page = pno + 1
    return best_page


def choose_thumbnail_page(doc) -> tuple[int, str]:
    """Pick page to render. Returns (page_number, reason_tag)."""
    figure_page = first_page_with_large_figure(doc)
    if figure_page is not None:
        return figure_page, "figure-page"
    caption_page = first_page_with_figure1_caption(doc)
    if caption_page is not None:
        return caption_page, "figure-1"
    largest = page_with_largest_embedded_image(doc)
    if largest is not None:
        return largest, "largest-image"
    return 1, "first-page"


def render_page_normalized(doc, page: int, dest: Path) -> bool:
    """Render a PDF page to a fixed PREVIEW_W×PREVIEW_H PNG."""
    import fitz

    if page < 1 or page > doc.page_count:
        return False
    pg = doc[page - 1]
    pw, ph = pg.rect.width, pg.rect.height
    scale = min(PREVIEW_W / pw, PREVIEW_H / ph)
    pix = pg.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)

    try:
        from PIL import Image
    except ImportError:
        tmp = dest.with_suffix(".raw.png")
        pix.save(tmp)
        resize_png(tmp, dest)
        tmp.unlink(missing_ok=True)
        return dest.is_file()

    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    canvas = Image.new("RGB", (PREVIEW_W, PREVIEW_H), (255, 255, 255))
    canvas.paste(img, ((PREVIEW_W - img.width) // 2, (PREVIEW_H - img.height) // 2))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, "PNG")
    return True


def generate_preview(entry: dict, out: Path, dry_run: bool) -> str:
    """Returns method name or empty string on failure."""
    pdf_src = entry["pdf"]
    if dry_run:
        print(f"  would render pdf={pdf_src!r}")
        return "dry-run"

    with tempfile.TemporaryDirectory(prefix="folio-preview-") as tmp:
        tmpdir = Path(tmp)
        pdf_path = tmpdir / "paper.pdf"

        if isinstance(pdf_src, Path):
            print(f"  local PDF {pdf_src.relative_to(ROOT)}")
            shutil.copy2(pdf_src, pdf_path)
        else:
            print("  downloading PDF …")
            if not download_pdf(pdf_src, pdf_path):
                return ""

        page, reason = 1, "first-page"
        try:
            import fitz

            doc = fitz.open(pdf_path)
            page, reason = choose_thumbnail_page(doc)
            if render_page_normalized(doc, page, out):
                doc.close()
                return f"{reason}-{page}"
            doc.close()
        except ImportError:
            pass

        page_png = tmpdir / "thumb.png"
        if render_pdf_page(pdf_path, page, page_png):
            resize_png(page_png, out)
            return f"{reason}-{page}"

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
    args = parser.parse_args()
    if not _which("pdftoppm") and not _which("gs"):
        print("Warning: no pdftoppm or gs — PDF thumbnails will not work.", file=sys.stderr)

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
