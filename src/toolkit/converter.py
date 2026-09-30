import argparse
import sys
from decimal import Decimal

from toolkit import config, constans, errors, repository


# ANCHOR[id=validate]
def validate(args: argparse.Namespace):
    """Validate user input

    Args:
        args (argparse.Namespace): Parsed data

    Raises:
        errors.UnknownUnitError: неизвестная единица
        errors.IncompatibleUnitsError: несовместимые единицы
        errors.TemperaturesBelowAbsoluteZero: температура ниже абсолютного нуля
    """
    flag_from: str = str(args.flag_from).lower()
    flag_to: str = str(args.flag_to).lower()

    if (
        flag_from not in constans.LENGTH_ENUM
        and flag_from not in constans.TEMPERATURE_ENUM
        and flag_from not in constans.WEIGHT_ENUM
    ):
        raise errors.UnknownUnitError(flag_from)
    elif (
        flag_to not in constans.LENGTH_ENUM
        and flag_to not in constans.TEMPERATURE_ENUM
        and flag_to not in constans.WEIGHT_ENUM
    ):
        raise errors.UnknownUnitError(flag_to)

    if (
        (flag_from in constans.LENGTH_ENUM and flag_to not in constans.LENGTH_ENUM)
        or (flag_from in constans.WEIGHT_ENUM and flag_to not in constans.WEIGHT_ENUM)
        or (
            flag_from in constans.TEMPERATURE_ENUM
            and flag_to not in constans.TEMPERATURE_ENUM
        )
    ):
        raise errors.IncompatibleUnitsError(flag_from, flag_to)

    if (
        (flag_from == "c" and args.value <= -273)
        or (flag_from == "k" and args.value <= 0)
        or (flag_from == "f" and args.value <= -460)
    ):
        raise errors.TemperaturesBelowAbsoluteZeroError


# ANCHOR[id=convert]
def convert(args: argparse.Namespace):
    """Entry point to the converter, where build all logic

    Args:
        args (argparse.Namespace): Parsed data
    """
    validate(args=args)

    value: Decimal = Decimal(args.value)
    flag_from: str = str(args.flag_from).lower()
    flag_to: str = str(args.flag_to).lower()

    result: Decimal = convert_units(value=value, flag_from=flag_from, flag_to=flag_to)

    sys.stdout.write(str(result))

    if hasattr(args, "command"):
        data = constans.JSON_RESPONSE(
            command=args.command,
            exression=f"{value} --from {flag_from} --to {flag_to}",
            answer=float(result),
        )
        repository.add(data=data)


# ANCHOR[id=convert_units]
def convert_units(value: Decimal, flag_from: str, flag_to: str) -> Decimal:
    """Convert units of measurement from one category to another.

    Args:
        value (Decimal): What number are we converting?
        flag_from (str): From which category are we converting?
        flag_to (str): What category are we converting to?

    Returns:
        Decimal: answer
    """
    answer: Decimal = Decimal("0.00")
    if flag_from in constans.LENGTH_ENUM:
        answer = convert_length(value=value, flag_from=flag_from, flag_to=flag_to)
    elif flag_from in constans.WEIGHT_ENUM:
        answer = convert_weight(value=value, flag_from=flag_from, flag_to=flag_to)
    elif flag_from in constans.TEMPERATURE_ENUM:
        answer = convert_temperature(value=value, flag_from=flag_from, flag_to=flag_to)
    return answer


# ANCHOR[id=get_units_of_measurement]
def get_units_of_measurement(value: str) -> str:
    """Convert length to standard (meters)

    Args:
        value (str): value

    Returns:
        Decimal: number
    """
    match value:
        case "mm":
            return config.SETTINGS["length"]["mm"]
        case "cm":
            return config.SETTINGS["length"]["cm"]
        case "m":
            return config.SETTINGS["length"]["m"]
        case "km":
            return config.SETTINGS["length"]["km"]
    raise errors.UnknownUnitError(value)


# ANCHOR[id=convert_length]
def convert_length(value: Decimal, flag_from: str, flag_to: str) -> Decimal:
    """Convert length

    Args:
        value (Decimal): [mm, cm, m, km]
        flag_from (str): From which category are we converting?
        flag_to (str): What category are we converting to?

    Returns:
        Decimal: answer
    """
    if flag_from == flag_to:
        return value

    meters: Decimal = Decimal(value * Decimal(get_units_of_measurement(flag_from)))
    return meters / Decimal(get_units_of_measurement(flag_to))


# ANCHOR[id=convert_temperature]
def convert_temperature(value: Decimal, flag_from: str, flag_to: str) -> Decimal:
    """Convert temperature

    Args:
        value (Decimal): [f, c, k]
        flag_from (str): From which category are we converting?
        flag_to (str): What category are we converting to?

    Returns:
        Decimal: answer
    """
    if flag_from == flag_to:
        return value

    match flag_from:
        case "f":
            celsius = (value - 32) / Decimal("1.8")
        case "k":
            celsius = value - 273
        case _:
            celsius = value

    match flag_to:
        case "f":
            return (celsius * Decimal("1.8")) + 32
        case "k":
            return celsius + 273
        case _:
            return celsius


# ANCHOR[id=convert_weight]
def convert_weight(value: Decimal, flag_from: str, flag_to: str) -> Decimal:
    """Convert weight

    Args:
        value (Decimal): [g, kg]
        flag_from (str): From which category are we converting?
        flag_to (str): What category are we converting to?

    Returns:
        Decimal: answer
    """
    if flag_from == flag_to:
        return value

    return (
        value
        * Decimal(config.SETTINGS["weight"][flag_from])
        / Decimal(config.SETTINGS["weight"][flag_to])
    )
