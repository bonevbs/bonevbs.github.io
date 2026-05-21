---
layout: page
permalink: /publications/
title: publications
description: Publications in reverse chronological order.
nav: true
nav_order: 1
---
<!-- _pages/publications.md -->

Publications are listed from `_bibliography/papers.bib`. To add a paper, append a BibTeX entry there (see `CONTENT.md` in the repo root).

<div class="publications">

{% bibliography -f {{ site.scholar.bibliography }} %}

</div>
