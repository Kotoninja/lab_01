import argparse

import pytest

from toolkit import calculator, errors


# LINK src/toolkit/calculator.py#validate
def test_validate_zero_length_input():
    with pytest.raises(errors.ZeroLength):
        calculator.validate(argparse.Namespace(expression=""))
