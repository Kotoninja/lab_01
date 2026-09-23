import argparse
import sys

from toolkit import errors


def validate(args: argparse.Namespace):
    expression: str = args.expression
    if len(expression.rstrip()) == 0:
        raise errors.ZeroLength


def calculate(args: argparse.Namespace):
    try:
        validate(args=args)
    except errors.ZeroLength as e:
        sys.stdout.write(e.text.format("Expression"))
        return
