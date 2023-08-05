from math import isclose

import pytest

from numcertain import uncertain


def test_initialisation_two_float():
    value = uncertain(1.23, 0.45)
    assert 1.23 == value.nominal
    assert 0.45 == value.uncertainty


def test_initialisation_one_float():
    value = uncertain(1.23)
    assert 1.23 == value.nominal
    assert 0.00 == value.uncertainty


def test_initialisation_two_int():
    value = uncertain(5, 4)
    assert 5.0 == value.nominal
    assert 4.0 == value.uncertainty


def test_initialisation_one_int():
    value = uncertain(5)
    assert 5.0 == value.nominal
    assert 0.0 == value.uncertainty


@pytest.mark.parametrize(
    ["nominal_a", "nominal_b", "uncertainty_a", "uncertainty_b"],
    [(5.0, 5, 3.0, 3), (7.4, 7.4, 2.6, 2.6)],
)
def test_equality(nominal_a, nominal_b, uncertainty_a, uncertainty_b):
    a = uncertain(nominal_a, uncertainty_a)
    b = uncertain(nominal_b, uncertainty_b)
    assert a == b


@pytest.mark.parametrize(
    ["nominal_a", "nominal_b", "uncertainty_a", "uncertainty_b"],
    [(5.0, 7.0, 3.0, 3.0), (5.0, 5.0, 3.0, 4.0), (5.0, 7.0, 3.0, 4.0)],
)
def test_inequality(nominal_a, nominal_b, uncertainty_a, uncertainty_b):
    a = uncertain(nominal_a, uncertainty_a)
    b = uncertain(nominal_b, uncertainty_b)
    assert a != b


@pytest.mark.parametrize(
    [
        "nominal_a",
        "nominal_b",
        "nominal_expected",
        "uncertainty_a",
        "uncertainty_b",
        "uncertainty_expected",
    ],
    [(5.0, 12.0, 17.0, 3.0, 4.0, 5.0), (5.2, 4.8, 10.0, 0.8, 0.6, 1.0)],
)
def test_addition(
    nominal_a,
    nominal_b,
    nominal_expected,
    uncertainty_a,
    uncertainty_b,
    uncertainty_expected,
):
    a = uncertain(nominal_a, uncertainty_a)
    b = uncertain(nominal_b, uncertainty_b)
    result = a + b
    assert isclose(nominal_expected, result.nominal)
    assert isclose(uncertainty_expected, result.uncertainty)


@pytest.mark.parametrize(
    [
        "nominal_a",
        "nominal_b",
        "nominal_expected",
        "uncertainty_a",
        "uncertainty_b",
        "uncertainty_expected",
    ],
    [(12.0, 5.0, 7.0, 4.0, 3.0, 5.0), (5.2, 4.8, 0.4, 0.8, 0.6, 1.0)],
)
def test_subtraction(
    nominal_a,
    nominal_b,
    nominal_expected,
    uncertainty_a,
    uncertainty_b,
    uncertainty_expected,
):
    a = uncertain(nominal_a, uncertainty_a)
    b = uncertain(nominal_b, uncertainty_b)
    result = a - b
    assert isclose(nominal_expected, result.nominal)
    assert isclose(uncertainty_expected, result.uncertainty)


@pytest.mark.parametrize(
    [
        "nominal_a",
        "nominal_b",
        "nominal_expected",
        "uncertainty_a",
        "uncertainty_b",
        "uncertainty_expected",
    ],
    [(2.0, 3.0, 6.0, 1.6, 1.8, 6.0), (2.5, 1.0, 2.5, 4.0, 1.2, 5.0)],
)
def test_multiplication(
    nominal_a,
    nominal_b,
    nominal_expected,
    uncertainty_a,
    uncertainty_b,
    uncertainty_expected,
):
    a = uncertain(nominal_a, uncertainty_a)
    b = uncertain(nominal_b, uncertainty_b)
    result = a * b
    assert isclose(nominal_expected, result.nominal)
    assert isclose(uncertainty_expected, result.uncertainty)


@pytest.mark.parametrize(
    [
        "nominal_a",
        "nominal_b",
        "nominal_expected",
        "uncertainty_a",
        "uncertainty_b",
        "uncertainty_expected",
    ],
    [(3.0, 2.0, 1.5, 1.8, 1.6, 1.5), (2.5, 1.0, 2.5, 4.0, 1.2, 5.0)],
)
def test_division(
    nominal_a,
    nominal_b,
    nominal_expected,
    uncertainty_a,
    uncertainty_b,
    uncertainty_expected,
):
    a = uncertain(nominal_a, uncertainty_a)
    b = uncertain(nominal_b, uncertainty_b)
    result = a / b
    assert isclose(nominal_expected, result.nominal)
    assert isclose(uncertainty_expected, result.uncertainty)


@pytest.mark.parametrize(
    ["nominal", "uncertainty", "expected"],
    [(2.0, 0.5, 2), (1.2, 0.5, 1), (1.6, 0.5, 1)],
)
def test_cast_int(nominal, uncertainty, expected):
    a = uncertain(nominal, uncertainty)
    assert expected == (int)(a)


@pytest.mark.parametrize(
    ["nominal", "uncertainty", "expected"],
    [(2.0, 0.5, 2.0), (1.2, 0.5, 1.2), (1.6, 0.5, 1.6)],
)
def test_cast_float(nominal, uncertainty, expected):
    a = uncertain(nominal, uncertainty)
    assert expected == (float)(a)


def test_repr():
    a = uncertain(1.5, 0.7)
    assert "uncertain(1.5, 0.7)" == repr(a)


def test_str():
    a = uncertain(1.5, 0.7)
    assert "1.5±0.7" == str(a)
