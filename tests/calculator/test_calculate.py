import argparse

import pytest

from toolkit import calculator, errors

# LINK src/toolkit/calculator.py#calculate


def test_calculate_zero_length_input(capsys):
    calculator.calculate(args=argparse.Namespace(expression=""))
    captured = capsys.readouterr()
    assert captured.out == errors.ZeroLength.text.format("Expression") + "\n"


# LINK src/toolkit/calculator.py#tokenization
def test_tokenization_unary_operator_before_number():
    assert calculator.tokenization("-2 + 1") == ["-2", "+", "1"]
    assert calculator.tokenization("1 + -2") == ["1", "+", "-2"]
    assert calculator.tokenization("1 -2") == ["1", "-2"]
    assert calculator.tokenization("1 - 2") == ["1", "-", "2"]
    assert calculator.tokenization("(-2)") == ["(", "-2", ")"]
    assert calculator.tokenization("-2") == ["-2"]
    assert calculator.tokenization("1--2") == ["1", "-", "-2"]
    assert calculator.tokenization("-1-2") == ["-1", "-", "2"]
    assert calculator.tokenization("-1--2") == ["-1", "-", "-2"]
    assert calculator.tokenization("-1-----2") == ["-1", "-", "-", "-", "-", "-2"]
    assert calculator.tokenization("1 +2") == ["1", "+2"]
    assert calculator.tokenization("++1 ++2") == ["+", "+1", "+", "+2"]
    assert calculator.tokenization("1++2") == ["1", "+", "+2"]


def test_tokenization_default_cases():
    assert calculator.tokenization("10/4") == ["10", "/", "4"]
    assert calculator.tokenization("10/(4)") == ["10", "/", "(", "4", ")"]
    assert calculator.tokenization("10/-4") == ["10", "/", "-4"]
    assert calculator.tokenization("(10)/(4)") == ["(", "10", ")", "/", "(", "4", ")"]
    assert calculator.tokenization("-10/-4") == ["-10", "/", "-4"]
    assert calculator.tokenization("100000") == ["100000"]
    assert calculator.tokenization("10/4 + 2") == ["10", "/", "4", "+", "2"]
    assert calculator.tokenization("(2+3)*4") == ["(", "2", "+", "3", ")", "*", "4"]
    assert calculator.tokenization("(2+3) * -4)") == [
        "(",
        "2",
        "+",
        "3",
        ")",
        "*",
        "-4",
        ")",
    ]


# LINK src/toolkit/calculator.py#convert_infix_to_postfix
def test_convert_infix_to_postfix():
    assert calculator.convert_infix_to_postfix(calculator.tokenization("")) == []

    assert calculator.convert_infix_to_postfix(calculator.tokenization("2+2")) == [
        "2",
        "2",
        "+",
    ]
    assert calculator.convert_infix_to_postfix(calculator.tokenization("2*2")) == [
        "2",
        "2",
        "*",
    ]
    assert calculator.convert_infix_to_postfix(calculator.tokenization("2a2")) == [
        "2",
        "2",
        "a",
    ]
    assert calculator.convert_infix_to_postfix(calculator.tokenization("2+-")) == [
        "2",
        "+",
        "-",
    ]
    assert calculator.convert_infix_to_postfix(calculator.tokenization("5")) == ["5"]
    assert calculator.convert_infix_to_postfix(calculator.tokenization("1+2*3")) == [
        "1",
        "2",
        "3",
        "*",
        "+",
    ]
    assert calculator.convert_infix_to_postfix(calculator.tokenization("(1+2*3)")) == [
        "1",
        "2",
        "3",
        "*",
        "+",
    ]
    assert calculator.convert_infix_to_postfix(calculator.tokenization("10/4 + 2")) == [
        "10",
        "4",
        "/",
        "2",
        "+",
    ]

    assert calculator.convert_infix_to_postfix(
        calculator.tokenization("10/40 + 20")
    ) == ["10", "40", "/", "20", "+"]

    assert calculator.convert_infix_to_postfix(calculator.tokenization("(1+2)")) == [
        "1",
        "2",
        "+",
    ]

    assert calculator.convert_infix_to_postfix(calculator.tokenization("1+2)")) == [
        "1",
        "2",
        "+",
    ]

    assert calculator.convert_infix_to_postfix(calculator.tokenization("-2+2")) == [
        "-2",
        "2",
        "+",
    ]

    assert calculator.convert_infix_to_postfix(calculator.tokenization("-2.3+2")) == [
        "-2.3",
        "2",
        "+",
    ]


# LINK src/toolkit/calculator.py#isnumber
def test_isnumber():
    assert calculator.isnumber("2")
    assert calculator.isnumber("-2")
    assert calculator.isnumber("2.0")
    assert calculator.isnumber("02")


def test_use_operation():
    with pytest.RaisesExc(errors.UnknownOperation):
        calculator.use_operation(1, 1, "^")


def convert_to_postfix(expression: str) -> list[str]:
    return calculator.convert_infix_to_postfix(
        calculator.tokenization(expression=expression)
    )


# LINK src/toolkit/calculator.py#execute_expression
def test_execute_expression():
    assert calculator.execute_expression(convert_to_postfix("2")) == 2.0
    assert calculator.execute_expression(convert_to_postfix("22")) == 22.0
    assert calculator.execute_expression(convert_to_postfix("2+2")) == 4.0
    assert calculator.execute_expression(convert_to_postfix("10-2")) == 8.0
    assert calculator.execute_expression(convert_to_postfix("2.6+2")) == 4.6
    assert calculator.execute_expression(convert_to_postfix("6*7")) == 42
    assert calculator.execute_expression(convert_to_postfix("6*7")) == 42.0
    assert calculator.execute_expression(convert_to_postfix("10/2")) == 5.0
    with pytest.RaisesExc(errors.DivisionByZero):
        assert calculator.execute_expression(convert_to_postfix("10/0")) == 5.0

    assert calculator.execute_expression(convert_to_postfix("(1+2)*3")) == 9.0
    assert calculator.execute_expression(convert_to_postfix("1+2*3")) == 7.0

    with pytest.RaisesExc(errors.ValidationExpression):
        assert calculator.execute_expression(convert_to_postfix("a +a ")) == 7.0
