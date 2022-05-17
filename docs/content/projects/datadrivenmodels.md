---
type: gallery-details
active: true

# Display name
title: Data-driven Stellar Models

url: https://www.cosmos.esa.int/web/gaia/home
brief: Going beyond the synthetic stellar atmospheres combined with isochrones and extinction curves.

keywords:
    - data-driven
    - astrophysical parameters

preview-image: https://s3.amazonaws.com/aasie/images/0004-637X/907/1/57/apjabd1ddf1_hr.jpg

# Image slideshow
images:
    - url: https://s3.amazonaws.com/aasie/images/0004-637X/907/1/57/apjabd1ddf1_hr.jpg
      caption: |
        From [Green et al. 2021](https://ui.adsabs.harvard.edu/abs/2021ApJ...907...57G/abstract),
        Directed graph of our model of stellar magnitudes and colors. Shaded nodes represent _observed_ quantities (i.e., likelihoods). Our model parameters are the neural network weights and biases that control the mapping from stellar type to absolute magnitudes, as well as the neural network weights and biases that control the dependence of the extinction vector on stellar type. The extinction vector controls the direction in magnitude space that increasing dust density moves stars, and is only weakly dependent on stellar type, due to strong regularization of the weights WR. The constant matrix B, given by Equation (5), transforms the vector m, containing apparent magnitudes, to the vector c, containing one apparent magnitude and (# of bands)−1 colors.
    - url: https://s3.amazonaws.com/aasie/images/0004-637X/907/1/57/apjabd1ddf6_hr.jpg
      caption: |
        From [Green et al. 2021](https://ui.adsabs.harvard.edu/abs/2021ApJ...907...57G/abstract),
        Gaia color–magnitude diagrams of observed (left) and predicted zero-reddening (right) photometry. The average learned reddening vector for the Gaia filters is shown in red.

information: |
    ### Data driven stellar models

    * Going beyond the synthetic stellar atmospheres combined with isochrones and extinction curves.

---

### Goals of data driven models

We are now in an era where data are so precise that are physical models are systematically significantly wrong.

In [Green et al. 2021](https://ui.adsabs.harvard.edu/abs/2021ApJ...907...57G/abstract), we developed a data-driven model to map stellar parameters ($T_{eff}$,  $\log g$  , and  [Fe/H]) accurately and precisely to broadband stellar photometry. This model must, and does, simultaneously constrain the passband-specific dust reddening vector in the Milky Way, $R$. The model uses a neural network to learn the (de-reddened) absolute magnitude in one band and colors across many bands, given stellar parameters from spectroscopic surveys and parallax constraints from Gaia. To demonstrate the effectiveness of this approach, we train our model on a data set with spectroscopic parameters from LAMOST, APOGEE, and GALAH, Gaia parallaxes, and optical and near-infrared photometry from Gaia, Pan-STARRS 1, Two Micron All Sky Survey and Wide-field Infrared Survey Explorer. Testing the model on these data sets leads to an excellent fit and a precise—and by construction—accurate prediction of the color-magnitude diagrams in many bands. This flexible approach rigorously links spectroscopic and photometric surveys, and also results in an improved, Teff-dependent R. As such, it provides a simple and accurate method for predicting photometry in stellar evolutionary models. Our model will form a basis to infer stellar properties, distances, and dust extinction from photometric data, which should be of great use in 3D mapping of the Milky Way.
Our trained model can be obtained at [doi:10.5281/zenodo.3902382](https://zenodo.org/record/3922300#.YoNYi5NBzlw).