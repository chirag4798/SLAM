from abc import ABC, abstractmethod
from pydantic import BaseModel, confloat


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


# GeneralFormLine class
class GeneralFormLine(Line):
    A: float  # Coefficient of x
    B: float  # Coefficient of y
    C: float  # Constant term

    def to_general_form(self):
        return self

    def to_slope_intercept_form(self):
        if self.B == 0:
            raise ValueError("Vertical line: cannot convert to slope-intercept form.")
        slope = -self.A / self.B
        intercept = -self.C / self.B
        return SlopeInterceptLine(slope=slope, intercept=intercept)

    def slope(self) -> float:
        if self.B == 0:
            raise ValueError("Vertical line: slope is undefined.")
        return -self.A / self.B

    def intercept(self) -> float:
        return -self.C / self.B


# SlopeInterceptLine class
class SlopeInterceptLine(Line):
    slope: float  # Slope of the line
    intercept: float  # y-intercept of the line

    def to_general_form(self):
        A = -self.slope
        B = 1
        C = -self.intercept
        return GeneralFormLine(A=A, B=B, C=C)

    def to_slope_intercept_form(self):
        return self

    def slope(self) -> float:
        return self.slope

    def intercept(self) -> float:
        return self.intercept


# Example usage
if __name__ == "__main__":
    general_line = GeneralFormLine(A=2, B=3, C=6)
    slope_intercept_line = general_line.to_slope_intercept_form()

    print(f"General Form Line: {general_line}")
    print(f"Slope-Intercept Form Line: {slope_intercept_line}")

    # Calculate slope and intercept
    print(f"Slope of General Form Line: {general_line.slope()}")
    print(f"Intercept of General Form Line: {general_line.intercept()}")

    # Convert back to General Form from Slope-Intercept Form
    converted_general = slope_intercept_line.to_general_form()
    print(f"Converted back to General Form: {converted_general}")
