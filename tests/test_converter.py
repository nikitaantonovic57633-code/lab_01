import pytest

from toolkit.converter import convert
from toolkit.errors import ConverterError

# Поддержать группы:
# Длина: mm, cm, m, km.
def test_length():
    assert convert(10, "mm", "cm") == 1.0
    assert convert(100, "cm", "m") == 1.0
    assert convert(1000, "m", "km") == 1.0
    assert convert(1, "km", "mm") == 1000000.0
# Масса: g, kg.
def test_mass():
    assert convert(1000, "g", "kg") == 1.0
    assert convert(500, "kg", "g") == 500000.0
# Температура: c, f, k.
def test_temperature():
    assert convert(100, "c", "f") == pytest.approx(212.0)
    assert convert(0, "c", "k") == pytest.approx(273.15)
    assert convert(32, "f", "c") == pytest.approx(0.0)


# Регистр единиц не учитывается.
def test_register():
    assert convert(1, "M", "CM") == 100.0
    assert convert(1, "KG", "G") == 1000.0


# Конвертация между разными группами запрещена.
def test_dif_groups():
    with pytest.raises(ConverterError):
        convert(1, "m", "kg")
    with pytest.raises(ConverterError):
        convert(1, "km", "c")


# Температура ниже абсолютного нуля запрещена.
def test_zero():
    assert convert(-273.15, "c", "k") == pytest.approx(0.0)

def test_below_zero():
    with pytest.raises(ConverterError):
        convert(-300, "c", "k")
    with pytest.raises(ConverterError):
        convert(-1, "k", "c")


# Результат возвращается как float.
def test_float():
    assert isinstance(convert(1, "m", "cm"), float)


# Неизвестная единица.
def test_unknown():
    with pytest.raises(ConverterError):
        convert(1, "xyz", "m")