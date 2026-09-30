import argparse
import sys

from toolkit import calculator, converter, errors


def create_parser():
    """Generate main parser

    Returns:
        argparse.ArgumentParser: parser
    """
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="CLI app for calculation and converter",
    )
    subparsers = parser.add_subparsers(required=True)

    # calculator
    calc_parser = subparsers.add_parser(
        "calc", help="Calculate a mathematical expression"
    )
    calc_parser.add_argument("expression", default="", type=str, nargs="?", help="Expression")
    calc_parser.set_defaults(func=calculator.calculate, command="calc")

    # converter
    convert_parser = subparsers.add_parser(
        "convert", help="Convert a value from one unit to another"
    )
    convert_parser.add_argument(
        "value", default="", nargs="?", type=float, help="Value to convert"
    )
    convert_parser.add_argument(
        "--from",
        dest="flag_from",
        required=True,
        help="From which category are we converting",
    )
    convert_parser.add_argument(
        "--to", dest="flag_to", required=True, help="What category are we converting to"
    )
    convert_parser.set_defaults(func=converter.convert, command="converter")

    return parser


def main() -> None:
    """
    Entry point to the application
    """
    parser = create_parser()

    # Parse arguments and select func
    args = parser.parse_args()
    try:
        args.func(args)
        sys.stdout.write("\n")
        sys.exit(0)
    except errors.AppError as e:
        sys.stderr.write(f"\033[31mError: {e}\033[0m\n")
        sys.exit(2)
