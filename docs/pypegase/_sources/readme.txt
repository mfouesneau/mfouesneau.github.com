pyPEGASE v1.0
=============

This user-guide attempts to give you a quick start, and to help you understand
the structure of the code.

Contents of the directory
-------------------------

The package directory contains the following:

+-----------------+--------------------------------------------------------------------+
| `doc`           | Documentation folder                                               | 
+-----------------+--------------------------------------------------------------------+
| `examples`      | Contains a few examples                                            | 
+-----------------+--------------------------------------------------------------------+
| `external`      | Contains scripts to read from Pegase.2                             | 
+-----------------+--------------------------------------------------------------------+
| `imf`           | Initial Mass function classes and tools                            | 
+-----------------+--------------------------------------------------------------------+
| `include`       | Various Cython parts                                               | 
+-----------------+--------------------------------------------------------------------+
| `io`            | Tools to handle input/outputs                                      | 
+-----------------+--------------------------------------------------------------------+
| `isochrones`    | Package to interface with isochrones                               | 
+-----------------+--------------------------------------------------------------------+
| `junks`         | Some old scripts (will disappear in further versions)              | 
+-----------------+--------------------------------------------------------------------+
| `libs`          | Where the library files are (filters, vega, stellar libraries...)  | 
+-----------------+--------------------------------------------------------------------+
| `paper`         | Parts of the papers, and figure scripts                            | 
+-----------------+--------------------------------------------------------------------+
| `stellibs`      | Package interface to stellar libraries                             | 
+-----------------+--------------------------------------------------------------------+
| `tools`         | Some common tools                                                  | 
+-----------------+--------------------------------------------------------------------+
| `units`         | Package based on :class:`pint` to handle units throughout the code | 
+-----------------+--------------------------------------------------------------------+
| `config.py`     | A few global variables for the code to run properly                | 
+-----------------+--------------------------------------------------------------------+
| `extinction.py` | Extinction package                                                 | 
+-----------------+--------------------------------------------------------------------+
| `helpers.py`    | Helpers to handle common tasks                                     | 
+-----------------+--------------------------------------------------------------------+
| `nebular.py`    | Nebular continuum and emission package                             | 
+-----------------+--------------------------------------------------------------------+
| `phot.py`       | Package to provide photometric tools for convolution and filters   | 
+-----------------+--------------------------------------------------------------------+
| `ssp.py`        | Main functions to generate SSP models from different methods       | 
+-----------------+--------------------------------------------------------------------+
| `vega.py`       | Vega Package, an interface to Vega reference                       | 
+-----------------+--------------------------------------------------------------------+

	
.. todo::

        Content deeply changed and needs updates


Setup
-----

Setup assumes python is installed on your machine. 

.. warning::

        pyPEGASE  has been developed and tested with python 2.7., and python 3

All dependencies can be installed using `easy_install`, `pip`,...

Requirements
~~~~~~~~~~~~

* Standard python libraries:
        * pyfits or astropy  handles fits format
        * tables             handles HDF5 formats (mainly for spectral in/output)
        * numpy              numerical libraries 
        * scipy              numerical libraries 
        * matplotlib         making figures

* Not so standard libraries:
        * None

.. note::

        units are handled with an adaptation of `pint` (standalone version included)

Optional
~~~~~~~~
        
Optional libraries are not requested but highly recommended to take advantage of
the full speed of the code.

        * cython          Used to speed up parts of the code
                          If not present, the code will fallback into pure python
                          version.
                          (speeds up computations by ~20%)

        * ipython		For a more interactive usage of python

Customization
~~~~~~~~~~~~~

* Run 'make' to make use of cython code if cython is present.

* Edit config.py to customize the way you wish to run the codes.



Quick Start
-----------

SSP Generation Description
~~~~~~~~~~~~~~~~~~~~~~~~~~

A Single Stellar Population is a co-eval population, which means: 

1. Stellar masses are drawn from a given mass function (:math:`dN/dM`).
2. Each mass, :math:`m`, is associated with a temperature :math:`T_{eff}`, 
   a gravity :math:`\log(g)`, and a luminosity :math:`L`, 
   through an isochrone :math:`(t=age, Z=metallicity)`.
