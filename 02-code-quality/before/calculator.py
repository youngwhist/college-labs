import math
import os

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return None
    return a / b

def average(numbers):
    total = 0
    for n in numbers:
        total = total + n
    return total / len(numbers)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def grade(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "F"

def discount(price, percent, Unused=None):
    if percent < 0 or percent > 100:
        raise ValueError("bad percent")
    result = price - price * percent / 100
    return round(result, 2)
