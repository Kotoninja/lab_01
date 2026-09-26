import unittest

import pytest

from toolkit import main


class TestCalc(unittest.TestCase):
    def setUp(self):
        self.parser = main.create_parser()

    def test_parser_with_no_input(self):
        with pytest.raises(SystemExit) as e:
            self.parser.parse_args([])
        assert e.value.code == 2

    def test_calc(self):
        parsed = self.parser.parse_args(["calc", "expression"])
        assert parsed.expression == "expression"


class TestConvert(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = main.create_parser()

    def test_convert(self):
        parsed = self.parser.parse_args(
            ["convert", "value", "--from", "mm", "--to", "km"]
        )
        assert parsed.value == "value"
        assert parsed.flag_from == "mm"
        assert parsed.flag_to == "km"
