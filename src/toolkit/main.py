import argparse

from toolkit import calculator, converter


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
    convert_parser.add_argument("value", default="", nargs="?")
    convert_parser.add_argument("--from", dest="flag_from")
    convert_parser.add_argument("--to", dest="flag_to")
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
    args.func(args)
