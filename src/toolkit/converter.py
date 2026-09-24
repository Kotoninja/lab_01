import argparse
import sys

from toolkit import errors
from toolkit.constans import LENGTH_ENUM, TEMPERATURE_ENUM, WEIGHT_ENUM


# ANCHOR[id=validate]
def validate(args: argparse.Namespace):
    value: str = args.value
    if not len(value.rstrip()):
        raise errors.ZeroLength

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

    try:
        different_cotegory()
    except errors.DifferentConverterCategory:
        raise errors.DifferentConverterCategory


def convert(args: argparse.Namespace):
    try:
        validate(args=args)
    except errors.ZeroLength:
        sys.stdout.write("Please specify value\n")
        return
    except (errors.FromNone, errors.ToNone, errors.DifferentConverterCategory) as e:
        sys.stdout.write(f"{e.text}\n")
        return
    else:
        print("somel logic")
