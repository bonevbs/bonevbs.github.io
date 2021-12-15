---
permalink: /research/
title: "Research"
excerpt: "Research"
author_profile: true
redirect_from: 
  - /research.html
---

My research interests broadly revolve arounds mathematical algorithms. In particular, I am interested in *Machine Learning*, *Numerical Linear Algebra* and *Numerical algorithms for PDEs*. You can find out about my work in [my PhD dissertation](https://infoscience.epfl.ch/record/288711/files/EPFL_TH8641.pdf) and on [my Google scholar page]().

## Sparse direct solvers for wave problems

As part of my PhD thesis work, I have worked on direct solvers for wave problems, which aim to solve sparse linear systems of the form

$$A x = b, \nonumber$$

efficiently. This is done by exploiting physical properties of the underlying problem, which are encoded in the matrix $A$. More precisely, we use so-called *hierarchical matrices* to compress the dense fill-in that arises when $A$ is factored. This class of solvers can be used to solve problems such as the Helmholtz problem, which is illustrated below. These problems are typically difficult because of their indefinite nature and the spectrum of $A$. You can read more about our work on this topic in [our paper](https://infoscience.epfl.ch/record/279971?ln=en)

![Helmholtz solutions on a guitar](/files/guitars_hprecon.png)

## Discontinuous Galerkin methods for Tsunami simulations

As of now, the website is still under construction. In the meantime, you can check out some of my tsunami simulations. For more info, check out the publications page.

[![Watch the video](https://bonevbs.github.io/files/amr_showcase_prev.png)](/files/amr_showcase.mp4) 
[![Watch the video](https://bonevbs.github.io/files/tohoku_prev.png)](/files/tohoku.mp4)

[Find the paper here](https://infoscience.epfl.ch/record/232449?ln=en)

