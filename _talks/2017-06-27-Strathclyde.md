---
title: "Large-Scale Tsunami Simulations using the Discontinuous Galerkin Method"
collection: talks
type: "Talk"
permalink: /talks/2017-06-27-Strathclyde
venue: "27th Biennial Conference on Numerical Analysis, Glasgow, UK"
date: 2017-06-27
location: "Glasgow, UK"
---

Discontinuous Galerkin methods have desirable properties, which make them suitable for the com- putation of wave problems. Being parallelizable and hp-adaptive makes them attractive for the simulation of large-scale tsunami propagation. In order to retrieve such a scheme, we formulate the shallow water equations on the spherical shell and apply the discontinuous Galerkin discretiza- tion to construct a numerical method which is able to handle the effects of curvature and Coriolis forces naturally. Common challenges in solving the shallow water equations numerically are well- balancedness and wetting/drying. To overcome this, we utilize a method based on a timestep restriction, which guarantees the positivity of the numerical solution. Moreover, we show that our discretization yields a well-balanced numerical scheme. In this talk we will present our method as well as the numerical results, that we have obtained with our implementation.