3. Each star referenced by :math:`(m, Z, \log(T_{eff}), \log(g), \log(L) )` is then
   associated with a spectral contribution :math:`( \lambda, F(\lambda) )`.
4. The integrated SED/spectrum is the sum of the individual stellar
   contributions.

The integrated stellar SED/spectrum can subsequently be modified, e.g., by
extinction and/or via the reprocessing of Lyman continuum emission into nebular
emission (continuum + lines). 
 


Calculation Modes
~~~~~~~~~~~~~~~~~

Our code provides three modes to generate an SSP model: **continuous**,
fully **discrete**, and **fast-discrete**.

* **continuous**: this mode assumes a continuously populated mass function.
  This is a good representation only for very massive stellar populations
  (strictly speaking for an infinite number of stars). This mode also represents
  mean properties of SSPs (beware: these mean properties are very unlikely, or
  even non-physical, for any single low mass cluster).
  The results computed in this mode are normalized to :math:`1\,M_\odot`.

* **discrete** and **fast-discrete**: both modes assume a discrete sampling of
  the mass function.  The results are provided for a given number of stars
  (user-defined).  The fast-discrete mode approximates the spectral contribution
  of each star in order to speed up calculations (<3% error in flux).


Shopping centers: Where to find the ingredients?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The code is organized in multiple sub-packages, each of which collects one
ingredient.
       
* imf:  defines common initial mass functions 
        * Kennicutt 
	* Kroupa2001 
	* Kroupa93 
	* MillerScalo 
	* Salpeter 
	* Scalo86 
	* Scalo98 

* isochrones:   interface isochrone libraries
        * Pegase
        * Padova2010
        * ezPadova

* stellibs:  interface spectral libraries
        * Pegase
        * Elodie
         
* nebular:     compute nebular components
        * Pegase

* extinctions:  provides extinction laws
	* Calzetti et al, 2000
	* Cardelli et al, 19xx
	* Fitzpatrick, 1999
	* Gordon et al., 2003, SMC bar
	* mixture of Fitzpatrick99 and Gordon03_SMCBar

* ssp.py provides main routines to produce SSP models
        * continuous
        * discrete
        * fastdiscrete


Quick start by example : 3 steps to build one "continuous" population
---------------------------------------------------------------------
All examples below are in demo.py (which also includes some figure scripts)

1. We need to define the population properties and ingredients. We select
        * age and metallicity
        * an IMF, for instance from Kroupa (2001)
        * a set of isochrones, Padova 2010 for instance
        * a spectral library, here BaSeL (Lejeune+1998)
        * a prescription for nebular emission (currently only the prescription from Pegase.2 is available, see Fioc+1997)

.. code-block:: python
        
        from pypegase.units import unit
        from pypegase import (imf, isochrones, stellibs, nebular)

        age = 1.e6 * unit['yr']  # default units assumed by the code
        Z   = 0.02   # solar
        oIMF = imf.Kroupa2001()
        ISO = isochrones.padova2010()
        oSL  = stellibs.BaSeL()
        oNEB     = nebular.pegase()
        fracNeb = 1.  # fraction of the ionizing photons that will
                      # be reprocessed into nebular emission

2. So far we did not select a computation mode. Let's do it now:

.. code-block:: python

        from pypegase.ssp import continuous

3. Launch the actual computations:

.. code-block:: python

        l, s, p = continuous(age, Z, oIMF, oISO, oSL, oNEB, fracNeb=fracNeb)

* `s`, provides the integrated spectrum of the population.
* `l`, contains the wavelengths at which the spectrum is provided.
* `p`, is a dictionary that collects the internal properties and intermediate steps of the computations.

Plot the result with your favourite python tool, for instance

.. code-block:: python

        import pylab
        pylab.loglog(l, s)


Some details, if you want to do it by hand instead of using a black box at step 3:

3.1 Selected isochrone :math:`(t,Z)` in the continuous prescription (this
prescription imposes the isochrone sampling too.)

