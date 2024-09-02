import math
import numpy as np

from fractions import Fraction
from pydantic import BaseModel
from abc import ABC, abstractmethod
from geometry.point import Point, CartesianPoint


# Abstract class for Line
class Line(ABC, BaseModel):
    @abstractmethod
    def to_general_form(self):
        pass

    @abstractmethod
    def to_slope_intercept_form(self):
        pass

    @abstractmethod
    def slope(self) -> float:
        pass

    @abstractmethod
    def intercept(self) -> float:
        pass

    def get_intersection(self, other: "Line"):
        self_slope = self.to_slope_intercept_form().slope
        other_slope = other.to_slope_intercept_form().slope

        if self_slope == other_slope:
            raise ValueError("Two lines are parallel!")

        self = self.to_general_form()
        other = other.to_general_form()

        return Point(
            x=(self.C * other.B - self.B * other.C)
            / (self.B * other.A - self.A * other.B),
            y=(self.A * other.C - self.C * other.A)
            / (self.B * other.A - self.A * other.B),
        )

    def distance_from_point(self, point: Point):
        point = point.to_cartesian()
        line = self.to_general_form()
        numerator = abs(line.A * point.x + line.B * point.y + line.C)
        denominator = math.sqrt(line.A**2 + line.B**2)
        return numerator / denominator

    def get_points(self, x1=5, x2=2000):
        line = self.to_slope_intercept_form()
        point1 = CartesianPoint(
            x=x1,
            y=line.slope * x1 + line.intercept,
        )
        point2 = CartesianPoint(
            x=x2,
            y=line.slope * x2 + line.intercept,
        )
        return (point1, point2)


# GeneralFormLine class
class GeneralFormLine(Line):
    A: float  # Coefficient of x
    B: float  # Coefficient of y
    C: float  # Constant term

    def to_general_form(self):
        return self

    def to_slope_intercept_form(self, epsilon=1e-6):
        self.B = max(self.B, epsilon)
        slope = -self.A / self.B
        intercept = -self.C / self.B
        return SlopeInterceptLine(slope=slope, intercept=intercept)

    def slope(self, epsilon=1e-6) -> float:
        self.B = max(self.B, epsilon)
        return -self.A / self.B

    def intercept(self) -> float:
        return -self.C / self.B


# SlopeInterceptLine class
class SlopeInterceptLine(Line):
    slope: float  # Slope of the line
    intercept: float  # y-intercept of the line

    def to_general_form(self):
        B = 1
        A = -self.slope
        C = -self.intercept
        if A >= 0:
            return GeneralFormLine(A=A, B=B, C=C)

        A, B, C = -A, -B, -C
        denominator_A = Fraction(A).limit_denominator(1000).as_integer_ratio()[1]
        denominator_C = Fraction(C).limit_denominator(1000).as_integer_ratio()[1]
        gcd = np.gcd(denominator_A, denominator_C)
        lcm = denominator_A * denominator_C / gcd

        A *= lcm
        B *= lcm
        C *= lcm
        return GeneralFormLine(A=A, B=B, C=C)

    def to_slope_intercept_form(self):
        return self

    def slope(self) -> float:
        return self.slope

    def intercept(self) -> float:
        return self.intercept
