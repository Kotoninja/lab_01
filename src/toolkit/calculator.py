import argparse
import sys

from toolkit import errors


def validate(args: argparse.Namespace):
    expression: str = args.expression
    if not len(expression.rstrip()):
        raise errors.ZeroLength


def calculate(args: argparse.Namespace):
    try:
        validate(args=args)
    except errors.ZeroLength as e:
        sys.stdout.write(e.text.format("Expression\n"))
        return