.. code-block:: python

        stars = oISO._get_continuous_isochrone(t, Z)

.. note::

        the variable 'stars' is a table (:class:`pypegase.io.Table`) that
        contains all the needed the quantities (logT, logg, logL, Z, M, and
        more)

3.2 Compute the contribution of each bin of mass with respect to the IMF:
expected fraction of stars: :math:`dN = imf(M) * dM`

.. code-block:: python

        dN = oIMF.nstars( stars['logM'], dlogm=stars['dlogm'] )

.. note::  

        nstars does the computations in log(mass)

3.3 Interpolate the spectral library and compute the weight of each library star
 in the integrated spectrum of the isochrone population.

.. code-block:: python

       r = oSL.interpMany(stars['logT'], stars['logg'], Z, stars['logL'], weights=dN )

3.4 Sum the contributions from the stars in the library itself using the
interpolation weights `r`

.. code-block:: python

        s0 = oSL.genSpectrum(r)
        l0 = oSL.wavelength

3.5 Reprocess hydrogen ionizing photons NHI into nebular emission:

.. code-block:: python

        NHI  = oSL.genQ('NHI', r)
	l, s = oNEB.add_emission(l0, s0, NHI, fracNeb)

.. note::

        Units: fluxes are by default in Lsun/AA/1Msun (AA=Angstroem, Lsun=bolometric luminosity of the Sun).
        
        a keyword inLsun of genSpectrum is available to switch to ergs/s/AA/1Msun

        All functions are able to use units in most of their arguments when it
        makes sense. e.g., wavelength definitions supports units AA, um, nm, etc...


Quick start by example: 3 steps to build one "discrete" population
------------------------------------------------------------------

Quick start by example: 3 steps to build one "fast-discrete" population
-----------------------------------------------------------------------
This method relies on an approximation of each individual star by a precomputed
close replacement from a continuously sampled isochrone. As long as the
replacement is close from the actual desired star, the approximation is not bad.

There are two methods possible to make fast discrete populations. First, in the
same manner as the continuous method, we get a continuously sampled isochrone,
then instead of using the number of stars from the IMF predicitions, we draw
`Nstars` from the IMF and associate the closest mass on the isochrone, which
leads to a effective `dN` per mass-bin. Finally proceed as before to generate
the integrated spectrum.

Below would be a script applying this method

.. code-block:: python

        from pypegase.units import unit
        from pypegase import (imf, isochrones, stellibs, nebular)

        age = 1.e6 * unit['yr']  # default units assumed by the code
        nstars = 1e6  # number of stars in the population
        Z   = 0.02   # solar
        oIMF = imf.Kroupa2001()
        ISO = isochrones.padova2010()
        oSL  = stellibs.BaSeL()
        oNEB     = nebular.pegase()
        fracNeb = 1.  # fraction of the ionizing photons that will
                      # be reprocessed into nebular emission

        # get reference stars for a continuously sampled isochrone
        stars, logm_bins = iso._get_continuous_isochrone(_age, Z, ret_bins=True, dlogm=dlogm)
        m_bins = 10 ** logm_bins
        # find the maximum stellar mass possible at that given age
        logM = stars['logM']
        maxM = 10 ** stars['logM'].max()

        # generate random masses from the IMF
        _masses = imf.random(nstars)
        ind = (_masses > maxM)
        Mdead[k] = np.sum(_masses[ind])   # total mass above the isochrone limit
        Minit[k] = np.sum(_masses)
        Mmax[k] = np.max(_masses)

        # Approximation scheme
        dN = np.histogram( _masses, bins=m_bins)[0]

        # Generate the stellar spectrum
        r, l0, s0, NHI = genStellarSpectrum(stars, Z, sl, weights=(dN).astype(float))

        # add Nebular component
        l, s = neb.add_emission(l0 * unit['angstrom'], s0, NHI, fracNeb)


However we can also imagine precomputing the stars for a given isochrone (incl.
nebular component per star) and then proceed to a weighted sum. This method
becomes especially powerful when doing collections of models because the
isochrone and all the spectra are computed only once. Such a script would look
like:

