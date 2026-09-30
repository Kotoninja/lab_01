import argparse

import pytest

from toolkit import constans, converter, errors

# LINK src/toolkit/converter.py#validate


def test_validate_correct_cotegory():
    for converter_category in [
        constans.LENGTH_ENUM,
        constans.WEIGHT_ENUM,
        constans.TEMPERATURE_ENUM,
    ]:
        for from_status in converter_category:
            for to_status in converter_category:
                converter.validate(
                    argparse.Namespace(
                        value=10, flag_from=from_status, flag_to=to_status
                    )
                )


def test_validate_different_category():
    with pytest.raises(errors.IncompatibleUnitsError):
        converter.validate(
            argparse.Namespace(
                value=10,
                flag_from=constans.LENGTH_ENUM[0],
                flag_to=constans.TEMPERATURE_ENUM[0],
            )
        )
    with pytest.raises(errors.IncompatibleUnitsError):
        converter.validate(
            argparse.Namespace(
                value=10,
                flag_from=constans.LENGTH_ENUM[0],
                flag_to=constans.WEIGHT_ENUM[0],
            )
        )
    with pytest.raises(errors.IncompatibleUnitsError):
        converter.validate(
            argparse.Namespace(
                value=1.0,
                flag_from=constans.TEMPERATURE_ENUM[0],
                flag_to=constans.WEIGHT_ENUM[0],
            )
        )


def test_temperature_below_zero():
    with pytest.raises(errors.TemperaturesBelowAbsoluteZeroError):
        converter.validate(
            args=argparse.Namespace(value=-1, flag_from="k", flag_to="c")
        )
    with pytest.raises(errors.TemperaturesBelowAbsoluteZeroError):
        converter.validate(
            args=argparse.Namespace(value=-274, flag_from="c", flag_to="c")
        )
    with pytest.raises(errors.TemperaturesBelowAbsoluteZeroError):
        converter.validate(
            args=argparse.Namespace(value=-461, flag_from="f", flag_to="c")
        )


def test_unknow_unit():
    with pytest.RaisesExc(errors.UnknownUnitError):
        converter.validate(
            args=argparse.Namespace(value=1, flag_from="test", flag_to="m")
        )
    with pytest.RaisesExc(errors.UnknownUnitError):
        converter.validate(
            args=argparse.Namespace(value=1, flag_from="m", flag_to="test")
        )
