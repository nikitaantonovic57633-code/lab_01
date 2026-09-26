"""Конвертер величин: длина, масса, температура."""

from .errors import ConverterError

# Коэффициенты к базовой единице:
# для длины база — метр, для массы — килограмм.
_length = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
_mass = {"g": 0.001, "kg": 1.0}

# Какая единица к какой группе относится.
_groups = {
    "mm": "length",
    "cm": "length",
    "m": "length",
    "km": "length",
    "g": "mass",
    "kg": "mass",
    "c": "temperature",
    "f": "temperature",
    "k": "temperature",
}


def convert(value, from_unit, to_unit):
    """Сконвертировать value из from_unit в to_unit."""
    src = _normalize(from_unit)
    dst = _normalize(to_unit)

    if src not in _groups:
        raise ConverterError(f"неизвестная единица: {from_unit}")
    if dst not in _groups:
        raise ConverterError(f"неизвестная единица: {to_unit}")

    if _groups[src] != _groups[dst]:
        raise ConverterError(
            f"несовместимые единицы: {from_unit} и {to_unit}"
        )

    number = _to_float(value)
    group = _groups[src]

    if group == "length":
        result = number * _length[src] / _length[dst]
    elif group == "mass":
        result = number * _mass[src] / _mass[dst]
    else:
        result = _convert_temperature(number, src, dst)

    return round(result, 10)


def _normalize(unit):
    """Привести единицу к нижнему регистру и убрать пробелы."""
    if not isinstance(unit, str):
        raise ConverterError(f"неизвестная единица: {unit}")
    return unit.strip().lower()


def _to_float(value):
    """Превратить значение в float, проверив, что оно число."""
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ConverterError(f"неверное числовое значение: {value}") from exc


def _convert_temperature(value, src, dst):
    """Перевести температуру через Кельвины."""
    kelvin = _to_kelvin(value, src)
    if kelvin < -1e-9:
        raise ConverterError(
            f"температура ниже абсолютного нуля: {value} {src}"
        )
    return _from_kelvin(kelvin, dst)


def _to_kelvin(value, unit):
    if unit == "c":
        return value + 273.15
    if unit == "f":
        return (value + 459.67) * 5.0 / 9.0
    return value  # уже Кельвин


def _from_kelvin(kelvin, unit):
    if unit == "c":
        return kelvin - 273.15
    if unit == "f":
        return kelvin * 9.0 / 5.0 - 459.67
    return kelvin