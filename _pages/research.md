---
layout: page
permalink: /research/
title: Research
description: Research in AI for science and engineering, numerical linear algebra, and PDE solvers.
nav: true
nav_order: 2
wide_media: true
---

I have a background in classical numerical methods, with a focus on **numerical linear algebra** and **numerical solvers for PDEs**. I am also interested in the reliable use of machine learning in science and engineering—building models that are accurate, efficient, and trustworthy when deployed outside the training distribution.

A full publication list is on [Google Scholar](https://scholar.google.com/citations?user=sYo-KS4AAAAJ).

## AI for Science and Engineering

ML-based methods can greatly accelerate scientific computing. In weather and climate, learned models now compete with operational forecast systems. A central question is how to trust predictions from data-driven models that are not tied to first-principles discretizations. Our work on [Spherical Fourier Neural Operators](https://arxiv.org/abs/2306.03838) generalizes Fourier Neural Operators to spherical geometry for global atmospheric dynamics. See the [NVIDIA blog post](https://developer.nvidia.com/blog/modeling-earths-atmosphere-with-spherical-fourier-neural-operators/) and [ICML paper](https://openreview.net/forum?id=TwsJ9IOZDx).

![Spherical Fourier Neural Operators demo](https://developer-blogs.nvidia.com/wp-content/uploads/2023/07/figure_1.11-2.gif)

## Numerical Methods

### Numerical linear algebra

Much of my earlier work concerns scalable linear algebra for large sparse systems, especially those arising from wave and Helmholtz problems. **Hierarchical matrices** (and related low-rank formats) compress dense blocks that appear during sparse factorization, so memory and operation counts grow nearly linearly with problem size while retaining controllable accuracy.

Sparse direct solvers solve $A x = b$ without relying on many Krylov iterations—important when spectra are unfavorable or right-hand sides are numerous. We combine hierarchical compression with structured elimination to obtain approximate factorizations and preconditioners for challenging wave problems. See [our SIAM paper](https://epubs.siam.org/doi/10.1137/20M1365958) and the [PhD dissertation]({{ '/files/thesis_compressed.pdf' | relative_url }}).

![Helmholtz solutions on a guitar]({{ '/files/guitars_hprecon.png' | relative_url }})

### Numerical solvers for PDEs

Discontinuous Galerkin (DG) methods achieve high accuracy per degree of freedom for hyperbolic PDEs and scale well on HPC systems. We adapted DG to global tsunami modeling with the spherical shallow water equations, including well-balanced discretizations, wetting and drying, and mesh adaptivity on the sphere. See [JCP](https://doi.org/10.1016/j.jcp.2018.02.008) and [Ocean Modelling](https://doi.org/10.1016/j.ocemod.2019.101429).

<div class="media-grid media-grid--2-third">
  <a href="{{ '/files/amr_showcase.mp4' | relative_url }}">
    <img src="{{ '/assets/img/publication_preview/amr_showcase_prev.png' | relative_url }}" alt="Tsunami AMR simulation">
  </a>
  <a href="{{ '/files/tohoku.mp4' | relative_url }}">
    <img src="{{ '/assets/img/publication_preview/tohoku_prev.png' | relative_url }}" alt="Tohoku tsunami simulation">
  </a>
</div>
