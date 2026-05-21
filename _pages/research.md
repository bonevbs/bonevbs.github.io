---
layout: page
permalink: /research/
title: research
description: Research interests in machine learning, scientific computing, and numerical algorithms.
nav: true
nav_order: 2
wide_media: true
---

My research interests broadly revolve around mathematical algorithms, with a focus on *machine learning*, *scientific computing*, and *numerical linear algebra*.

You can find a full publication list on [Google Scholar](https://scholar.google.com/citations?user=sYo-KS4AAAAJ).

## ML-based weather prediction with neural operators

ML-based methods promise to greatly accelerate scientific computing. Recent advances in ML-based weather prediction have shown that these methods can compete with state-of-the-art classical systems. A central question is how to trust models trained from data rather than first principles. Our work on [Spherical Fourier Neural Operators](https://arxiv.org/abs/2306.03838) generalizes Fourier Neural Operators to spherical geometry. See the [NVIDIA blog post](https://developer.nvidia.com/blog/modeling-earths-atmosphere-with-spherical-fourier-neural-operators/) and [ICML paper](https://openreview.net/forum?id=TwsJ9IOZDx).

![Spherical Fourier Neural Operators demo](https://developer-blogs.nvidia.com/wp-content/uploads/2023/07/figure_1.11-2.gif)

## Sparse direct solvers for wave problems

Sparse direct solvers solve $A x = b$ without relying on many Krylov iterations — important for wave problems. We use *hierarchical matrices* to compress fill-in during factorization, enabling quasi-linear complexity for problems such as the Helmholtz equation. These methods also serve as preconditioners. See [our SIAM paper](https://epubs.siam.org/doi/10.1137/20M1365958) and [PhD dissertation]({{ '/files/thesis_compressed.pdf' | relative_url }}).

![Helmholtz solutions on a guitar]({{ '/files/guitars_hprecon.png' | relative_url }})

## Discontinuous Galerkin methods for tsunami simulations

Discontinuous Galerkin methods achieve high accuracy per degree of freedom for hyperbolic PDEs and scale well on HPC systems. We adapted DG to global tsunami modeling using the spherical shallow water equations, with well-balancedness, wetting/drying, and mesh adaptivity. See [JCP](https://doi.org/10.1016/j.jcp.2018.02.008) and [Ocean Modelling](https://doi.org/10.1016/j.ocemod.2019.101429).

<div class="media-grid">
  <a href="{{ '/files/amr_showcase.mp4' | relative_url }}">
    <img src="{{ '/assets/img/publication_preview/amr_showcase_prev.png' | relative_url }}" alt="Tsunami AMR simulation">
  </a>
  <a href="{{ '/files/tohoku.mp4' | relative_url }}">
    <img src="{{ '/assets/img/publication_preview/tohoku_prev.png' | relative_url }}" alt="Tohoku tsunami simulation">
  </a>
</div>
