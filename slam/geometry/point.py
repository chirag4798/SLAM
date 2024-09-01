import math

from typing import Annotated
from abc import ABC, abstractmethod
from pydantic import BaseModel, confloat


# Abstract class for Point
class Point(ABC, BaseModel):
    @abstractmethod
    def to_cartesian(self):
        pass

    @abstractmethod
    def to_rotary(self):
        pass

    @classmethod
    @abstractmethod
    def from_tuple(cls):
        pass

    @abstractmethod
    def to_tuple(cls):
        pass

    def euclidean_distance(self, other: "Point") -> float:
        self_cartesian = self.to_cartesian()
        other_cartesian = other.to_cartesian()
        px = (self_cartesian.x - other_cartesian.x) ** 2
        py = (self_cartesian.y - other_cartesian.y) ** 2
        return math.sqrt(px + py)


# CartesianPoint class
class CartesianPoint(Point):
    x: float = confloat(ge=0)  # x-coordinate must be non-negative
    y: float = confloat(ge=0)  # y-coordinate must be non-negative

    def to_cartesian(self):
        return self

    def to_rotary(self):
        angle = math.atan2(self.y, self.x)
        distance = math.sqrt(self.x**2 + self.y**2)
        return RotaryPoint(distance=distance, angle=angle)

    @classmethod
    def from_tuple(cls, point):
        return cls(x=point[0], y=point[1])

    def to_tuple(self):
        return (int(self.x), int(self.y))


# RotaryPoint class
class RotaryPoint(Point):
    distance: float = confloat(ge=0)  # distance must be non-negative
    angle: float = confloat(ge=0)  # angle in radians

    def to_cartesian(self):
        x = int(self.distance * math.cos(self.angle))
        y = int(-self.distance * math.sin(self.angle))
        return CartesianPoint(x=x, y=y)

    def to_rotary(self):
        return self

    @classmethod
    def from_tuple(cls, point):
        return cls(distance=point[0], angle=point[1])

    def to_tuple(self):
        return (self.distance, self.angle)
