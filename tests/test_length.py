"""Tests for the length converter."""

import pytest
from converter.length import convert_length


# --- Identity conversions (same unit) ---
def test_identity_m():
    assert convert_length(100, "m", "m") == 100


def test_identity_km():
    assert convert_length(5, "km", "km") == 5


def test_identity_mi():
    assert convert_length(10, "mi", "mi") == 10


def test_identity_ft():
    assert convert_length(42, "ft", "ft") == 42


# --- Simple conversions ---
def test_m_to_km():
    assert convert_length(1000, "m", "km") == 1.0


def test_km_to_m():
    assert convert_length(1, "km", "m") == 1000


def test_ft_to_m():
    assert convert_length(3.28084, "ft", "m") == pytest.approx(1.0, rel=1e-4)


def test_m_to_ft():
    assert convert_length(1, "m", "ft") == pytest.approx(3.28084, rel=1e-4)


def test_mi_to_km():
    assert convert_length(1, "mi", "km") == pytest.approx(1.609344, rel=1e-4)


def test_km_to_mi():
    assert convert_length(1.609344, "km", "mi") == pytest.approx(1.0, rel=1e-4)


# --- Cross-unit conversions ---
def test_ft_to_mi():
    assert convert_length(5280, "ft", "mi") == pytest.approx(1.0, rel=1e-4)


def test_mi_to_ft():
    assert convert_length(1, "mi", "ft") == pytest.approx(5280.0, rel=1e-4)


def test_km_to_ft():
    assert convert_length(1, "km", "ft") == pytest.approx(3280.84, rel=1e-4)


def test_ft_to_km():
    assert convert_length(3280.84, "ft", "km") == pytest.approx(1.0, rel=1e-4)


# --- Edge cases ---
def test_zero():
    assert convert_length(0, "m", "km") == 0
    assert convert_length(0, "mi", "ft") == 0


def test_negative():
    assert convert_length(-100, "m", "km") == -0.1


def test_float_precision():
    result = convert_length(1.23456789, "m", "ft")
    assert result == pytest.approx(4.050419586614173, rel=1e-6)


# --- Error handling ---
def test_unknown_from_unit():
    with pytest.raises(ValueError, match="Unknown unit"):
        convert_length(10, "parsec", "m")


def test_unknown_to_unit():
    with pytest.raises(ValueError, match="Unknown unit"):
        convert_length(10, "m", "lightyear")
