---
type: section
active: true

date: 2022-04-11

# Display name
title: Empirical flux calibration of Coronagraph observations

brief: A problem that requires flux calibration of low spectral resolution time series data.

keywords:
    - data-driven
    - modeling

preview-image: https://images.unsplash.com/photo-1630419493571-5066ebfb5889?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1726&q=80

---
[Matthias Samland](https://www2.mpia-hd.mpg.de/~samland/) (MPIA) came to discuss his calibration of coronagraphic observations with [SPHERE](https://www.eso.org/sci/facilities/paranal/instruments/sphere/overview.html). These are typically spectroscopic data (low-resolution) at a relatively high cadence with and without the occulation of the star for the characterization of planetary systems.

However in constrast with the direct observations, the spectra with the occulation have well established relative calibration but unknown absolute flux scaling. To solve the issue, the traditional way is to observe the star without the occulation before and after the scientific sequence to have an absolute flux reference. He is trying to use the three timeseries to implement a robust flux scaling factors (estimate and uncertainties). One of his first examples showed a an observation affected by clouds during the sequence. This problem is not a simple scaling constant number.

As many discussions, this discussion spent a significant time defining a common vocabulary and phrasing the question.

We discussed directions to explore. I offered to try toy models on my side.