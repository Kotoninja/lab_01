import argparse
import sys
from decimal import Decimal, InvalidOperation, getcontext

from toolkit import errors, repository


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
    getcontext().prec = 6
    tokens: list[str] = tokenization(args.expression)
    postfix_convertation: list[str] = convert_infix_to_postfix(tokens)
    result: Decimal = execute_expression(postfix_list=postfix_convertation)
    sys.stdout.write(str(result))
    data = {"expression": args.expression, "answer": float(result)}
    repository.add(data=data)


# ANCHOR[id=validate_tokenization]
def validate_tokenization(infix_list: list[str]):
    """Validate tokenized expression

    Args:
        infix_list (list[str]): Tokenized expression

    Raises:
        errors.InvalidCharacterError: недопустимый символ
        errors.MissingOperandError: пропущенный операнд
        errors.ConsecutiveOperatorsError: два бинарных оператора подряд
    """
    if len(infix_list) == 1 and not isnumber(infix_list[0]):
        raise errors.InvalidCharacterError(infix_list[0])

    operation_list: list[str] = ["//", "/", "+", "-", "*", "%"]
    for i in range(len(infix_list) - 1):
        if isnumber(infix_list[i]) and isnumber(infix_list[i + 1]):
            raise errors.MissingOperandError
        elif infix_list[i] in operation_list and infix_list[i + 1] in operation_list:
            raise errors.ConsecutiveOperatorsError


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
    i: int = 0
    while i < len(expression):
        symbol: str = expression[i].lower()

        if not symbol.isdigit() and symbol not in "/*+-%.()% ":
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

            if expression[i] == "/" and expression[i + 1] == "/":
                result.append("//")
                i += 2
                continue

            if not symbol.isspace():
                result.append(symbol)
        i += 1
    if len(buffer):
        result.append(buffer)

    validate_tokenization(result)
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
    """Value is number?

    Args:
        value (str): "2" or "-2" or "2.0"

    Returns:
        bool: answer
    """
    if value.isdigit():
        return True

    try:
        Decimal(value)
        return True
    except InvalidOperation:
        return False


# ANCHOR[id=use_operation]
def use_operation(op1: Decimal, op2: Decimal, operation: str) -> Decimal:
    """Apply a binary arithmetic operator to two operands.

    Args:
        op1 (Decimal): operand
        op2 (Decimal): operand
        operation (str): [+, -, /, *]

    Raises:
        errors.DivisionByZero: деление на ноль
        errors.InvalidCharacterError: недопустимый символ

    Returns:
        Decimal: answer
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
        case "//":
            if op2 == 0:
                raise errors.DivisionByZero
            return op1 // op2
        case "%":
            if op2 == 0:
                raise errors.DivisionByZero
            return op1 % op2
        case _:
            raise errors.InvalidCharacterError(operation)


# ANCHOR[id=execute_expression]
def execute_expression(postfix_list: list[str]) -> Decimal:
    """Evaluate a tokenized postfix (Reverse Polish) expression

    Args:
        postfix_list (list[str]): Tokenized postfix expression, e.g. ["1", "2", "+"]

    Raises:
        errors.InvalidNumberError: неверное числовое значение
        errors.MissingOperandError: пропущенный операнд

    Returns:
        Decimal: answer
    """
    stack: list[str] = []

    for i in range(len(postfix_list)):
        symbol: str = postfix_list[i]

        is_operation: bool = symbol in ["+", "-", "*", "/", "%", "//"]

        if not is_operation:
            if isnumber(symbol):
                stack.append(symbol)
            else:
                raise errors.InvalidNumberError(symbol)
            continue

        if is_operation and len(stack) < 2:
            raise errors.MissingOperandError

        first: Decimal = Decimal(stack.pop())
        second: Decimal = Decimal(stack.pop())

        stack.append(str(use_operation(second, first, symbol)))

    if len(stack) != 1:
        raise errors.MissingOperandError
    return Decimal(stack.pop())
