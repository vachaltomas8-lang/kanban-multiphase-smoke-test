"""Tests for the weight converter."""

import pytest
from converter.weight import convert_weight


# --- Identity conversions (same unit) ---
def test_identity_kg():
    assert convert_weight(10, "kg", "kg") == 10


def test_identity_g():
    assert convert_weight(500, "g", "g") == 500


def test_identity_lb():
    assert convert_weight(2.5, "lb", "lb") == 2.5


def test_identity_oz():
    assert convert_weight(16, "oz", "oz") == 16


# --- Simple conversions ---
def test_kg_to_g():
    assert convert_weight(1, "kg", "g") == 1000.0


def test_g_to_kg():
    assert convert_weight(1000, "g", "kg") == 1.0


def test_kg_to_lb():
    # 1 kg = 2.20462... lb
    assert convert_weight(1, "kg", "lb") == pytest.approx(2.2046226218487757, rel=1e-6)


def test_lb_to_kg():
    # 1 lb = 0.45359237 kg
    assert convert_weight(1, "lb", "kg") == pytest.approx(0.45359237, rel=1e-6)


# --- Cross-unit conversions ---
def test_lb_to_oz():
    # 1 lb = 16 oz
    assert convert_weight(1, "lb", "oz") == pytest.approx(16.0, rel=1e-6)


def test_oz_to_lb():
    # 16 oz = 1 lb
    assert convert_weight(16, "oz", "lb") == pytest.approx(1.0, rel=1e-6)


def test_g_to_oz():
    # 1 g = 0.03527396... oz (1 / 28.349523125)
    assert convert_weight(1, "g", "oz") == pytest.approx(0.03527396194958041, rel=1e-6)


def test_oz_to_g():
    # 1 oz = 28.349523125 g
    assert convert_weight(1, "oz", "g") == pytest.approx(28.349523125, rel=1e-6)


# --- Edge cases ---
def test_weight_zero():
    assert convert_weight(0, "kg", "g") == 0
    assert convert_weight(0, "lb", "oz") == 0
    assert convert_weight(0, "g", "kg") == 0


def test_weight_negative():
    assert convert_weight(-1, "kg", "g") == -1000.0
    assert convert_weight(-2, "lb", "oz") == pytest.approx(-32.0, rel=1e-6)


def test_weight_precision():
    # Round-trip: kg -> lb -> kg should recover original
    converted = convert_weight(1.23456789, "kg", "lb")
    back = convert_weight(converted, "lb", "kg")
    assert back == pytest.approx(1.23456789, rel=1e-6)


# --- Error handling ---
def test_weight_unknown_from_unit():
    with pytest.raises(ValueError, match="Unknown unit"):
        convert_weight(10, "stone", "kg")


def test_weight_unknown_to_unit():
    with pytest.raises(ValueError, match="Unknown unit"):
        convert_weight(10, "kg", "tonne")
