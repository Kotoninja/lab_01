import argparse

from toolkit import converter, errors

# LINK src/toolkit/calculator.py#calculate


# def test_calculate_zero_length_input(capsys):
#     converter.convert(
#         args=argparse.Namespace(value="test", flag_from="m", flag_to="mm")
#     )
#     captured = capsys.readouterr()
#     assert captured.out == errors.ZeroLength.text.format("Expression") + "\n"


def test_convert_zero_length_input(capsys):
    converter.convert(args=argparse.Namespace(value=""))
    captured = capsys.readouterr()
    assert captured.out == errors.ZeroLength.text.format("Value") + "\n"


def test_convert_zero_flag_from(capsys):
    converter.convert(args=argparse.Namespace(value="10", flag_from=""))
    captured = capsys.readouterr()
    assert captured.out == errors.FromNone.text + "\n"


# def test_convert_zero_flag_to(capsys):
#     converter.convert(args=argparse.Namespace(value="10", flag_from="m", flag_to=""))
#     captured = capsys.readouterr()
#     assert captured.out == errors.DifferentConverterCategory.text + "\n"
