import argparse
import sys

from toolkit import errors


# ANCHOR[id=validate]
def validate(args: argparse.Namespace):
    """Validate user input

    Args:
        args (argparse.Namespace): Parsed data

    Raises:
        errors.EmptyExpressionError: пустое выражение
    """
    expression: str = args.expression
    if not len(expression.rstrip()):
        raise errors.EmptyExpressionError


# ANCHOR[id=calculate]
def calculate(args: argparse.Namespace):
    """Entry point to the calculator, where build all logic

    Args:
        args (argparse.Namespace): Parsed data
    """
    validate(args=args)
    tokens: list[str] = tokenization(args.expression)
    postfix_convertation: list[str] = convert_infix_to_postfix(tokens)
    result: float = execute_expression(postfix_list=postfix_convertation)
    sys.stdout.write(f"{result}")


# ANCHOR[id=tokenization]
def tokenization(expression: str) -> list[str]:
    """tokenize input, e.g. expression="11+1" return: ["11", "+", "1"]

    Args:
        expression (str): expression, for example "11+1"

    Returns:
        list[str]: tokenized input
    """
    expression = expression.rstrip() + " "
    result: list[str] = []

    buffer: str = ""
    for i in range(len(expression)):
        symbol: str = expression[i].lower()

        # print(symbol not in "/*+-% ")
        if not symbol.isdigit() and symbol not in "/*+-%.() ":
            raise errors.InvalidCharacterError(symbol)

        if (isnumber(symbol) or symbol == ".") or (
            symbol in "+-"
            and (not isnumber(expression[i - 1]) and isnumber(expression[i + 1]))
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


# ANCHOR[id=higher_or_equal]
def higher_or_equal(op1: str, op2: str) -> bool:
    """Compare operator

    Args:
        op1 (str): operator
        op2 (str): operator

    Raises:
        errors.InvalidCharacterError: недопустимый символ

    Returns:
        bool or error
    """
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "(": 0}
    if op1 not in precedence:
        raise errors.InvalidCharacterError(op1)
    if op2 not in precedence:
        raise errors.InvalidCharacterError(op2)
    return precedence[op1] >= precedence[op2]


# ANCHOR[id=convert_infix_to_postfix]
def convert_infix_to_postfix(infix_list: list[str]) -> list[str]:
    """Convert an infix expression to postfix notation.

    Args:
        infix_list (list[str]): tokenized expression

    Returns:
        list[str]: answer
    """
    postfix_list: list[str] = []

    stack: list[str] = []

    for symbol in infix_list:
        if isnumber(symbol):
            postfix_list.append(symbol)
        elif symbol == ")":
            while len(stack):
                stack_element: str = stack.pop()
                if stack_element != "(":
                    postfix_list.append(stack_element)
                else:
                    break
        else:
            while len(stack) and higher_or_equal(stack[-1], symbol):
                postfix_list.append(stack.pop())
            stack.append(symbol)
    while len(stack):
        postfix_list.append(stack.pop())

    return postfix_list


# ANCHOR[id=isnumber]
def isnumber(value: str) -> bool:
    """Value is number or float?

    Args:
        value (str): "2" or "-2" or "2.0"

    Returns:
        bool: answer
    """
    if value.isdigit():
        return True

    try:
        float(value)
        return True
    except ValueError:
        return False

# ANCHOR[id=use_operation]
def use_operation(op1: float, op2: float, operation: str) -> float:
    """Apply a binary arithmetic operator to two operands.

    Args:
        op1 (float): operand
        op2 (float): operand
        operation (str): [+, -, /, *]

    Raises:
        errors.DivisionByZero: деление на ноль
        errors.InvalidCharacterError: недопустимый символ

    Returns:
        float: answer
    """
    match operation:
        case "+":
            return op1 + op2
        case "-":
            return op1 - op2
        case "*":
            return op1 * op2
        case "/":
            if op2 == 0:
                raise errors.DivisionByZero
            return op1 / op2
        case _:
            raise errors.InvalidCharacterError(operation)


# ANCHOR[id=execute_expression]
def execute_expression(postfix_list: list[str]) -> float:
    """Evaluate a tokenized postfix (Reverse Polish) expression

    Args:
        postfix_list (list[str]): Tokenized postfix expression, e.g. ["1", "2", "+"]

    Raises:
        errors.InvalidNumberError: неверное числовое значение
        errors.MissingOperandError: пропущенный операнд

    Returns:
        float: answer
    """
    stack: list[str] = []

    for i in range(len(postfix_list)):
        symbol: str = postfix_list[i]

        is_operation: bool = symbol in "+-*/"

        if not is_operation:
            value: str = postfix_list[i]
            if isnumber(symbol):
                stack.append(value)
            else:
                raise errors.InvalidNumberError(value)
            continue

        if is_operation and len(stack) < 2:
            raise errors.MissingOperandError

        first: float = float(stack.pop())
        second: float = float(stack.pop())

        stack.append(str(use_operation(second, first, symbol)))

    if len(stack) != 1:
        raise errors.MissingOperandError
    return float(stack.pop())
