---
layout: page
permalink: /research/
title: Research
description: Research in AI for science and engineering, numerical methods, and scientific machine learning.
nav: true
nav_order: 2
wide_media: true
---

I work at the interface of scientific computing, numerical analysis, and machine learning. My training is in classical **numerical methods**; I am interested in how modern ML can be used reliably in science and engineering—where predictions must be accurate, efficient, and interpretable beyond the training set.

A full publication list is on [Google Scholar](https://scholar.google.com/citations?user=sYo-KS4AAAAJ).

## AI for Science and Engineering

Scientific machine learning is reshaping how we model complex physical systems. In weather and climate, learned models now compete with operational forecast systems; in other domains, neural operators and related architectures learn maps between function spaces from data or hybrid data–physics setups. A recurring theme is **trustworthiness**: stability, generalization, uncertainty, and consistency with known structure (symmetries, conservation, geometry).

My recent work emphasizes ML methods for science and engineering, including AI weather and climate models. [Spherical Fourier Neural Operators](https://arxiv.org/abs/2306.03838) generalize Fourier Neural Operators to spherical geometry for global atmospheric dynamics. See the [NVIDIA blog post](https://developer.nvidia.com/blog/modeling-earths-atmosphere-with-spherical-fourier-neural-operators/) and [ICML paper](https://openreview.net/forum?id=TwsJ9IOZDx). Related directions include the **numerics of ML methods**, **geometric machine learning** on spheres and other manifolds, and **uncertainty quantification** for operational use.

![Spherical Fourier Neural Operators demo](https://developer-blogs.nvidia.com/wp-content/uploads/2023/07/figure_1.11-2.gif)

## Numerical Methods

Rigorous numerical methods remain essential—for verification, hybrid models, and problems where data alone are insufficient. I develop and analyze algorithms for large-scale linear systems and PDEs, with an eye toward complexity, robustness, and implementations that scale on modern hardware. This strand of work complements scientific ML: many of the same tools (sparse structure, low rank, adaptivity) appear in both classical solvers and learned models.

In **numerical linear algebra**, I focus on scalable solvers for sparse systems, especially from wave and Helmholtz formulations. **Hierarchical matrices** and related formats compress dense blocks that arise during factorization, so memory and operation counts can grow nearly linearly with problem size while retaining controllable accuracy. Sparse direct solvers target systems $A x = b$ without relying on many Krylov iterations when spectra are unfavorable or many right-hand sides are needed; hierarchical compression combined with structured elimination yields approximate factorizations and preconditioners for challenging wave problems. See [our SIAM paper](https://epubs.siam.org/doi/10.1137/20M1365958) and the [PhD dissertation]({{ '/files/thesis_compressed.pdf' | relative_url }}).

![Helmholtz solutions on a guitar]({{ '/files/guitars_hprecon.png' | relative_url }})

For **numerical solvers for PDEs**, I am interested in high-order discretizations, stability, and faithful treatment of multiscale geophysical phenomena. Discontinuous Galerkin (DG) methods offer strong accuracy per degree of freedom for hyperbolic problems and parallel well on HPC systems. We adapted DG to global tsunami modeling with the spherical shallow water equations, including well-balanced schemes, wetting and drying, and mesh adaptivity on the sphere. See [JCP](https://doi.org/10.1016/j.jcp.2018.02.008) and [Ocean Modelling](https://doi.org/10.1016/j.ocemod.2019.101429).

<div class="media-grid media-grid--2-third">
  <a href="{{ '/files/amr_showcase.mp4' | relative_url }}">
    <img src="{{ '/assets/img/publication_preview/amr_showcase_prev.png' | relative_url }}" alt="Tsunami AMR simulation">
  </a>
  <a href="{{ '/files/tohoku.mp4' | relative_url }}">
    <img src="{{ '/assets/img/publication_preview/tohoku_prev.png' | relative_url }}" alt="Tohoku tsunami simulation">
  </a>
</div>
