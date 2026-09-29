from .errors import ConverterError

_length = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
_mass = {"g": 0.001, "kg": 1.0}

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
    src = _normalize(from_unit)
    dst = _normalize(to_unit)

    if src not in _groups:
        raise ConverterError(f"Неизвестная единица: {from_unit}")
    if dst not in _groups:
        raise ConverterError(f"Неизвестная единица: {to_unit}")

    if _groups[src] != _groups[dst]:
        raise ConverterError(f"Несовместимые единицы: {from_unit} и {to_unit}")

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
    if not isinstance(unit, str):
        raise ConverterError(f"Неизвестная единица: {unit}")
    return unit.strip().lower()


def _to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ConverterError(f"Неверное числовое значение: {value}") from exc


def _convert_temperature(value, src, dst):
    kelvin = _to_kelvin(value, src)
    if kelvin < 0:
        raise ConverterError(f"Температура ниже абсолютного нуля: {value} {src}")
    return _from_kelvin(kelvin, dst)


def _to_kelvin(value, unit):
    if unit == "c":
        return value + 273.15
    if unit == "f":
        return (value + 459.67) * 5.0 / 9.0
    return value


def _from_kelvin(kelvin, unit):
    if unit == "c":
        return kelvin - 273.15
    if unit == "f":
        return kelvin * 9.0 / 5.0 - 459.67
    return kelvin