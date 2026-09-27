"""Точка входа CLI: ``python -m toolkit``."""

import argparse
import sys

from .calculator import calculate
from .converter import convert
from .errors import ToolkitError


def build_parser():
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description=(
            "Console utilities: arithmetic calculator and unit converter."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    calc = sub.add_parser(
        "calc", help="Evaluate an arithmetic expression."
    )
    calc.add_argument(
        "expression",
        help="Expression, e.g. '1 + 2 * 3'.",
    )

    conv = sub.add_parser(
        "convert", help="Convert a value between units."
    )
    conv.add_argument("value", help="Numeric value to convert.")
    conv.add_argument(
        "--from",
        dest="from_unit",
        required=True,
        help="Source unit (mm, cm, m, km, g, kg, c, f, k).",
    )
    conv.add_argument(
        "--to",
        dest="to_unit",
        required=True,
        help="Target unit (mm, cm, m, km, g, kg, c, f, k).",
    )

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "calc":
            print(calculate(args.expression))
        elif args.command == "convert":
            print(convert(args.value, args.from_unit, args.to_unit))
    except ToolkitError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())