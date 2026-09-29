from .errors import CalculatorError

_OPERATORS = ("+", "-", "*", "/")
_NUMBER_CHARS = "0123456789."


def tokenize(expression):
    if not isinstance(expression, str):
        raise CalculatorError("Выражение должно быть строкой")

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
        raise CalculatorError(f"Недопустимый символ: {ch!r}")
    return tokens


def _parse_number(token):
    try:
        if "." in token:
            return float(token)
        return int(token)
    except ValueError as exc:
        raise CalculatorError(f"Неверное число: {token}") from exc


def validate(tokens):
    if not tokens:
        raise CalculatorError("Пустое выражение")

    expect_number = True
    for tok in tokens:
        if tok in _OPERATORS:
            if expect_number:
                if tok in ("+", "-"):
                    continue
                raise CalculatorError(
                    f"Неожиданный оператор {tok}: пропущен операнд"
                )
            expect_number = True
        else:
            if not expect_number:
                raise CalculatorError(f"Пропущен оператор перед {tok}")
            _parse_number(tok)
            expect_number = False

    if expect_number:
        raise CalculatorError("Выражение заканчивается оператором")


class _Evaluator:

    def __init__(self, tokens):
        self._tokens = tokens
        self._pos = 0

    def _peek(self):
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return None

    def _take(self):
        tok = self._tokens[self._pos]
        self._pos += 1
        return tok

    def expression(self):
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
        value = self.factor()
        while self._peek() in ("*", "/"):
            op = self._take()
            rhs = self.factor()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise CalculatorError("Деление на ноль")
                value = value / rhs
        return value

    def factor(self):
        sign = 1
        while self._peek() in ("+", "-"):
            if self._take() == "-":
                sign = -sign
        return sign * self._primary()

    def _primary(self):
        tok = self._peek()
        if tok is None:
            raise CalculatorError("Пропущен операнд")
        self._take()
        return _parse_number(tok)


def calculate(expression):
    tokens = tokenize(expression)
    validate(tokens)
    return _Evaluator(tokens).expression()