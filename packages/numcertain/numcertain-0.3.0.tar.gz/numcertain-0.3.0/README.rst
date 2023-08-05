numcertain
==========

|code_ci| |docs_ci| |coverage| |pypi_version| |license|

This package provides a python and numpy data type (`uncertain`) which implements a
floating point value with quantified uncertainity, allowing for forward uncertainity
propagation of uncorrelated values.

============== ==============================================
PyPI           ``pip install numcertain``
Source code    https://github.com/DiamondLightSource/numcertain
Documentation  https://DiamondLightSource.github.io/numcertain
Releases       https://github.com/DiamondLightSource/numcertain/releases
============== ==============================================

Aritmatic Examples
------------------

A brief example of arithmatic with the provided uncertain data type is presented below:

.. code:: python

    a = uncertain(42.0, 5.0)
    b = uncertain(36, 12)

    print(a + b)
    print(a - b)
    print(a * b)
    print(a / b)

.. code::

    >> 78.0±13.0
    >> 6.0±13.0
    >> 1512.0±535.1784749034662
    >> 1.1666666666666667±0.41294635409218067

A brief example of arithmatic with numpy arrays with the uncertain dtype is presented
below:

.. code:: python

    a = array([uncertain(5.0, 3.0), uncertain(7.0, 6.0)])
    b = array([uncertain(12.0, 4.0), uncertain(24.0, 8.0)])

    print(a + b)
    print(a - b)
    print(a * b)
    print(a / b)

.. code::

    >> [uncertain(17.0, 5.0) uncertain(31.0, 10.0)]
    >> [uncertain(-7.0, 5.0) uncertain(-17.0, 10.0)]
    >> [uncertain(60.0, 41.182520563948) uncertain(168.0, 154.50566332662373)]
    >> [uncertain(0.4166666666666667, 0.2859897261385278) uncertain(0.2916666666666667, 0.268238998830944)]

Alternative Methods
-------------------

In order to accurately propagate uncertainties of related values the derivative of the
computed expectation must be known with respect to expectations it is comprised of.
Automatic differentiation (autodiff) provides a mechanism for computing the derivative
of arbitrary functions with respect to their components by exploiting the fact that all
codes, regardless of complexity, are reduced to a sequence of primative arithmetic
operations during execution for which the derivatives are known, by applying the chain
rule the overall derivative can be determined automatically.

The python package `Uncertainties`_ provides a python data type which performs autodiff
to propagate the corresponding uncertainity, unforunately due to Implementation as a
python object the library is non-performant when used for array math.

Whilst `Propagation of Uncertainty with autodiff`_, describes the use of autodiff
provided by the python package `JAX`_ in propagating uncertainities for array math.

.. _Uncertainties: https://uncertainties-python-package.readthedocs.io/en/latest/

.. _Propagation of Uncertainty with autodiff: http://theoryandpractice.org/intro-exp-phys-book/error-propagation/error_propagation_with_jax.html

.. _JAX: https://jax.readthedocs.io/en/latest/

.. |code_ci| image:: https://github.com/DiamondLightSource/numcertain/workflows/Code%20CI/badge.svg?branch=master
    :target: https://github.com/DiamondLightSource/numcertain/actions?query=workflow%3A%22Code+CI%22
    :alt: Code CI

.. |docs_ci| image:: https://github.com/DiamondLightSource/numcertain/workflows/Docs%20CI/badge.svg?branch=master
    :target: https://github.com/DiamondLightSource/numcertain/actions?query=workflow%3A%22Docs+CI%22
    :alt: Docs CI

.. |coverage| image:: https://codecov.io/gh/DiamondLightSource/numcertain/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/DiamondLightSource/numcertain
    :alt: Test Coverage

.. |pypi_version| image:: https://img.shields.io/pypi/v/numcertain.svg
    :target: https://pypi.org/project/numcertain
    :alt: Latest PyPI version

.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache License

..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

See https://DiamondLightSource.github.io/numcertain for more detailed documentation.
