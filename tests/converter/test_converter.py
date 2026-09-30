import argparse
from decimal import Decimal

import pytest

from toolkit import converter, errors


# LINK src/toolkit/converter.py#convert
def test_convert_zero_length_input():
    converter.convert(args=argparse.Namespace(value=1, flag_from="m", flag_to="mm"))


def test_convert_different_category(capsys):
    with pytest.RaisesExc(errors.IncompatibleUnitsError):
        converter.convert(args=argparse.Namespace(value=1, flag_from="m", flag_to="f"))


# LINK src/toolkit/converter.py#convert_units
def test_convert_units():
    assert (
        converter.convert_units(value=Decimal("1.0"), flag_from="km", flag_to="m")
        == 1000
    )
    assert (
        converter.convert_units(value=Decimal("1.0"), flag_from="c", flag_to="k") == 274
    )
    assert (
        converter.convert_units(value=Decimal("1.0"), flag_from="kg", flag_to="g")
        == 1000
    )
    assert (
        converter.convert_units(value=Decimal("1.0"), flag_from="test", flag_to="g")
        == 0
    )


# LINK src/toolkit/converter.py#get_units_of_measurement
def test_get_units_of_measurement():
    assert converter.get_units_of_measurement("mm") == "0.001"
    assert converter.get_units_of_measurement("cm") == "0.01"
    assert converter.get_units_of_measurement("m") == "1"
    assert converter.get_units_of_measurement("km") == "1000"
    with pytest.RaisesExc(errors.UnknownUnitError):
        converter.get_units_of_measurement("test")


# LINK src/toolkit/converter.py#convert_length
def test_convert_length():
    assert (
        converter.convert_units(value=Decimal("1.0"), flag_from="m", flag_to="m") == 1
    )


# LINK src/toolkit/converter.py#convert_temperature
def test_convert_temperature():
    assert converter.convert_units(
        value=Decimal("1.0"), flag_from="c", flag_to="c"
    ) == Decimal("1.0")
    assert converter.convert_units(
        value=Decimal("1.0"), flag_from="k", flag_to="c"
    ) == Decimal("-272.00")
    assert converter.convert_units(
        value=Decimal("1.0"), flag_from="c", flag_to="f"
    ) == Decimal("33.8")
    assert converter.convert_units(
        value=Decimal("1.0"), flag_from="c", flag_to="k"
    ) == Decimal("274.00")
    assert converter.convert_units(
        value=Decimal("1.0"), flag_from="k", flag_to="c"
    ) == Decimal("-272.00")
    assert converter.convert_units(
        value=Decimal("32.0"), flag_from="f", flag_to="c"
    ) == Decimal()


# LINK src/toolkit/converter.py#convert_weight
def test_convert_weight():
    assert (
        converter.convert_units(value=Decimal("1.0"), flag_from="g", flag_to="g") == 1
    )
    assert converter.convert_units(
        value=Decimal("1.0"), flag_from="g", flag_to="kg"
    ) == Decimal("0.001")
