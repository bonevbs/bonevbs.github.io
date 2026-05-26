---
layout: page
permalink: /research/
title: Research
nav: true
nav_order: 2
wide_media: true
---

I work at the interface of scientific computing, numerical analysis, and machine learning. My training is in classical **numerical methods**; I am interested in how modern ML can be used reliably in science and engineering—where predictions must be accurate, efficient, and interpretable beyond the training set.

A full publication list is on [Google Scholar](https://scholar.google.com/citations?user=sYo-KS4AAAAJ).

## AI for Science and Engineering

Scientific machine learning is reshaping how we model complex physical systems. In weather and climate, learned models now compete with operational forecast systems; in other domains, neural operators and related architectures learn maps between function spaces from data or hybrid data–physics setups. A recurring theme is **trustworthiness**: stability, generalization, uncertainty, and consistency with known structure (symmetries, conservation, geometry).

My recent work emphasizes ML methods for science and engineering, including AI weather and climate models. [Spherical Fourier Neural Operators](https://arxiv.org/abs/2306.03838) generalize Fourier Neural Operators to spherical geometry for global atmospheric dynamics. See the [NVIDIA blog post](https://developer.nvidia.com/blog/modeling-earths-atmosphere-with-spherical-fourier-neural-operators/) and [ICML paper](https://openreview.net/forum?id=TwsJ9IOZDx). Related directions include the **numerics of ML methods**, **geometric machine learning** on spheres and other manifolds, and **uncertainty quantification** for operational use.

![FourCastNet 3 ensemble rollout trained with Makani](https://raw.githubusercontent.com/NVIDIA/makani/main/images/fcn3_ens15.gif)

I believe numerical methods and machine learning will keep converging: ideas from traditional numerics—stability, preconditioning, multiscale structure—are showing up in learned models, and ML is feeding back into how we build solvers and discretizations.

## Numerical Methods

My background is in **algorithms for wave problems**: numerical PDE solvers and numerical linear algebra for large sparse systems. During my [PhD]({{ '/files/thesis_compressed.pdf' | relative_url }}), I worked on [approximate fast direct solvers](https://github.com/bonevbs/HierarchicalSolvers.jl) for Helmholtz-type problems ([SIAM paper](https://epubs.siam.org/doi/10.1137/20M1365958)) and [discontinuous Galerkin methods](https://doi.org/10.1016/j.jcp.2018.02.008) for global tsunami modeling ([Ocean Modelling](https://doi.org/10.1016/j.ocemod.2019.101429)).

<div class="media-grid media-grid--2x3">
  <a href="{{ '/files/amr_showcase.mp4' | relative_url }}">
    <img src="{{ '/assets/img/research/amr_showcase_prev.png' | relative_url }}" alt="Tsunami AMR simulation">
  </a>
  <a href="{{ '/files/tohoku.mp4' | relative_url }}">
    <img src="{{ '/assets/img/research/tohoku_prev.png' | relative_url }}" alt="Tohoku tsunami simulation">
  </a>
  <a href="https://epubs.siam.org/doi/10.1137/20M1365958">
    <img src="{{ '/assets/img/research/helmholtz_square.png' | relative_url }}" alt="Helmholtz wave solutions">
  </a>
  <a href="https://github.com/bonevbs/HierarchicalSolvers.jl">
    <img src="{{ '/assets/img/research/hss_sparsity_pattern.png' | relative_url }}" alt="Sparse factor sparsity pattern">
  </a>
  <a href="https://github.com/bonevbs/HssMatrices.jl">
    <img src="{{ '/assets/img/research/hss_rank_structure.png' | relative_url }}" alt="HSS block rank structure">
  </a>
  <a href="https://epubs.siam.org/doi/10.1137/20M1365958">
    <img src="{{ '/assets/img/research/hss_rank_structure_large.png' | relative_url }}" alt="HSS rank structure for Helmholtz problem">
  </a>
</div>
