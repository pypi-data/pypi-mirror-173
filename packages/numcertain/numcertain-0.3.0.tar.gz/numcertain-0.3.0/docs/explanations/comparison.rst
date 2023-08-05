Comparison of Uncertain Values Explained
========================================

Currently, the `uncertain` data type provides logical comparison for equality (i.e.
``eq`` & ``neq``). The implementations of such are detailed in the Implementations
table below:

.. list-table:: Comparison Implementations
    :align: center
    :widths: 50 50
    :header-rows: 1

    * - Operator
      - Condition

    * - Equal (EQ)
      - .. math::

            a = b \land \sigma_a = \sigma_b

    * - Not Equal (NE)
      - .. math::

            a \neq b \lor \sigma_a \neq \sigma_b