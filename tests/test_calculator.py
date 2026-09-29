import pytest

from toolkit.calculator import calculate, tokenize, validate
from toolkit.errors import CalculatorError

# Поддержать целые и вещественные числа.
def test_tokenize_int():
    assert tokenize("1 + 2 * 3") == ["1", "+", "2", "*", "3"]
    assert tokenize("1.23") == ["1.23"]
    assert calculate("1 + 2") == 3
    assert calculate("1.5 * 2") == 3.0


# Поддержать +, -, *, /.
# Соблюдать приоритет * и / над + и -.
def test_calc():
    assert calculate("1 + 2 * 3") == 7
    assert calculate("1 * 2 - 3") == -1
    assert calculate("1 + 2 * 2 / 4") == 2


# Поддержать унарный + и - перед числом.
def test_unary():
    assert calculate("-1") == -1
    assert calculate("+2") == 2
    assert calculate("1 + -2") == -1


# Игнорировать пробелы между токенами.
def test_space():
    assert calculate("  1   +   2 * 3  ") == 7


# Пустое выражение.
def test_empty():
    with pytest.raises(CalculatorError):
        calculate("")


# Недопустимый символ.
def test_letter():
    with pytest.raises(CalculatorError):
        calculate("1 + a")


# Пропущенный операнд.
def test_operand():
    with pytest.raises(CalculatorError):
        calculate("1 +")


# Два бинарных оператора подряд.
def test_two_operators():
    with pytest.raises(CalculatorError):
        calculate("1 * * 2")


# Деление на ноль.
def test_zero():
    with pytest.raises(CalculatorError):
        calculate("1 / 0")