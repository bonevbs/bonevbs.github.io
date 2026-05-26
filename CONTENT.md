# Adding content

## Publications

1. Open [`_bibliography/papers.bib`](_bibliography/papers.bib).
2. Add a BibTeX entry (`@article`, `@inproceedings`, `@unpublished`, etc.).
3. Optional fields used by this site:
   - `abbr={ICML}` — venue badge (define colors in [`_data/venues.yml`](_data/venues.yml))
   - `preview={filename.png}` — thumbnail in `assets/img/publication_preview/`
   - `selected={true}` — highlight on the about page
   - `html`, `pdf`, `code`, `eprint` — link buttons on the publication card (`pdf` is also used for auto-thumbnails)
   - For PDFs: use direct URLs (arXiv `https://arxiv.org/pdf/…`, EPFL Infoscience `…/record/…/files/…`, or site paths like `/files/thesis_compressed.pdf`). Do not use bare Infoscience record pages — they can redirect with personal tokens.
   - Preprints with `eprint={…}` get an automatic arXiv PDF link when `pdf` is omitted.
   - `note={Under review}` — status line for preprints

Co-author links: add entries to [`_data/coauthors.yml`](_data/coauthors.yml) keyed by last name.

### Thumbnails (uniform size)

- All preview images are displayed at a fixed height (max 280px, width max 200px) with `object-fit: contain` via CSS.
- **Deploy CI** runs `bin/generate_publication_previews.py` before each `jekyll build` (see [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)). You do not need to run it manually for the live site.
- Generated files: `assets/img/publication_preview/{bibkey}.png` and [`_data/generated_previews.yml`](_data/generated_previews.yml) (lists bib keys with auto `{bibkey}.png` only).
- Manual `preview={your-image.png}` in `papers.bib` is **off** by default (`enable_manual_publication_previews: false` in `_config.yml`). Set it to `true` to use custom images again.
- Entries with no auto thumb show the venue **abbr** badge.

**Local run** (optional, for `jekyll serve` without waiting for CI):

```bash
sudo apt-get install -y poppler-utils ghostscript imagemagick   # once
pip install pymupdf
python3 bin/generate_publication_previews.py
```

Add a direct link in the bib entry: `pdf={https://…/paper.pdf}` or `pdf={/files/your.pdf}` for site-local files. The script only reads `pdf=` (no URL guessing from `eprint` / `html`). It uses the first page with an embedded figure large enough on the page (via PyMuPDF), otherwise page 1. The full page is scaled to fit without cropping.

**Clear and regenerate** (existing `{bibkey}.png` files are skipped unless you force):

```bash
python3 bin/generate_publication_previews.py --clear   # deletes auto {bibkey}.png + manifest only, then rebuilds
# or
python3 bin/generate_publication_previews.py --force # overwrite {bibkey}.png only
```

**CI:** Actions → **deploy** → **Run workflow**, check **Clear publication preview cache** to skip the preview cache, wipe thumbnails, regenerate from PDFs, build, and deploy.

Flags: `--dry-run`, `--force`, `--clear`, `--keys KEY`, `--update-bib` (optional; writes `preview=` into `papers.bib` — not required for CI).

To disable preview generation in CI, set repo variable `SKIP_PUBLICATION_PREVIEWS` = `true`.

### Homepage selected papers

Order is fixed in [`_includes/selected_papers.html`](_includes/selected_papers.html) (not by `selected={true}` sort). Edit the `-q @*[key^=...]*` lines to change which papers appear and in what order.

## Courses / teaching

Edit the course list directly in [`_pages/teaching.md`](_pages/teaching.md). Legacy per-course files may remain in `_teaching/` for reference but are not rendered on the site.

## Blog posts

1. Create `_posts/YYYY-MM-DD-slug.md`.
2. Use YAML front matter:

```yaml
---
title: "Post title"
date: 2025-01-15
tags: [machine-learning]
permalink: /posts/my-slug/
---
```

3. Write the post body in Markdown below the front matter.

## Local preview

```bash
docker compose up
# or
bundle install && bundle exec jekyll serve
```

This site is built for **https://bonevbs.github.io/** (`url` + empty `baseurl` in [`_config.yml`](_config.yml)). Deploy from a repo named `bonevbs.github.io` (GitHub user Pages). Use `relative_url` for internal paths in Markdown/Liquid.
