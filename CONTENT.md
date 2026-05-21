# Adding content

## Publications

1. Open [`_bibliography/papers.bib`](_bibliography/papers.bib).
2. Add a BibTeX entry (`@article`, `@inproceedings`, `@unpublished`, etc.).
3. Optional fields used by this site:
   - `abbr={ICML}` — venue badge (define colors in [`_data/venues.yml`](_data/venues.yml))
   - `preview={filename.png}` — thumbnail in `assets/img/publication_preview/`
   - `selected={true}` — highlight on the about page
   - `html`, `pdf`, `code`, `eprint` — link buttons on the publication card
   - `note={Under review}` — status line for preprints

Co-author links: add entries to [`_data/coauthors.yml`](_data/coauthors.yml) keyed by last name.

## Courses / teaching

1. Copy [`_teaching/_template.md`](_teaching/_template.md) to `_teaching/YYYY-term-slug.md`.
2. Set `published: true` (or remove `published: false` from the template).
3. Fill `title`, `type`, `venue`, `date`, `location`, and the markdown body.

Courses appear on [/teaching/](_pages/teaching.md) automatically.

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
