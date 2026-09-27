import argparse
import sys

from toolkit import errors


# ANCHOR[id=validate]
def validate(args: argparse.Namespace):
    expression: str = args.expression
    if not len(expression.rstrip()):
        raise errors.ZeroLength


# ANCHOR[id=calculate]
def calculate(args: argparse.Namespace):
    try:
        validate(args=args)
    except errors.ZeroLength as e:
        sys.stdout.write(e.text.format("Expression") + "\n")
        return
    else:
        print(tokenization(args.expression))


def tokenization(expression: str) -> list[str]:
    expression = " " + expression.rstrip()
    result: list[str] = []

    buffer: str = ""
    for i in range(len(expression)):
        symbol: str = expression[i]
        if (symbol.isdigit() or symbol == ".") or (
            symbol in "+-"
            and (not expression[i - 1].isdigit() and expression[i + 1].isdigit())
        ):
            buffer += symbol
        else:
            if len(buffer):
                result.append(buffer)
                buffer = ""
            if not symbol.isspace():
                result.append(symbol)

    if len(buffer):
        result.append(buffer)
    return result
