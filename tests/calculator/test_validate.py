import argparse

import pytest

from toolkit import calculator, errors


# LINK src/toolkit/calculator.py#validate
def test_validate_zero_length_input():
    with pytest.raises(errors.EmptyExpressionError):
        calculator.validate(argparse.Namespace(expression=""))


# LINK src/toolkit/calculator.py#validate_tokenization
def test_validate_tokenization():
    with pytest.raises(errors.InvalidCharacterError):
        calculator.validate_tokenization(["+"])
    with pytest.raises(errors.MissingOperandError):
        calculator.validate_tokenization(["2", "2", "2", "2", "2"])
    with pytest.raises(errors.MissingOperandError):
        calculator.validate_tokenization(["1", "-2"])
