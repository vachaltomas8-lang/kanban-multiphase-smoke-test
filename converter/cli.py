"""Unified CLI for length and weight conversions.

Usage:
    python3 -m converter.cli length <value> <from_unit> <to_unit>
    python3 -m converter.cli weight <value> <from_unit> <to_unit>
"""

import argparse
import sys

from converter.length import convert_length
from converter.weight import convert_weight


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

    # --- weight subcommand ---
    weight_parser = subparsers.add_parser("weight", help="Convert weight units (kg, g, lb, oz)")
    weight_parser.add_argument("value", type=float, help="Numeric value to convert")
    weight_parser.add_argument("from_unit", type=str, help="Source unit")
    weight_parser.add_argument("to_unit", type=str, help="Target unit")

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
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
