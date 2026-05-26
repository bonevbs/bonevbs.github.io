---
layout: page
permalink: /research/
title: Research
nav: true
nav_order: 2
wide_media: true
---

I work at the interface of scientific computing, numerical analysis, and machine learning. My training is in classical **numerical methods**; I am interested in how modern ML can be used reliably in science and engineering—where predictions must be accurate, efficient, and interpretable beyond the training set.

## AI for Science and Engineering

Scientific machine learning is reshaping how we model complex physical systems. In weather and climate, learned models now compete with operational forecast systems; in other domains, neural operators learn maps between function spaces from data or hybrid data–physics setups. Much of my work aims to develop AI-for-science methods from first principles: architectures and training objectives that respect geometry, stability, and uncertainty, rather than treating these as afterthoughts at deployment time.

Representative examples include [Spherical Fourier Neural Operators (SFNO)](https://arxiv.org/abs/2306.03838) for stable dynamics on the sphere, [neural operators with localized integral and differential kernels](https://arxiv.org/abs/2402.16845) for multiscale structure, [principled approaches for extending neural architectures to function spaces](https://arxiv.org/abs/2506.10973), and [FourCastNet 3](https://arxiv.org/abs/2507.12144), which combines spherical signal-processing primitives with end-to-end probabilistic ensemble training. These ideas connect to classical numerical analysis—resolution invariance, controlled spectra, calibrated uncertainty—and are supported in practice by libraries such as [torch-harmonics](https://github.com/NVIDIA/torch-harmonics) and [NeuralOperator](https://github.com/NeuralOperator/neuraloperator).

The same geometric operator viewpoint has carried into operational climate and weather modeling. SFNO-based methods underpin learned global models and large ensembles, including [ACE](https://arxiv.org/abs/2310.02074) for climate prediction, the [Huge Ensembles](https://doi.org/10.5194/gmd-18-5575-2025) hindcast studies ([Part 1](https://doi.org/10.5194/gmd-18-5575-2025), [Part 2](https://doi.org/10.5194/gmd-18-5605-2025)), and [FourCastNet 3](https://arxiv.org/abs/2507.12144) for fast, skillful probabilistic medium-range forecasting. The video below shows 15 FourCastNet 3 ensemble members from a rollout trained with [Makani](https://github.com/NVIDIA/makani); in the [paper](https://arxiv.org/abs/2507.12144), each 15-day global forecast is generated in about 60 seconds on a single NVIDIA H100 GPU, so an ensemble of this size is feasible on one GPU in minutes rather than the hours required by conventional systems.

![FourCastNet 3 ensemble rollout trained with Makani]({{ '/assets/img/research/fcn3_ens15.gif' | relative_url }})

## Numerical Methods

My background is in numerical methods, with a focus on partial differential equations and numerical linear algebra. That training remains a source of inspiration for my ML work: stability, preconditioning, and multiscale structure show up in learned models, and ideas from ML feed back into how we build solvers and discretizations. I believe numerical methods and machine learning will ultimately form one cohesive field that integrates tools from both traditions.

During my [PhD]({{ '/files/thesis_compressed.pdf' | relative_url }}), I worked on [approximate fast direct solvers](https://github.com/bonevbs/HierarchicalSolvers.jl) for Helmholtz-type problems ([SIAM paper](https://epubs.siam.org/doi/10.1137/20M1365958)) and [discontinuous Galerkin methods](https://doi.org/10.1016/j.jcp.2018.02.008) for global tsunami modeling ([Ocean Modelling](https://doi.org/10.1016/j.ocemod.2019.101429)). Here are some interesting samples:

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
