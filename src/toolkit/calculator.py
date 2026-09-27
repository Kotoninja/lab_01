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
        print(convert_infix_to_postfix(tokenization(args.expression)))


def tokenization(expression: str) -> list[str]:
    """tokenize input, e.g. expression="11+1" return: ["11", "+", "1"]

    Args:
        expression (str): user input

    Returns:
        list[str]: tokenized input
    """
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


def higher_or_equal(op1, op2):
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    return precedence[op1] >= precedence[op2]


def convert_infix_to_postfix(infix_list: list[str]) -> list[str]:
    postfix_list: list[str] = []

    stack: list[str] = []

    for symbol in infix_list:
        if symbol.isdigit():
            postfix_list.append(symbol)
        elif symbol == ")":
            while len(stack):
                stack_element: str = stack.pop()
                if stack_element != "(":
                    postfix_list.append(stack_element)
                else:
                    break
        elif symbol != "(":
            while len(stack):
                if higher_or_equal(symbol, stack[-1]):
                    postfix_list.append(stack.pop())
            stack.append(symbol)
    while len(stack):
        postfix_list.append(stack.pop())

    return postfix_list
