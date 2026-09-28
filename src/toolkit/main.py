import argparse
import sys
from toolkit import calculator, converter, errors


def create_parser():
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="CLI app for calculation and converter",
    )
    subparsers = parser.add_subparsers(required=True)

    # calculate
    calc_parser = subparsers.add_parser("calc")
    calc_parser.add_argument("expression", default="", nargs="?")
    calc_parser.set_defaults(func=calculator.calculate, command="calc")

    # converter
    convert_parser = subparsers.add_parser("convert")
    convert_parser.add_argument("value", default="", nargs="?", type=float)
    convert_parser.add_argument("--from", dest="flag_from", required=True)
    convert_parser.add_argument("--to", dest="flag_to", required=True)
    convert_parser.set_defaults(func=converter.convert, command="converter")

    return parser


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
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
