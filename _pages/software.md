---
layout: page
permalink: /software/
title: software
description: Open-source software and libraries.
nav: true
nav_order: 3
wide_media: true
---

Some publicly available projects are listed below. More are on [GitHub](https://github.com/bonevbs).

## torch-harmonics

[![Build status](https://github.com/NVIDIA/torch-harmonics/actions/workflows/tests.yml/badge.svg)](https://github.com/NVIDIA/torch-harmonics/actions/workflows/tests.yml)
[![pypi](https://img.shields.io/pypi/v/torch_harmonics)](https://pypi.org/project/torch_harmonics/)

[torch-harmonics](https://github.com/NVIDIA/torch-harmonics) is a differentiable implementation of the spherical harmonic transform in PyTorch, originally developed for [Spherical Fourier Neural Operators](https://openreview.net/forum?id=TwsJ9IOZDx). It uses quadrature rules and FFTs for projections onto the harmonic basis and supports distributed computation across ranks.

[torch-harmonics](https://github.com/NVIDIA/torch-harmonics) has been used for differentiable PDE solvers and Spherical Fourier Neural Operators (SFNOs):

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

[Makani](https://github.com/NVIDIA/makani) is a library for GPU-accelerated machine-learning weather and climate models in PyTorch. It was used to train [FourCastNet](https://github.com/NVlabs/FourCastNet), [SFNO](https://developer.nvidia.com/blog/modeling-earths-atmosphere-with-spherical-fourier-neural-operators/), and [AFNO](https://arxiv.org/abs/2111.13587) on ERA5-scale data.

<img src="https://github.com/NVIDIA/modulus-makani/blob/main/images/sfno_rollout.gif?raw=true" alt="Makani SFNO weather rollout">

## neuraloperator

[neuraloperator](https://github.com/neuraloperator/neuraloperator) is a Python library for learning mappings between function spaces (neural operators).

## HssMatrices.jl

[![CI](https://github.com/bonevbs/HssMatrices.jl/workflows/CI/badge.svg)](https://github.com/bonevbs/HssMatrices.jl/actions)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4696465.svg)](https://doi.org/10.5281/zenodo.4696465)

[HssMatrices.jl](https://github.com/bonevbs/HssMatrices.jl) implements hierarchically semi-separable (HSS) matrices for PDE-related linear algebra, including compression, arithmetic, and visualization.

<img src="https://raw.githubusercontent.com/bonevbs/HssMatrices.jl/main/img/plotranks.svg" alt="HSS matrix rank structure">

## HierarchicalSolvers.jl

[HierarchicalSolvers.jl](https://github.com/bonevbs/HierarchicalSolvers.jl) is an approximate sparse direct solver in Julia using hierarchical low-rank structure, usable as a preconditioner with quasi-linear complexity.

## nodal-dg-extensions

[nodal-dg-extensions](https://github.com/bonevbs/nodal-dg-extension) extends the [nodal-dg](https://github.com/tcew/nodal-dg) Matlab library with continuous Galerkin methods on triangular meshes, sharing DG data structures for research and teaching.
