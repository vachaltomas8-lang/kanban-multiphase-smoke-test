"""Tests for the unified CLI."""

import subprocess
import sys


def run_cli(*args):
    """Run the CLI module as a subprocess and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, "-m", "converter.cli", *args],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


# --- Length happy paths ---
def test_cli_length_identity():
    rc, out, err = run_cli("length", "100", "m", "m")
    assert rc == 0
    assert out == "100.0"


def test_cli_length_m_to_km():
    rc, out, err = run_cli("length", "1000", "m", "km")
    assert rc == 0
    assert out == "1.0"


def test_cli_length_km_to_m():
    rc, out, err = run_cli("length", "1", "km", "m")
    assert rc == 0
    assert out == "1000.0"


# --- Weight happy paths ---
def test_cli_weight_kg_to_g():
    rc, out, err = run_cli("weight", "1", "kg", "g")
    assert rc == 0
    assert out == "1000.0"


def test_cli_weight_lb_to_oz():
    rc, out, err = run_cli("weight", "1", "lb", "oz")
    assert rc == 0
    assert out == "16.0"


def test_cli_weight_g_to_kg():
    rc, out, err = run_cli("weight", "500", "g", "kg")
    assert rc == 0
    assert out == "0.5"


# --- Invalid category ---
def test_cli_invalid_category():
    rc, out, err = run_cli("volume", "1", "l", "ml")
    assert rc != 0


# --- Invalid unit errors ---
def test_cli_length_invalid_unit():
    rc, out, err = run_cli("length", "10", "parsec", "m")
    assert rc == 1
    assert "Error:" in err


def test_cli_weight_invalid_unit():
    rc, out, err = run_cli("weight", "10", "kg", "stone")
    assert rc == 1
    assert "Error:" in err


# --- Missing required arguments ---
def test_cli_no_args():
    rc, out, err = run_cli()
    assert rc != 0


def test_cli_missing_subcommand():
    rc, out, err = run_cli()
    assert rc != 0
