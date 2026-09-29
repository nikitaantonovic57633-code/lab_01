import argparse
import sys

from .calculator import calculate
from .converter import convert
from .errors import ToolkitError


def build_parser():
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Калькулятор выражений и конвертер величин.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    calc = sub.add_parser(
        "calc", help="Посчитать арифметическое выражение."
    )
    calc.add_argument(
        "expression",
        help="Выражение, например '1 + 2 * 3'.",
    )

    conv = sub.add_parser(
        "convert", help="Перевести значение из одной единицы в другую."
    )
    conv.add_argument("value", help="Числовое значение.")
    conv.add_argument(
        "--from",
        dest="from_unit",
        required=True,
        help="Исходная единица: mm, cm, m, km, g, kg, c, f, k.",
    )
    conv.add_argument(
        "--to",
        dest="to_unit",
        required=True,
        help="Целевая единица: mm, cm, m, km, g, kg, c, f, k.",
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
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())