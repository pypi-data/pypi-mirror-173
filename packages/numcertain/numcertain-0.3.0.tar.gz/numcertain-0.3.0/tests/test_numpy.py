from math import isclose
from typing import cast

from numpy import array, float32, float64, int16, int32, int64

from numcertain import nominal, uncertain, uncertainty


def test_initialisation_uncertain():
    a = array([uncertain(1.0, 0.2), uncertain(1.6, 0.8)])
    assert uncertain(1.0, 0.2) == a[0]


def test_cast_from_int16():
    a = array([1, 2, 3], dtype=int16).astype(uncertain)
    assert uncertain(1, 0) == a[0]


def test_cast_from_int32():
    a = array([1, 2, 3], dtype=int32).astype(uncertain)
    assert uncertain(1, 0) == a[0]


def test_cast_from_int64():
    a = array([1, 2, 3], dtype=int64).astype(uncertain)
    assert uncertain(1, 0) == a[0]


def test_cast_from_float32():
    a = array([1.8, 2.4, 3.6], dtype=float32).astype(uncertain)
    assert isclose(1.8, cast(uncertain, a[0]).nominal, rel_tol=1e-7)
    assert 0 == cast(uncertain, a[0]).uncertainty


def test_cast_from_float64():
    a = array([1.8, 2.4, 3.6], dtype=float64).astype(uncertain)
    assert isclose(1.8, cast(uncertain, a[0]).nominal)
    assert 0 == cast(uncertain, a[0]).uncertainty


def test_equality():
    a = array([uncertain(1.2, 0.6), uncertain(1.5, 0.3)])
    b = array([uncertain(1.2, 0.6), uncertain(1.5, 0.3)])
    assert (a == b).all()


def test_inequality():
    a = array([uncertain(1.2, 0.6), uncertain(1.5, 0.3)])
    b = array([uncertain(1.4, 0.6), uncertain(1.5, 0.4)])
    assert (a != b).all()


def test_addition():
    a = array([uncertain(1.6, 0.8), uncertain(2.4, 1.2)])
    b = array([uncertain(1.2, 0.6), uncertain(1.5, 0.9)])
    result = a + b
    assert isclose(2.8, cast(uncertain, result[0]).nominal, rel_tol=1e-7)
    assert isclose(1.0, cast(uncertain, result[0]).uncertainty, rel_tol=1e-7)


def test_subtraction():
    a = array([uncertain(1.6, 0.8), uncertain(2.4, 1.2)])
    b = array([uncertain(1.2, 0.6), uncertain(1.5, 0.9)])
    result = a - b
    assert isclose(0.4, cast(uncertain, result[0]).nominal, rel_tol=1e-7)
    assert isclose(1.0, cast(uncertain, result[0]).uncertainty, rel_tol=1e-7)


def test_multipliction():
    a = array([uncertain(2.0, 1.6), uncertain(2.4, 1.2)])
    b = array([uncertain(3.0, 1.8), uncertain(1.5, 0.9)])
    result = a * b
    assert isclose(6.0, cast(uncertain, result[0]).nominal, rel_tol=1e-7)
    assert isclose(6.0, cast(uncertain, result[0]).uncertainty, rel_tol=1e-7)


def test_division():
    a = array([uncertain(3.0, 1.8), uncertain(2.4, 1.2)])
    b = array([uncertain(2.0, 1.6), uncertain(1.5, 0.9)])
    result = a / b
    assert isclose(1.5, cast(uncertain, result[0]).nominal, rel_tol=1e-7)
    assert isclose(1.5, cast(uncertain, result[0]).uncertainty, rel_tol=1e-7)


def test_cast_to_int16():
    a = array([uncertain(1.0, 0.2), uncertain(1.6, 0.8)]).astype(int16)
    assert (array([1, 1], dtype=int16) == a).all()


def test_cast_to_int32():
    a = array([uncertain(1.0, 0.2), uncertain(1.6, 0.8)]).astype(int32)
    assert (array([1, 1], dtype=int32) == a).all()


def test_cast_to_int64():
    a = array([uncertain(1.0, 0.2), uncertain(1.6, 0.8)]).astype(int64)
    assert (array([1, 1], dtype=int64) == a).all()


def test_cast_to_float32():
    a = array([uncertain(1.0, 0.2), uncertain(1.6, 0.8)]).astype(float32)
    assert (array([1.0, 1.6], dtype=float32) == a).all()


def test_cast_to_float64():
    a = array([uncertain(1.0, 0.2), uncertain(1.6, 0.8)]).astype(float64)
    assert (array([1.0, 1.6], dtype=float64) == a).all()


def test_get_nominal():
    a = array([uncertain(1.0, 0.2), uncertain(1.6, 0.8)])
    assert (array([1.0, 1.6]) == nominal(a)).all()


def test_get_uncertainty():
    a = array([uncertain(1.0, 0.2), uncertain(1.6, 0.8)])
    assert (array([0.2, 0.8]) == uncertainty(a)).all()
