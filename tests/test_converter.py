"""Тесты конвертера величин."""

import pytest

from toolkit.converter import convert
from toolkit.errors import ConverterError


def test_length():
    assert convert(1, "m", "cm") == 100.0
    assert convert(1, "km", "m") == 1000.0


def test_mass():
    assert convert(1, "kg", "g") == 1000.0
    assert convert(500, "g", "kg") == 0.5


def test_temperature():
    assert convert(100, "c", "f") == pytest.approx(212.0)
    assert convert(0, "c", "k") == pytest.approx(273.15)
    assert convert(32, "f", "c") == pytest.approx(0.0)


def test_case_insensitive():
    assert convert(1, "M", "CM") == 100.0
    assert convert(1, "KG", "G") == 1000.0


def test_result_is_float():
    assert isinstance(convert(1, "m", "cm"), float)


def test_absolute_zero_allowed():
    assert convert(-273.15, "c", "k") == pytest.approx(0.0, abs=1e-9)


def test_unknown_unit():
    with pytest.raises(ConverterError):
        convert(1, "xyz", "m")
    with pytest.raises(ConverterError):
        convert(1, "m", "xyz")


def test_incompatible_units():
    with pytest.raises(ConverterError):
        convert(1, "m", "kg")
    with pytest.raises(ConverterError):
        convert(1, "km", "c")


def test_below_absolute_zero():
    with pytest.raises(ConverterError):
        convert(-300, "c", "k")
    with pytest.raises(ConverterError):
        convert(-1, "k", "c")


def test_invalid_numeric_value():
    with pytest.raises(ConverterError):
        convert("abc", "m", "cm")