How to use the Uncertain dtype with numpy
=========================================

The `uncertain` type is implemented as a CPython extension type and a Numpy user
defined data type, as such it may be used like any other numpy array ``dtype``. The
following imports are required to follow the examples presented in this section:

.. code:: python

    from numpy import array
    from numcertain import uncertain, nominal, uncertainties


Creating an array of uncertain values
-------------------------------------

An array of uncertain values may be created with use of the Numpy `array` function
and the Numcertain ``uncertain`` object. This is performed by passing a list of
``uncertain`` objects, created as as described in  to the numpy ``array`` function, as:

.. code:: python

    x = array([uncertain(42.0, 12.7), uncertain(36, 8), uncertain(87)])
    print(x)

.. code::

    >> [uncertain(42.0, 12.7) uncertain(36.0, 8.0) uncertain(87.0, 0.0)]

.. note::

    See :ref:`How to use the Uncertain Type <use-uncertain-type-creating>` for details
    of how an ``uncertain`` value is created.

Converting an array to the uncertain dtype
------------------------------------------

An array of integer or floating point values may be cast into the ``uncertain`` dtype
with use of the ``astype`` method of the numpy array, with ``uncertain`` as the sole
argument. The syntax for which is shown below:

.. code:: python

    x = array([1, 2, 3]).astype(uncertain)
    print(x)

.. code::

    >> [uncertain(1.0, 0.0) uncertain(2.0, 0.0) uncertain(3.0, 0.0)]

.. note::

    See :ref:`How to use the Uncertain Type <use-uncertain-type-casting>` for details
    of how casting to an ``uncertain`` value is performed.


Arithmetic with uncertain values
--------------------------------

It is likely you will wish to perform arethemtic operations on uncertain values, these
may be performed as normal for numeric python types (i.e. with use of the ``+``, ``-``,
``*`` & ``/`` operators). An example of such is shown below:

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

.. note::

    See: :ref:`Uncertainty Propagation Explained
    <uncertainty-propagation-in-numcertain>` for details of how the uncertainty
    propagation math is performed.


Retrieving expectance or standard deviation
-------------------------------------------

A pair of numpy Universal Functions (ufuncs) are supplied to allow retrieval of the
nominal values and uncertainties of an array of uncertain values. The use of these is
demonstrated below:

.. code:: python

    a = array([uncertain(5.0, 3.0), uncertain(7.0, 6.0)])

    print(nominal(a))
    print(uncertainties(a))

.. code::

    >> [5.0, 7.0]
    >> [3.0, 6.0]
