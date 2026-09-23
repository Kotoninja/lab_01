import argparse
import sys

from toolkit import errors


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
        if flag_from in ["mm", "cm", "m", "km"] and flag_to in ["mm", "cm", "m", "km"]:
            return
        if flag_from in ["g", "km"] and flag_to in ["g", "km"]:
            return
        if flag_from in ["c", "f", "k"] and flag_to in ["c", "f", "k"]:
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
