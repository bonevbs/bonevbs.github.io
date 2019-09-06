---
title: "Discontinuous Galerkin scheme for the spherical shallow water equations with applications to tsunami modeling and prediction"
collection: publications
permalink: /publication/2018-dg-tsunami
excerpt: 'We present a novel high-order discontinuous Galerkin discretization for the spherical shallow water equations, able to handle wetting/drying and non-conforming, curved meshes in a well-balanced manner. This requires a well-balanced discretization, that cannot rely on exact quadrature, due to the curved mesh. Using the strong form of the discontinuous Galerkin discretization, we achieve a splitting of the well-balanced condition into individual problems for the flux and volume terms, which has significant advantages: It allows for the construction of non-conforming, well-balanced flux discretizations, i.e. we can perform non- conforming mesh refinement while preserving the well-balanced property of the scheme. More importantly, this approach enables the development of a new method for handling wet/dry transitions. In contrast to other wetting/drying methods, it is well-balanced and able to handle wetting/drying robustly at any polynomial order, without the introduction of physical model assumptions such as viscosity, artificial porosity or cancellation of gravity. We perform a series of one-dimensional tests and analyze the properties of our scheme. In order to validate our method for the simulation of large-scale tsunami events on the rotating sphere, we perform numerical simulations of the 2011 Tohoku tsunami and compare our results to real-world buoy data. The method is able to predict arrival times and wave amplitudes accurately even over long distances. This indicates that our method accurately captures all physical phenomena relevant to the long-term evolution of tsunami waves.'
date: 2009-10-01
venue: 'Journal of Computational Physics'
paperurl: 'http://dx.doi.org/10.1016/j.jcp.2018.02.008'
citation: 'Bonev, Boris; Hesthaven, Jan S.; Giraldo, Francis X.; Kopera, Michal A. (2018). &quot;Paper Title Number 1.&quot; <i>Journal of Computational Physics</i>. 362, 425-448.'
---
This paper is about Tsunami simulations using a Discontinuous Galerkin method for the Spherical Shallow Water Equations. We present a method that is well-balanced even when wetting-drying and dynamically adaptive meshing is considered.

[Download paper here](https://infoscience.epfl.ch/record/232449?ln=en)

Recommended citation: Bonev, Boris; Hesthaven, Jan S.; Giraldo, Francis X.; Kopera, Michal A. (2018). &quot;Paper Title Number 1.&quot; <i>Journal of Computational Physics</i>. 362, 425-448.
