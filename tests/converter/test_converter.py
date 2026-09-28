import argparse

from toolkit import converter, errors

# LINK src/toolkit/converter.py#convert


def test_convert_zero_length_input():
    converter.convert(args=argparse.Namespace(value=1, flag_from="m", flag_to="mm"))


def test_convert_different_category(capsys):
    converter.convert(args=argparse.Namespace(value=1, flag_from="m", flag_to="f"))
    captured = capsys.readouterr()
    assert captured.err == errors.DifferentConverterCategory.text + "\n"


def test_convert_units():
    assert converter.convert_units(value=1, flag_from="km", flag_to="m") == 1000
    assert converter.convert_units(value=1, flag_from="c", flag_to="k") == 274
    assert converter.convert_units(value=1, flag_from="kg", flag_to="g") == 1000
    assert converter.convert_units(value=1, flag_from="test", flag_to="g") == 0


def test_get_units_of_measurement():
    assert converter.get_units_of_measurement("mm") == 0.001
    assert converter.get_units_of_measurement("cm") == 0.01
    assert converter.get_units_of_measurement("m") == 1
    assert converter.get_units_of_measurement("km") == 1000
    assert converter.get_units_of_measurement("test") == 0


def test_convert_length():
    assert converter.convert_units(value=1, flag_from="m", flag_to="m") == 1


def test_convert_temperature():
    assert converter.convert_units(value=1, flag_from="c", flag_to="c") == 1
    assert converter.convert_units(value=1, flag_from="f", flag_to="c") == -17.22222222222222
    assert converter.convert_units(value=1, flag_from="k", flag_to="c") == -272
    assert converter.convert_units(value=1, flag_from="c", flag_to="f") == 33.8
    assert converter.convert_units(value=1, flag_from="c", flag_to="k") == 274
    assert converter.convert_units(value=1, flag_from="k", flag_to="c") == -272


def test_convert_weight():
    assert converter.convert_units(value=1, flag_from="g", flag_to="g") == 1
    assert converter.convert_units(value=1, flag_from="g", flag_to="kg") == 0.001
