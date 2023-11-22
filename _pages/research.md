---
permalink: /research/
title: "Research"
excerpt: "Research"
author_profile: true
redirect_from: 
  - /research.html
---

My research interests broadly revolve arounds mathematical algorithms. In particular, I am interested in *Machine Learning*, *Scientific Computing* and *Numerical algorithms* with a focus on *Numerical Linear Algebra*.

You can find out about my work on [my Google scholar page]().

## ML-based Weather prediction with Neural Operators

ML-based methods promise to greatly accelerate scientific computing. Recent advances in ML-based weather predicion have proven that these methods can compete with state-of-the-art classical weather prediction systems and even outperform them. However, how can we trust such models if they have been trained from data rather than from first-principles such as physical equations? One possible solution is to embue them with the same symmetries that we consider when formulating the physical equations that describe these. Our work on Spherical Fourier Neural Operators generalizes Fourier Neural Operators, a class of succesful models for modeling PDE systems, to spherical geometry. Find out more in [our paper](https://arxiv.org/abs/2306.03838) and a recently [published NVIDIA blogpost](https://developer.nvidia.com/blog/modeling-earths-atmosphere-with-spherical-fourier-neural-operators/).

![SFNO](https://developer-blogs.nvidia.com/wp-content/uploads/2023/07/figure_1.11-2.gif)


## Sparse direct solvers for wave problems

Sparse direct solvers aim to solve sparse linear systems of the form $A x = b$ efficiently, without relying on iterated matrix-vector multiplications such as Krylov subspace methods. This is particularly interesting for wave problems, where Krylov subspace methods typically require prohibitively many iterations to converge. Efficient sparse direct methods can be developed by exploiting physical properties of the underlying problem, which are encoded in the matrix $A$. More precisely, we use so-called *hierarchical matrices* to compress the dense fill-in that arises when $A$ is factored. This class of solvers can be used to solve problems such as the Helmholtz problem, which is illustrated below. These problems are typically difficult because of their indefinite nature and the spectrum of $A$. Not only can these methods solve the problem exactly, they can also serve as approximate solvers, which in turn can be used as preconditioners for iterative methods. You can read more about our work on this topic in [our paper](https://infoscience.epfl.ch/record/279971?ln=en) or in [my PhD dissertation](https://infoscience.epfl.ch/record/288711/files/EPFL_TH8641.pdf).


![Helmholtz solutions on a guitar](/files/guitars_hprecon.png)

## Discontinuous Galerkin methods for tsunami simulations

Discontinuous Galerkin methods are a promising class of methods for solving PDEs numerically. This is especially true for hyperbolic PDEs, where these methods achieve a high accuracy per degree of freedom. Moreover, they offer high locality and flexibility, which makes them especially suitable for high performance computing and large-scale problems such as weather prediction and Tsunami simulations. We demonstrate this by adapting the discontinuous Galerkin method to the simulation of global-scale Tsunami events. More precisely, we use the spherical formulation of the shallow water equations and adapt the discontinuous Galerkin formalism to these equations, dealing with important properties such as well-balancedness, wetting and drying, as well as mesh adaptivity. You can check out the videos below and find more details in our papers [here](https://infoscience.epfl.ch/record/232449?ln=en) and [here](https://doi.org/10.1016/j.ocemod.2019.101429).

[![Watch the video](https://bonevbs.github.io/files/amr_showcase_prev.png)](/files/amr_showcase.mp4) 
[![Watch the video](https://bonevbs.github.io/files/tohoku_prev.png)](/files/tohoku.mp4)

<!-- ### Machine learning for fluid simulations

Machine learning methods have been succesfully applied in computer vision, natural language processing and many other applications. Recently, machine learning approaches have started to show up in many scientific computing applications. In this project, we approached the problem of dimensionality reduction of fluid phenomena using neural networks. The central goal in this setting is to infer the result of a new fluid simulation, corresponding to a new set of parameters, given some reference simulations and parameters, without running the actual simulation, which is too costly. To do so, we model the outcome of the fluid simulation by using a deformation field, which distorts the reference solution into the new solution. These distortion fields are then modelled using neural networks. You can read more about our work in [our paper](https://openreview.net/pdf?id=HyeGBj09Fm).

[![Check out the video](http://img.youtube.com/vi/O8hvg0-buLE/0.jpg)](http://www.youtube.com/watch?v=O8hvg0-buLE)   -->
