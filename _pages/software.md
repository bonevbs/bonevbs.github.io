---
permalink: /software/
title: "Software"
excerpt: "Software"
author_profile: true
redirect_from: 
  - /software.html
---

I enjoy writing software and making it available, so it may benefit others. Some projects that are publicly avaiable and which I am proud of are listed here. A complete list is available on [my GitHub page](https://github.com/bonevbs).

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
