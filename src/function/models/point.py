import math


class Point:
    def __init__(self, x: float, y: float, is_included: bool = True):
        self.x = x
        self.y = y
        self.is_included = is_included

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def truncate(self, decimals: int = 2):
        ten_pow = 10 ** decimals
        self.x = math.trunc(self.x * ten_pow) / ten_pow
        self.y = math.trunc(self.y * ten_pow) / ten_pow
