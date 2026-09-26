import argparse

import pytest

from toolkit import constans, converter, errors

# LINK src/toolkit/converter.py#validate


def test_validate_zero_length_value():
    with pytest.raises(errors.ZeroLength):
        converter.validate(argparse.Namespace(value=""))


def test_validate_zero_length_flag_from():
    with pytest.raises(errors.FromNone):
        converter.validate(argparse.Namespace(value="test", flag_from=""))


def test_validate_zero_length_flag_to():
    with pytest.raises(errors.ToNone):
        converter.validate(
            argparse.Namespace(value="test", flag_from="test", flag_to="")
        )


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
                        value="test", flag_from=from_status, flag_to=to_status
                    )
                )


def test_validate_different_category():
    with pytest.raises(errors.DifferentConverterCategory):
        converter.validate(
            argparse.Namespace(
                value="test",
                flag_from=constans.LENGTH_ENUM[0],
                flag_to=constans.TEMPERATURE_ENUM[0],
            )
        )
    with pytest.raises(errors.DifferentConverterCategory):
        converter.validate(
            argparse.Namespace(
                value="test",
                flag_from=constans.LENGTH_ENUM[0],
                flag_to=constans.WEIGHT_ENUM[0],
            )
        )
    with pytest.raises(errors.DifferentConverterCategory):
        converter.validate(
            argparse.Namespace(
                value="test",
                flag_from=constans.TEMPERATURE_ENUM[0],
                flag_to=constans.WEIGHT_ENUM[0],
            )
        )
