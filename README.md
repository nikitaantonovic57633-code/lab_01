# toolkit

Консольный набор утилит: калькулятор выражений и конвертер величин.

## Установка


pip install -e .
## Использование

python -m toolkit calc "1 + 2 * 3"
python -m toolkit calc "-5 + 2.5"


python -m toolkit convert 100 --from cm --to m
python -m toolkit convert 100 --from c --to f


python -m toolkit --help

## Возможности калькулятора
целые и вещественные числа;

операторы + - * /;

унарные + и - перед числом;

пробелы игнорируются;

приоритет *// над +/-;

запрещены eval, exec, ast.literal_eval и сторонние парсеры —
реализован собственный токенизатор и рекурсивный спуск.

## Возможности конвертера
длина: mm, cm, m, km;

масса: g, kg;

температура: c, f, k;

регистр единиц не учитывается;

запрещена конвертация между разными группами;

запрещена температура ниже абсолютного нуля;

результат — всегда float.

## Ошибки
Все ошибки выводятся в stderr, код возврата — 2. Успешные команды
возвращают 0.

---

## `lab_01/src/toolkit/__init__.py`

```python
"""Toolkit: консольный калькулятор и конвертер величин."""

from .calculator import calculate, tokenize, validate
from .converter import convert
from .errors import CalculatorError, ConverterError, ToolkitError

__all__ = [
    "calculate",
    "tokenize",
    "validate",
    "convert",
    "CalculatorError",
    "ConverterError",
    "ToolkitError",
]