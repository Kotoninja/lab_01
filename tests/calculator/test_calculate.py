import argparse

from toolkit import calculator, errors

# LINK src/toolkit/calculator.py#calculate


def test_calculate_zero_length_input(capsys):
    calculator.calculate(args=argparse.Namespace(expression=""))
    captured = capsys.readouterr()
    assert captured.out == errors.ZeroLength.text.format("Expression") + "\n"


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
