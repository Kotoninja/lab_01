class AppError(Exception): ...


class EmptyExpressionError(AppError):  # пустое выражение
    def __init__(self):
        super().__init__("Expression is empty.")


class InvalidCharacterError(AppError):  # недопустимый символ
    def __init__(self, value: str):
        super().__init__(f"Invalid character: {value!r}.")


class MissingOperandError(AppError):  # пропущенный операнд
    def __init__(self):
        super().__init__("Missing operand.")


class ConsecutiveOperatorsError(AppError):  # два бинарных оператора подряд
    def __init__(self):
        super().__init__("Two binary operators in a row.")


class InvalidNumberError(AppError):  # неверное числовое значение
    def __init__(self, token: str):
        super().__init__(f"Invalid number: {token!r}.")


class UnknownUnitError(AppError):  # неизвестную единицу
    def __init__(self, unit: str):
        super().__init__(f"Unknown unit: {unit!r}.")


class IncompatibleUnitsError(AppError):  # несовместимые единицы
    def __init__(self, src: str, dst: str):
        super().__init__(f"Incompatible units: {src!r} -> {dst!r}.")


class DivisionByZero(AppError):  # деление на ноль
    def __init__(self):
        super().__init__("Division by zero.")


class TemperaturesBelowAbsoluteZero(AppError):  # температура ниже абсолютного нуля
    def __init__(self):
        super().__init__("Temperatures below absolute zero.")
