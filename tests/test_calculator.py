"""Тесты вычислительного ядра (без subprocess)."""

import pytest

from toolkit.calculator import calculate, tokenize, validate
from toolkit.errors import CalculatorError


def test_tokenize_basic():
    assert tokenize("1 + 2 * 3") == ["1", "+", "2", "*", "3"]


def test_tokenize_float():
    assert tokenize("3.14") == ["3.14"]


def test_precedence():
    assert calculate("2 + 3 * 4") == 14
    assert calculate("2 * 3 + 4") == 10
    assert calculate("2 + 3 * 4 - 5") == 9


def test_spaces_ignored():
    assert calculate("  1   +   2 * 3  ") == 7


def test_unary_signs():
    assert calculate("-5") == -5
    assert calculate("+7") == 7
    assert calculate("1 + -2") == -1


def test_float_and_negative_result():
    assert calculate("1.5 * 2") == 3.0
    assert calculate("2 - 5") == -3


def test_empty_expression():
    with pytest.raises(CalculatorError):
        calculate("")


def test_invalid_character():
    with pytest.raises(CalculatorError):
        calculate("1 + a")


def test_missing_operand():
    with pytest.raises(CalculatorError):
        calculate("1 +")


def test_two_binary_operators():
    with pytest.raises(CalculatorError):
        calculate("1 * * 2")


def test_missing_operator():
    with pytest.raises(CalculatorError):
        calculate("1 2")


def test_division_by_zero():
    with pytest.raises(CalculatorError):
        calculate("1 / 0")


def test_invalid_number():
    with pytest.raises(CalculatorError):
        calculate("1.2.3")


def test_validate_rejects_empty():
    with pytest.raises(CalculatorError):
        validate([])