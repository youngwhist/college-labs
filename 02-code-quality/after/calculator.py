"""Модуль простых математических операций."""
import math


def add(a, b):
    """Возвращает сумму двух чисел."""
    return a + b


def subtract(a, b):
    """Возвращает разность двух чисел."""
    return a - b


def multiply(a, b):
    """Возвращает произведение двух чисел."""
    return a * b


def divide(a, b):
    """Делит a на b. Возвращает None при делении на ноль."""
    if b == 0:
        return None
    return a / b


def average(numbers):
    """Возвращает среднее арифметическое списка чисел."""
    if not numbers:
        raise ValueError("Список чисел пуст")
    return sum(numbers) / len(numbers)


def is_prime(n):
    """Проверяет, является ли число простым."""
    if n < 2:
        return False
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False
    return True


def grade(score):
    """Переводит балл в буквенную оценку."""
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    return "F"


def discount(price, percent):
    """Возвращает цену со скидкой percent процентов."""
    if percent < 0 or percent > 100:
        raise ValueError("Процент скидки должен быть от 0 до 100")
    result = price - price * percent / 100
    return round(result, 2)
