How to use the Uncertain type
=============================

The `uncertain` type is implemented as a CPython extension type, as such it may be used
like any other native python type. The following import is required to follow the
examples presented in this section:

.. code:: python

    from numcertain import uncertain


.. _use-uncertain-type-creating:

Creating an uncertain value
---------------------------

An uncertain value may be created with use of the `uncertain` object imported via
`numcertain`. Several examples of uncertain value instantiation are shown below.

Ideally, an uncertain value is created by passing a expectation and standard deviation
as floating point values. Thus an uncertain value with an expectation of :code:`42` and
standard deviation of :code:`12.7` should be created as follows:

.. code:: python

    x = uncertain(42.0, 12.7)
    print(x)

.. code::

    >> 42.0±12.7

If given two integer values, the library will cast these to floating point numbers. As
such, an uncertain value with an expectation of ``36`` and standard deviation of
:code:`8` could be created as follows:

.. code:: python

    x = uncertain(36, 8)
    print(x)

.. code::

    >> 36.0±8.0

Uncertain values may also be created with a single value, in which case it is treated
as the expectation and a standard deviation of zero is applied. E.g.:

.. code:: python

    x = uncertain(87)
    print(x)

.. code::

    >> 87.0±0.0

.. _use-uncertain-type-casting:


Converting to an uncertain value
--------------------------------

It is also possible to convert pre-existing floating point or integer values to the
uncertain data type via casting, in such cases the value is treated as the expectation
and a standard deviation of zero is applied. This is performed with the usual python
syntax, as:

.. code:: python

    x = 3.14
    y = (uncertain)(x)
    print(y)

.. code::

    >> 3.14±0.0


Displaying an uncertain value
-----------------------------

Printing an uncertain value will use the built in string representation (``__str__``)
which stringifies the value in the format ``expectance`` ± ``standard deviation``, as:

.. code:: python

    x = uncertain(42.0, 12.7)
    print(x)

Which will produce the following output:

.. code::

    >> 42.0±12.7

You may also wish to display the full object representation (``__repr__``) of an
uncertain value, this can be done by calling the ``repr`` method on the value, as:

.. code:: python

    x = uncertain(42.0, 12.7)
    print(repr(x))

Which will produce the following output:

.. code::

    >> uncertain(42.0, 12.7)


Retrieving expectance or standard deviation
-------------------------------------------

It is likely you will wish at some point to reteieve either the expectance or standard
deviation of the uncertain value in isolation; In order to do this we simply query the
``nominal`` and ``uncertainity`` attributes respectively, as:

.. code:: python

    x = uncertain(42.0, 12.7)
    print(x.nominal)
    print(x.uncertainty)

.. code:: python

    >> 42.0
    >> 12.7

Arithmetic with uncertain values
--------------------------------

It is likely you will wish to perform arethemtic operations on uncertain values, these
may be performed as normal for numeric python types (i.e. with use of the ``+``, ``-``,
``*`` & ``/`` operators). An example of such is shown below:

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

.. note::

    See: :ref:`Uncertainty Propagation Explained
    <uncertainty-propagation-in-numcertain>` for details of how the uncertainty
    propagation math is performed.
