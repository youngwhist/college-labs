import pytest
from calculator import add, subtract, multiply, divide, average, is_prime, grade, discount


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(10, 4) == 6


def test_multiply():
    assert multiply(3, 4) == 12


def test_divide():
    assert divide(10, 2) == 5


def test_average():
    assert average([1, 2, 3, 4]) == 2.5


def test_is_prime():
    assert is_prime(7) is True
    assert is_prime(9) is False


def test_grade():
    assert grade(95) == "A"
    assert grade(50) == "F"


def test_discount():
    assert discount(200, 10) == 180
    with pytest.raises(ValueError):
        discount(100, 150)
