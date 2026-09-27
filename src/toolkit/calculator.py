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
        tokens: list[str] = tokenization(args.expression)
        postfix_convertation: list[str] = convert_infix_to_postfix(tokens)

        try:
            result: float = execute_expression(postfix_list=postfix_convertation)
            sys.stdout.write(f"{result}\n")
            return
        except (errors.ValidationExpression, errors.UnknownOperation) as e:
            sys.stdout.write(e.text + "\n")
            return


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


def use_operation(op1: float, op2: float, operation: str) -> float:
    match operation:
        case "+":
            return op1 + op2
        case "-":
            return op1 - op2
        case "*":
            return op1 * op2
        case "/":
            return op1 / op2
        case _:
            raise errors.UnknownOperation


def execute_expression(postfix_list: list[str]) -> float:
    stack: list[str] = []

    for i in range(len(postfix_list)):
        symbol: str = postfix_list[i]

        is_operation: bool = symbol in "+-*/"

        if not is_operation:
            value: str = postfix_list[i]
            if value.isdigit():
                stack.append(value)
            else:
                raise errors.ValidationExpression
            continue

        if is_operation and len(stack) < 2:
            raise errors.ValidationExpression

        try:
            first: float = float(stack.pop())
            second: float = float(stack.pop())
        except ValueError:
            raise errors.ValidationExpression

        try:
            stack.append(str(use_operation(second, first, symbol)))
        except errors.ValidationExpression:
            raise errors.ValidationExpression

    if len(stack) != 1:
        raise errors.ValidationExpression
    return float(stack.pop())
