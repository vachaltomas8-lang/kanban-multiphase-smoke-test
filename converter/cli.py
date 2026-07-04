"""Unified CLI for length and weight conversions.

Usage:
    python3 -m converter.cli length <value> <from_unit> <to_unit>
    python3 -m converter.cli weight <value> <from_unit> <to_unit>
"""

import argparse
import json
import sys

from converter.length import convert_length
from converter.weight import convert_weight


def _json_error(category, value, from_unit, to_unit, error_msg):
    """Return JSON error payload string."""
    payload = {
        "success": False,
        "category": category,
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "result": None,
        "error": error_msg,
    }
    return json.dumps(payload)


def _json_success(category, value, from_unit, to_unit, result):
    """Return JSON success payload string."""
    payload = {
        "success": True,
        "category": category,
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "result": result,
    }
    return json.dumps(payload)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert between length and weight units."
    )
    subparsers = parser.add_subparsers(dest="category", required=True)

    # --- length subcommand ---
    length_parser = subparsers.add_parser("length", help="Convert length units (m, km, mi, ft)")
    length_parser.add_argument("value", type=float, help="Numeric value to convert")
    length_parser.add_argument("from_unit", type=str, help="Source unit")
    length_parser.add_argument("to_unit", type=str, help="Target unit")
    length_parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")

    # --- weight subcommand ---
    weight_parser = subparsers.add_parser("weight", help="Convert weight units (kg, g, lb, oz)")
    weight_parser.add_argument("value", type=float, help="Numeric value to convert")
    weight_parser.add_argument("from_unit", type=str, help="Source unit")
    weight_parser.add_argument("to_unit", type=str, help="Target unit")
    weight_parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")

    args = parser.parse_args(argv)

    try:
        if args.category == "length":
            result = convert_length(args.value, args.from_unit, args.to_unit)
        elif args.category == "weight":
            result = convert_weight(args.value, args.from_unit, args.to_unit)
        else:
            parser.print_help()
            return 1
    except ValueError as exc:
        if args.json:
            print(
                _json_error(args.category, args.value, args.from_unit,
                            args.to_unit, str(exc)),
                file=sys.stderr,
            )
            return 1
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(_json_success(args.category, args.value, args.from_unit,
                            args.to_unit, result))
    else:
        print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
