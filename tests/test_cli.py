"""Tests for the unified CLI."""

import json
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


# ================================================================
# JSON output mode tests (Phase 3)
# ================================================================

# --- JSON length happy path ---
def test_json_length_m_to_km():
    rc, out, err = run_cli("length", "1000", "m", "km", "--json")
    assert rc == 0
    assert err == ""
    data = json.loads(out)
    assert data == {
        "success": True,
        "category": "length",
        "value": 1000.0,
        "from_unit": "m",
        "to_unit": "km",
        "result": 1.0,
    }


def test_json_length_identity():
    rc, out, err = run_cli("length", "100", "m", "m", "--json")
    assert rc == 0
    data = json.loads(out)
    assert data["success"] is True
    assert data["category"] == "length"
    assert data["value"] == 100.0
    assert data["from_unit"] == "m"
    assert data["to_unit"] == "m"
    assert data["result"] == 100.0


# --- JSON weight happy path ---
def test_json_weight_kg_to_g():
    rc, out, err = run_cli("weight", "1", "kg", "g", "--json")
    assert rc == 0
    assert err == ""
    data = json.loads(out)
    assert data["success"] is True
    assert data["category"] == "weight"
    assert data["value"] == 1.0
    assert data["from_unit"] == "kg"
    assert data["to_unit"] == "g"
    assert data["result"] == 1000.0


def test_json_weight_lb_to_oz():
    rc, out, err = run_cli("weight", "1", "lb", "oz", "--json")
    assert rc == 0
    data = json.loads(out)
    assert data["success"] is True
    assert data["category"] == "weight"
    assert data["value"] == 1.0
    assert data["from_unit"] == "lb"
    assert data["to_unit"] == "oz"
    assert data["result"] == 16.0


# --- JSON zero value ---
def test_json_length_zero():
    rc, out, err = run_cli("length", "0", "m", "km", "--json")
    assert rc == 0
    data = json.loads(out)
    assert data["value"] == 0.0
    assert data["result"] == 0.0
    assert data["success"] is True


# --- JSON negative value ---
def test_json_weight_negative():
    rc, out, err = run_cli("weight", "-5", "kg", "g", "--json")
    assert rc == 0
    data = json.loads(out)
    assert data["value"] == -5.0
    assert data["result"] == -5000.0
    assert data["success"] is True


# --- Default non-JSON behavior preserved ---
def test_non_json_length_still_works():
    rc, out, err = run_cli("length", "1000", "m", "km")
    assert rc == 0
    assert out == "1.0"
    assert err == ""


def test_non_json_weight_still_works():
    rc, out, err = run_cli("weight", "1", "kg", "g")
    assert rc == 0
    assert out == "1000.0"
    assert err == ""


# --- JSON invalid unit ---
def test_json_length_invalid_unit():
    rc, out, err = run_cli("length", "10", "parsec", "m", "--json")
    assert rc == 1
    assert out == ""
    data = json.loads(err)
    assert data["success"] is False
    assert data["category"] == "length"
    assert data["value"] == 10.0
    assert data["from_unit"] == "parsec"
    assert data["to_unit"] == "m"
    assert data["result"] is None
    assert "error" in data
    assert "Unknown unit" in data["error"]


def test_json_weight_invalid_unit():
    rc, out, err = run_cli("weight", "10", "kg", "stone", "--json")
    assert rc == 1
    assert out == ""
    data = json.loads(err)
    assert data["success"] is False
    assert data["category"] == "weight"
    assert data["value"] == 10.0
    assert data["from_unit"] == "kg"
    assert data["to_unit"] == "stone"
    assert data["result"] is None
    assert "error" in data
    assert "Unknown unit" in data["error"]


# --- JSON invalid category (argparse usage error — deterministic nonzero exit) ---
def test_json_invalid_category():
    rc, out, err = run_cli("volume", "1", "l", "ml", "--json")
    assert rc != 0
    assert rc == 2  # argparse standard exit code for usage errors


# --- JSON missing subcommand (argparse usage error) ---
def test_json_missing_args():
    rc, out, err = run_cli("--json")
    assert rc != 0
    assert rc == 2
