---
permalink: /software/
title: "Software"
excerpt: "Software"
author_profile: true
redirect_from: 
  - /software.html
---

I enjoy writing software and making it available, so it may benefit others. Some projects that are publicly avaiable and which I am proud of are listed here. A complete list is available on [my GitHub page](https://github.com/bonevbs).

## torch-harmonics

<!-- <a href="https://github.com/NVIDIA/torch-harmonics">
<p align="left">
    <img src="https://raw.githubusercontent.com/NVIDIA/torch-harmonics/main/images/logo/logo.png"  width="568">
</p>
</a> -->

`torch_harmonics` is a differentiable implementation of the Spherical Harmonic transform in PyTorch. It uses quadrature to compute the projection onto the associated Legendre polynomials and FFTs for the projection onto the harmonic basis. This algorithm tends to outperform others with better asymptotic scaling for most practical purposes.

<p align="left">
     <img src="https://media.githubusercontent.com/media/NVIDIA/torch-harmonics/main/images/zonal_jet.gif"  width="238">
     <img src="https://media.githubusercontent.com/media/NVIDIA/torch-harmonics/main/images/ginzburg-landau.gif"  width="238">
     <img src="https://media.githubusercontent.com/media/NVIDIA/torch-harmonics/main/images/allen-cahn.gif"  width="238">
 </p>


You can install `torch-harmonics` by running
```bash
git clone git@github.com:NVIDIA/torch-harmonics.git
pip install ./torch_harmonics
```

## HssMatrices.jl

[![Build status (Github Actions)](https://github.com/bonevbs/HssMatrices.jl/workflows/CI/badge.svg)](https://github.com/bonevbs/HssMatrices.jl/actions)
[![codecov.io](http://codecov.io/github/bonevbs/HssMatrices.jl/coverage.svg?branch=main)](http://codecov.io/github/bonevbs/HssMatrices.jl?branch=main)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4696465.svg)](https://doi.org/10.5281/zenodo.4696465)

HssMatrices is a Julia package for hierarchically semi-separable (HSS) matrices. These matrices are a type of hierarchically structured matrices, that arise in the context of solving PDEs numerically, among others. HssMatrices.jl is intendend to help users experiment with HSS matrices and related algorithms. HssMatrices.jl implements compression routines, HSS arithmetic, as well as helpful routines for clustering and visualization. These matrices have structures similar to the one in the illustration below.
[![HssMatrices.jl](https://raw.githubusercontent.com/bonevbs/HssMatrices.jl/main/img/plotranks.svg)](https://github.com/bonevbs/HssMatrices.jl)

You can install HssMatrices with the built in package manager by running
```julia
(@v1.6) pkg> add HssMatrices
```

## Extensions to nodal-dg

[nodal-dg](https://github.com/tcew/nodal-dg) is a Matlab library for nodal discontinuous Galerkin methods, originally written by Jan S. Hesthaven and Tim Warburton. [nodal-dg-extensions](https://github.com/bonevbs/nodal-dg-extension) exteds its capabilities to continuous Galerkin methods. It makes heavy use of the original discontinuous Galerkin datastructures for triangular meshes and extends them by adding a mapping which keeps track of duplicated points, which in the continuous Galerkin framework have to be mapped onto a single point. The resulting library is useful for research and development settings, especially if switching between discontinuous and continuous Galerkin methods is necessary, or, if arbitrary order continuous Galerkin methods are of interest. The illustration below shows the solution to a Helmholtz problem computed using the continuous Galerkin method.
[![helmholtz_plot1](/files/nodal-dg-plot2.png)](https://github.com/bonevbs/nodal-dg-extension)

As of now, the extension includes the following features:
* High-order continuous Galerkin (CG/FEM) method on triangular meshes using the nodal-dg datastructures
* DG method for the high-contrast Poisson problem
* IPDG method for linear elasticity in 2D
* Routines for generating a nested dissection for the structured elimination of the resulting matrices
* Plotting routines designed to visualize the results
* Test routines designed to check behaviour under h- and p-refinement
