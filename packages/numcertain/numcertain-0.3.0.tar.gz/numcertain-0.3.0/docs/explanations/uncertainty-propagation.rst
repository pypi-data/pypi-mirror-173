Uncertainty Propagation Explained
=================================

.. _uncertainty-propagation-in-numcertain:

In Numcertain
-------------

Numcertain performs uncertainty propagation for math operations under the assumption
that the values being combined are unrelated to one and other, as such the covariance
:math:`\sigma_{ab}` can be assumed to be zero, reducing the computation of propagated
uncertainity to simple functions of prior expectations and standard deviation.

The arethmetic operations implemented in Numcertain are detailed in the Implementations
table below:

.. list-table:: Arithmetic Implementations
    :align: center
    :widths: 50 50
    :header-rows: 1
    
    * - Expectation
      - Standard Deviation

    * - .. math::

            z=a+b

      - .. math::

            \sigma_z=\sqrt{\sigma_a^2 + \sigma_b^2}

    * - .. math::

            z=a-b

      - .. math::

            \sigma_z=\sqrt{\sigma_a^2 + \sigma_b^2}

    * - .. math::

            z=ab

      - .. math::

            \sigma_z=ab\sqrt{\frac{\sigma_a}{a}^2+\frac{\sigma_b}{b}^2}

    * - .. math::

            z=\frac{a}{b}

      - .. math::

            \sigma_z=\frac{a}{b}\sqrt{\frac{\sigma_a}{a}^2+\frac{\sigma_b}{b}^2}


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
