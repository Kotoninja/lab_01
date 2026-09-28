import argparse
import sys

from toolkit import errors
from toolkit.constans import LENGTH_ENUM, TEMPERATURE_ENUM, WEIGHT_ENUM


# ANCHOR[id=validate]
def validate(args: argparse.Namespace):
    flag_from: str = str(args.flag_from).lower()
    if not len(flag_from.rstrip()):
        raise errors.FromNone

    flag_to: str = str(args.flag_to).lower()
    if not len(flag_to.rstrip()):
        raise errors.ToNone

    def different_cotegory():
        if flag_from in LENGTH_ENUM and flag_to in LENGTH_ENUM:
            return
        if flag_from in TEMPERATURE_ENUM and flag_to in TEMPERATURE_ENUM:
            return
        if flag_from in WEIGHT_ENUM and flag_to in WEIGHT_ENUM:
            return
        raise errors.DifferentConverterCategory

    if (
        (flag_from == "c" and args.value <= -273)
        or (flag_from == "k" and args.value <= 0)
        or (flag_from == "f" and args.value <= -460)
    ):
        raise errors.TemperaturesBelowAbsoluteZero

    try:
        different_cotegory()
    except errors.DifferentConverterCategory:
        raise errors.DifferentConverterCategory


# ANCHOR[id=convert]
def convert(args: argparse.Namespace):
    try:
        validate(args=args)
    except (
        errors.FromNone,
        errors.ToNone,
        errors.DifferentConverterCategory,
        errors.TemperaturesBelowAbsoluteZero,
    ) as e:
        sys.stderr.write(f"{e.text}\n")
    else:
        value: float = args.value  # TODO Add Decimal
        flag_from: str = str(args.flag_from).lower()
        flag_to: str = str(args.flag_to).lower()

        result: float = convert_units(value=value, flag_from=flag_from, flag_to=flag_to)

        sys.stdout.write(str(result) + "\n")


def convert_units(value: float, flag_from: str, flag_to: str) -> float:
    answer: float = 0
    if flag_from in LENGTH_ENUM:
        answer = convert_length(value=value, flag_from=flag_from, flag_to=flag_to)
    elif flag_from in WEIGHT_ENUM:
        answer = convert_weight(value=value, flag_from=flag_from, flag_to=flag_to)
    elif flag_from in TEMPERATURE_ENUM:
        answer = convert_temperature(value=value, flag_from=flag_from, flag_to=flag_to)
    return answer


def get_units_of_measurement(value: str) -> float:
    match value:
        case "mm":
            return 0.001
        case "cm":
            return 0.01
        case "m":
            return 1
        case "km":
            return 1000
    return 0


def convert_length(value: float, flag_from: str, flag_to: str) -> float:
    if flag_from == flag_to:
        return value

    meters: float = value * get_units_of_measurement(flag_from)
    return meters / get_units_of_measurement(flag_to)


def convert_temperature(value: float, flag_from: str, flag_to: str) -> float:
    if flag_from == flag_to:
        return value

    match flag_from:
        case "f":
            celsius = (value - 32) / 1.8
        case "k":
            celsius = value - 273
        case _:
            celsius = value

    match flag_to:
        case "f":
            return (celsius * 1.8) + 32
        case "k":
            return celsius + 273
        case _:
            return celsius


def convert_weight(value: float, flag_from: str, flag_to: str) -> float:
    if flag_from == flag_to:
        return value

    if flag_from == "g":
        return value / 1000
    else:
        return value * 1000
