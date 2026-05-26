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

### Trustworthy geometric neural operators

I am especially interested in operator-learning architectures that respect the geometry and physics of the domain—not as an afterthought, but in the design of the model class. On the sphere, this line of work includes:

- [**Spherical Fourier Neural Operators (SFNO)**](https://arxiv.org/abs/2306.03838) — spectral operators on the sphere for stable global dynamics ([ICML](https://openreview.net/forum?id=TwsJ9IOZDx), [NVIDIA blog](https://developer.nvidia.com/blog/modeling-earths-atmosphere-with-spherical-fourier-neural-operators/))
- [**Neural operators with localized integral and differential kernels**](https://arxiv.org/abs/2402.16845) — combining global spectral structure with local kernels for multiscale PDEs ([ICML 2024](https://arxiv.org/abs/2402.16845))
- [**Attention on the Sphere**](https://arxiv.org/abs/2505.11157) — attention mechanisms adapted to spherical geometry ([NeurIPS 2025](https://arxiv.org/abs/2505.11157))
- [**Principled approaches for extending neural architectures to function spaces**](https://arxiv.org/abs/2506.10973) — a unified view of how standard layers lift to operators on function spaces

These methods share a goal: models that generalize across resolution and grid, behave predictably outside the training distribution, and connect to classical numerical analysis. Related themes include mixed-precision guarantees for neural operators, codomain attention for multiphysics PDEs, and libraries such as [torch-harmonics](https://github.com/NVIDIA/torch-harmonics) and [NeuralOperator](https://github.com/NeuralOperator/neuraloperator) that make geometric operators practical at scale.

### AI weather and climate at scale

Building on SFNO, our group has pushed learned global models toward operational climate and ensemble forecasting:

- [**ACE**](https://arxiv.org/abs/2310.02074) — a fast, skillful learned global atmospheric model for climate prediction
- [**Huge Ensembles**](https://doi.org/10.5194/gmd-18-5575-2025) — design and analysis of very large ensemble hindcasts with SFNO-based models ([Part 1](https://doi.org/10.5194/gmd-18-5575-2025), [Part 2](https://doi.org/10.5194/gmd-18-5605-2025))
- [**FourCastNet 3**](https://arxiv.org/abs/2507.12144) — a geometric approach to probabilistic ML weather forecasting at scale, enabling fast and accurate large ensembles ([paper](https://arxiv.org/abs/2507.12144), [NVIDIA blog](https://developer.nvidia.com/blog/fourcastnet-3-enables-fast-and-accurate-large-ensemble-weather-forecasting-with-scalable-geometric-ml/))

![FourCastNet 3 ensemble rollout trained with Makani]({{ '/assets/img/research/fcn3_ens15.gif' | relative_url }})

*FourCastNet 3 ensemble rollout (15 members), trained with [Makani](https://github.com/NVIDIA/makani).*

<div class="publications">
{% bibliography -f {{ site.scholar.bibliography }} --group_by none -q @*[key^=bonev2025fourcastnet3]* %}
{% bibliography -f {{ site.scholar.bibliography }} --group_by none -q @*[key^=mahesh2025huge1]* %}
{% bibliography -f {{ site.scholar.bibliography }} --group_by none -q @*[key^=mahesh2025huge2]* %}
{% bibliography -f {{ site.scholar.bibliography }} --group_by none -q @*[key^=wattmeyer2023ace]* %}
{% bibliography -f {{ site.scholar.bibliography }} --group_by none -q @*[key^=bonev2023sfno]* %}
{% bibliography -f {{ site.scholar.bibliography }} --group_by none -q @*[key^=bonev2025attention]* %}
{% bibliography -f {{ site.scholar.bibliography }} --group_by none -q @*[key^=liu2024localno]* %}
{% bibliography -f {{ site.scholar.bibliography }} --group_by none -q @*[key^=berner2025principled]* %}
</div>

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
