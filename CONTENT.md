# Adding content

## Publications

1. Open [`_bibliography/papers.bib`](_bibliography/papers.bib).
2. Add a BibTeX entry (`@article`, `@inproceedings`, `@unpublished`, etc.).
3. Optional fields used by this site:
   - `abbr={ICML}` — venue badge (define colors in [`_data/venues.yml`](_data/venues.yml))
   - `preview={filename.png}` — thumbnail in `assets/img/publication_preview/`
   - `selected={true}` — highlight on the about page
   - `html`, `pdf`, `code`, `eprint` — link buttons on the publication card
   - For PDFs: use direct URLs (arXiv `https://arxiv.org/pdf/…`, EPFL Infoscience `…/record/…/files/…`, or site paths like `/files/thesis_compressed.pdf`). Do not use bare Infoscience record pages — they can redirect with personal tokens.
   - Preprints with `eprint={…}` get an automatic arXiv PDF link when `pdf` is omitted.
   - `note={Under review}` — status line for preprints

Co-author links: add entries to [`_data/coauthors.yml`](_data/coauthors.yml) keyed by last name.

### Thumbnails (uniform size)

- Add `preview={your-image.png}` in the bib entry; place the file in `assets/img/publication_preview/`.
- All preview images are displayed at a fixed height (140px) with `object-fit: cover` via CSS.
- Entries without `preview` show a venue **abbr** badge instead.

Optional: run `bin/fetch_publication_previews.py` before building to try downloading Open Graph images from `html` / arXiv URLs (requires network and ImageMagick). The script does not modify `papers.bib` automatically — review downloads and add `preview=` fields yourself.

### Homepage selected papers

Order is fixed in [`_includes/selected_papers.html`](_includes/selected_papers.html) (not by `selected={true}` sort). Edit the `-q @*[key^=...]*` lines to change which papers appear and in what order.

## Courses / teaching

1. Copy [`_teaching/_template.md`](_teaching/_template.md) to `_teaching/YYYY-term-slug.md`.
2. Set `published: true` (or remove `published: false` from the template).
3. Fill `title`, `type`, `venue`, and `date` in the front matter (no body text needed).

Courses appear on [/teaching/](_pages/teaching.md) as a compact list (no separate page per course). Add markdown files under `_teaching/` only.

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
