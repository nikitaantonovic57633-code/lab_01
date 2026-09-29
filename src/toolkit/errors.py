class ToolkitError(Exception):
    """Базовое исключение для всех утилит."""


class CalculatorError(ToolkitError):
    """Ошибка вычисления выражения."""


class ConverterError(ToolkitError):
    """Ошибка конвертации величин."""