"""Тесты для модуля calculator."""
import pytest
from calculator import add, subtract, multiply, divide, average, is_prime, grade, discount


def test_add():
    """Сложение."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    """Вычитание."""
    assert subtract(10, 4) == 6


def test_multiply():
    """Умножение."""
    assert multiply(3, 4) == 12
    assert multiply(5, 0) == 0


def test_divide():
    """Деление, в том числе на ноль."""
    assert divide(10, 2) == 5
    assert divide(1, 0) is None


def test_average():
    """Среднее и пустой список."""
    assert average([1, 2, 3, 4]) == 2.5
    with pytest.raises(ValueError):
        average([])


@pytest.mark.parametrize("n, expected", [(0, False), (1, False), (2, True), (7, True), (9, False)])
def test_is_prime(n, expected):
    """Простые и составные числа, граничные значения."""
    assert is_prime(n) is expected


@pytest.mark.parametrize("score, expected", [(95, "A"), (90, "A"), (80, "B"), (60, "C"), (59, "F")])
def test_grade(score, expected):
    """Все ветки оценок и границы."""
    assert grade(score) == expected


def test_discount():
    """Скидка и неверный процент."""
    assert discount(200, 10) == 180
    assert discount(99.99, 0) == 99.99
    with pytest.raises(ValueError):
        discount(100, 150)
    with pytest.raises(ValueError):
        discount(100, -5)
