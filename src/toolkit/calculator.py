"""Калькулятор арифметических выражений.

Код разделён на три шага:
1. tokenize  — превращает строку в список токенов.
2. validate  — проверяет, что токены идут в правильном порядке.
3. calculate — считает результат.

eval, exec и ast.literal_eval не используются — разбор написан вручную.
"""

from .errors import CalculatorError

_OPERATORS = ("+", "-", "*", "/")
_NUMBER_CHARS = "0123456789."


def tokenize(expression):
    """Разбить строку на токены (числа и операторы)."""
    if not isinstance(expression, str):
        raise CalculatorError("выражение должно быть строкой")

    tokens = []
    i, n = 0, len(expression)
    while i < n:
        ch = expression[i]
        if ch.isspace():
            i += 1
            continue
        if ch in _OPERATORS:
            tokens.append(ch)
            i += 1
            continue
        if ch in _NUMBER_CHARS:
            j = i
            while j < n and expression[j] in _NUMBER_CHARS:
                j += 1
            tokens.append(expression[i:j])
            i = j
            continue
        raise CalculatorError(f"недопустимый символ: {ch!r}")
    return tokens


def _parse_number(token):
    """Превратить строку в int или float."""
    try:
        if "." in token:
            return float(token)
        return int(token)
    except ValueError as exc:
        raise CalculatorError(f"неверное число: {token}") from exc


def validate(tokens):
    """Проверить структуру токенов."""
    if not tokens:
        raise CalculatorError("пустое выражение")

    expect_number = True
    for tok in tokens:
        if tok in _OPERATORS:
            if expect_number:
                if tok in ("+", "-"):
                    continue
                raise CalculatorError(
                    f"неожиданный оператор {tok}: пропущен операнд"
                )
            expect_number = True
        else:
            if not expect_number:
                raise CalculatorError(f"пропущен оператор перед {tok}")
            _parse_number(tok)
            expect_number = False

    if expect_number:
        raise CalculatorError("выражение заканчивается оператором")


class _Evaluator:
    """Считает значение по токенам (рекурсивный спуск)."""

    def __init__(self, tokens):
        self._tokens = tokens
        self._pos = 0

    def _peek(self):
        """Посмотреть текущий токен, не сдвигая позицию."""
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return None

    def _take(self):
        """Забрать текущий токен и сдвинуть позицию."""
        tok = self._tokens[self._pos]
        self._pos += 1
        return tok

    def expression(self):
        """Уровень + и -."""
        value = self.term()
        while self._peek() in ("+", "-"):
            op = self._take()
            rhs = self.term()
            if op == "+":
                value = value + rhs
            else:
                value = value - rhs
        return value

    def term(self):
        """Уровень * и /."""
        value = self.factor()
        while self._peek() in ("*", "/"):
            op = self._take()
            rhs = self.factor()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise CalculatorError("деление на ноль")
                value = value / rhs
        return value

    def factor(self):
        """Унарные + и -."""
        sign = 1
        while self._peek() in ("+", "-"):
            if self._take() == "-":
                sign = -sign
        return sign * self._primary()

    def _primary(self):
        """Число."""
        tok = self._peek()
        if tok is None:
            raise CalculatorError("пропущен операнд")
        self._take()
        return _parse_number(tok)


def calculate(expression):
    """Посчитать выражение."""
    tokens = tokenize(expression)
    validate(tokens)
    return _Evaluator(tokens).expression()