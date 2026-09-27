class ZeroLength(BaseException):
    text = "{} has zero length"


class FromNone(BaseException):
    text = "Specify --from value"


class ToNone(BaseException):
    text = "Specify --to value"


class DifferentConverterCategory(BaseException):
    text = "Different converter category"


# class ConvertToPostfix(BaseException):
#     text = "The expression could not be converted to postfix form. Please ensure it is written correctly and does not contain any syntax errors."


class ValidationExpression(BaseException):
    text = "The number of opening and closing parentheses does not match."


class UnknownOperation(BaseException):
    text = "Unknown operation"