.. code-block:: python

        from pypegase.units import unit
        from pypegase import (imf, isochrones, stellibs, nebular)

        age = 1.e6 * unit['yr']  # default units assumed by the code
        nstars = 1e6  # number of stars in the population
        Z   = 0.02   # solar
        oIMF = imf.Kroupa2001()
        ISO = isochrones.padova2010()
        oSL  = stellibs.BaSeL()
        oNEB     = nebular.pegase()
        fracNeb = 1.  # fraction of the ionizing photons that will
                      # be reprocessed into nebular emission

        # Continuously sample the corresponding isochrone
        # and simulate the continuous population
        stars, logm_bins = iso._get_continuous_isochrone(_age, Z, ret_bins=True, dlogm=dlogm)
        m_bins = 10 ** logm_bins

        # get the predicted number of stars per bin of mass on this isochrone
        # dN = imf.nstars(stars['logM'], ret_bins=False, edges=logm_bins)
        maxM = 10 ** stars['logM'].max()

        # compute all the individual spectra incl. neb component.
        # this will allow us to to a simple weighted sum.
        stars_lamb, stars_specs, NHI = genIndividualStellarSpectrum(stars, Z, sl, inLsun=inLsun)

        # add the nebular emission
        if (neb is not None) & (fracNeb > 0):
                if inLsun:
                    l, s = neb.add_emission_to_many(stars_lamb * unit['angstrom'],
                                                    stars_specs * Lsun,
                                                    NHI, fracNeb)
                    s /= Lsun
                else:
                    l, s = neb.add_emission_to_many(stars_lamb * unit['angstrom'],
                                                    stars_specs, NHI, fracNeb)
        else:
                l = stars_lamb
                s = stars_specs

        # Draw random masses 
        _masses = imf.random(nstars)

        # Approximation scheme
        _dN = histogram( _masses, m_bins)[0].astype(float)

        specs = (_dN[:, None] * s).sum(axis=0)
        Lbol = (10 ** stars['logL'] * _dN).sum()
        ind = (_masses > maxM)
        # total mass above the isochrone limit
        Mdead = np.sum(_masses[ind])
        Minit = np.sum(_masses)
        Mmax = np.max(_masses)

This second method is implemented in :func:`pypegase.ssp.fastdiscrete1` and thus
could be reduced to the following code:

.. code-block:: python

        from pypegase.units import unit
        from pypegase import (imf, isochrones, stellibs, nebular)
        from pypegase.ssp import fastdiscrete1

        age = 1.e6 * unit['yr']  # default units assumed by the code
        nstars = 1e6  # number of stars in the population
        Z   = 0.02   # solar
        oIMF = imf.Kroupa2001()
        ISO = isochrones.padova2010()
        oSL  = stellibs.BaSeL()
        oNEB     = nebular.pegase()
        fracNeb = 1.  # fraction of the ionizing photons that will
                      # be reprocessed into nebular emission

        # produce 20 populations of nstar stars given the rest of the assumptions
        l, s, p = fast_discrete(nstars, age, Z, imf, iso, sl, neb, fracNeb=fracneb,
                                nsamp=20, inLsun=False, with_units=True, full_outputs=False)




Customize your runs
-------------------

* Other inputs provided with this package :
        - In `imf`, you will find a variety of IMFs defined. Edit this file or derive
          :class:`IMF` to use your own favourite.
        - In `isochrones` two sets of isochrones are currently available :
          isochrone.Padova2010 (Girardi+2010), and isochrone.pegase (Fioc+1997),
          based on Padova 2004 with extension to TPAGB and reconnection to WD).
          we also provide an direct interface to the padova website CMD.
        - In `stellibs` two spectral libraries are currently available :
          stellibs.BaSeL (Lejeune+1998) and stellib.Elodie (as in PegaseHR, 
          Le Borgne+2004

* Redden the output spectra :
  [TBD]


Produce large collections of simulations
----------------------------------------


Compute colors
--------------


For those who wish to read/edit the codes
-----------------------------------------


Required acknowledgements
-------------------------

