def color(value: str) -> str:
    return f"\033[31mError: {value}\033[0m"


class ZeroLength(BaseException):
    text = "{} has zero length"


class FromNone(BaseException):
    text = "Specify --from value"


class ToNone(BaseException):
    text = "Specify --to value"


class DifferentConverterCategory(BaseException):
    text = "Different converter category"


class ValidationExpression(BaseException):
    text = color(value="Invalid mathematical expression syntax.")


class UnknownOperation(BaseException):
    text = color(value="Unknown operation.")


class DivisionByZero(BaseException):
    text = color(value="Division by zero.")
