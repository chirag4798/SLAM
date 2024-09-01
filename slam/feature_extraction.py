import math
import numpy as np
from typing import Tuple
from fractions import Fraction
from slam.geometry.point import GeneralLineParams


class FeatureDetector:
    def __init__(self):
        self.EPSILON = 10
        self.DELTA = 501
        self.SNUM = 6
        self.PMIN = 20
        self.GMAX = 20
        self.SEED_SEGMENTS = []
        self.LINE_SEGMENTS = []
        self.LASER_POINTS = []
        self.LINE_PARAMS = None
        self.NP = len(self.LASER_POINTS) - 1
        self.LMIN = 20  # Minimum length of line segment
        self.LR = 0  # Real length of line segment
        self.PR = 0  # Number of Laser Points contained in Line Segment

    @staticmethod
    def euclidean_distance(point1: Tuple[int], point2: Tuple[int]) -> float:
        px = (point1[0] - point2[0]) ** 2
        py = (point1[1] - point2[1]) ** 2
        return math.sqrt(px + py)

    @staticmethod
    def dist_point_to_line(line: GeneralLineParams, point: Tuple[int]) -> float:
        numerator = abs(line.a * point[0] + line.b * point[1] + line.c)
        deominator = math.sqrt(line.a**2 + line.b**2)
        return numerator / deominator
