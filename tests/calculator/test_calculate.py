import argparse

from toolkit import calculator, errors

# LINK src/toolkit/calculator.py#calculate


def test_calculate_zero_length_input(capsys):
    calculator.calculate(args=argparse.Namespace(expression=""))
    captured = capsys.readouterr()
    assert captured.out == errors.ZeroLength.text.format("Expression") + "\n"
