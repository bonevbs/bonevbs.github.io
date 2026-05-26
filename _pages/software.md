---
layout: page
permalink: /software/
title: Software
nav: true
nav_order: 3
wide_media: true
---

Below are open-source libraries I have contributed to or maintain. Additional code and experiments are on [GitHub](https://github.com/bonevbs).

## torch-harmonics

[![tests](https://github.com/NVIDIA/torch-harmonics/actions/workflows/tests.yml/badge.svg)](https://github.com/NVIDIA/torch-harmonics/actions/workflows/tests.yml)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/bonevbs/5d08af0f7f08ac865934a1929f198ffd/raw/torch_harmonics_coverage.json&cacheSeconds=3600)](https://github.com/NVIDIA/torch-harmonics)
[![pypi](https://img.shields.io/pypi/v/torch_harmonics)](https://pypi.org/project/torch_harmonics/)

[torch-harmonics](https://github.com/NVIDIA/torch-harmonics) is a differentiable implementation of the spherical harmonic transform in PyTorch. It was originally developed for [Spherical Fourier Neural Operators](https://openreview.net/forum?id=TwsJ9IOZDx) and is now used more broadly for global weather models, differentiable PDE solvers, and operator learning on the sphere. The library combines quadrature rules with FFT-based projections onto the harmonic basis and supports distributed computation across GPU ranks.

Examples below include SFNO weather rollouts, a zonal-jet simulation, and an Allen–Cahn solve on the sphere:

<div class="media-grid media-grid--3">
  <img src="https://media.githubusercontent.com/media/NVIDIA/torch-harmonics/main/images/sfno.gif" alt="SFNO rollout">
  <img src="https://media.githubusercontent.com/media/NVIDIA/torch-harmonics/main/images/zonal_jet.gif" alt="Zonal jet simulation">
  <img src="https://media.githubusercontent.com/media/NVIDIA/torch-harmonics/main/images/allen-cahn.gif" alt="Allen-Cahn simulation">
</div>

```bash
pip install torch-harmonics
```

## makani

[![tests](https://github.com/NVIDIA/makani/actions/workflows/tests.yml/badge.svg)](https://github.com/NVIDIA/makani/actions/workflows/tests.yml)

[Makani](https://github.com/NVIDIA/makani) is a training framework for large machine-learning weather and climate models in PyTorch. It scales from a single GPU to thousands on ERA5-scale and similar reanalysis datasets, with data pipelines, model configurations, and distributed training utilities built in. Makani was used to train [FourCastNet](https://github.com/NVlabs/FourCastNet), [SFNO](https://developer.nvidia.com/blog/modeling-earths-atmosphere-with-spherical-fourier-neural-operators/), and [AFNO](https://arxiv.org/abs/2111.13587).

<img class="figure-half-75" src="https://github.com/NVIDIA/modulus-makani/blob/main/images/sfno_rollout.gif?raw=true" alt="Makani SFNO weather rollout">

## neuraloperator

[![PyPI](https://img.shields.io/pypi/v/neuraloperator)](https://pypi.org/project/neuraloperator/)
[![tests](https://github.com/NeuralOperator/neuraloperator/actions/workflows/test.yml/badge.svg)](https://github.com/NeuralOperator/neuraloperator/actions/workflows/test.yml)

<img class="figure-line-75" src="{{ '/assets/img/software/neuraloperator_logo_long.png' | relative_url }}" alt="NeuralOperator logo">

[NeuralOperator](https://github.com/NeuralOperator/neuraloperator) is a PyTorch library for learning mappings between function spaces—neural operators that generalize across resolutions and domains. It ships the reference implementations of Fourier Neural Operators and related architectures (FNO, tensorized TFNO, Galerkin-style layers), together with training utilities and PDE benchmark examples. Operators are resolution invariant: a model trained on one grid can be applied on another without retraining. The project is part of the [PyTorch ecosystem](https://pytorch.org/blog/neuraloperatorjoins-the-pytorch-ecosystem); see the [documentation](https://neuraloperator.github.io/dev/index.html) and the [practical guide](https://arxiv.org/abs/2512.01421) for tutorials. I contribute to the core library and use it across several operator-learning projects.

```bash
pip install neuraloperator
```

## HssMatrices.jl

[![CI](https://github.com/bonevbs/HssMatrices.jl/workflows/CI/badge.svg)](https://github.com/bonevbs/HssMatrices.jl/actions)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4696465.svg)](https://doi.org/10.5281/zenodo.4696465)

[HssMatrices.jl](https://github.com/bonevbs/HssMatrices.jl) implements hierarchically semi-separable (HSS) matrices in Julia for PDE-related linear algebra. HSS compression represents dense blocks arising in sparse factorizations by low-rank structure, enabling fast matrix–vector products and approximate arithmetic. The package includes construction, multiplication, factorization hooks, and tools to visualize rank structure—useful when developing hierarchical preconditioners for wave problems.

<img class="figure-half-75" src="https://raw.githubusercontent.com/bonevbs/HssMatrices.jl/main/img/plotranks.svg" alt="HSS matrix rank structure">

## HierarchicalSolvers.jl

[HierarchicalSolvers.jl](https://github.com/bonevbs/HierarchicalSolvers.jl) is an approximate sparse direct solver in Julia that exploits hierarchical low-rank structure during factorization. Combined with nested-dissection orderings, it achieves quasi-linear complexity on many wave and Helmholtz problems and can be used as a robust preconditioner inside Krylov iterations. This code grew out of my [PhD work]({{ '/files/thesis_compressed.pdf' | relative_url }}) on scalable solvers for time-harmonic wave equations.

## nodal-dg-extensions

[nodal-dg-extensions](https://github.com/bonevbs/nodal-dg-extension) extends the [nodal-dg](https://github.com/tcew/nodal-dg) Matlab library with continuous Galerkin (CG) discretizations on triangular meshes, alongside the existing discontinuous Galerkin (DG) machinery. The design reuses the same nodal data structures so CG and DG variants can be compared in a unified framework—mainly for research prototypes and teaching.
