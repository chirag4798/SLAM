import math
import numpy as np
import pygame as pg

from typing import Tuple, List
from slam.geometry.point import Point, CartesianPoint, RotaryPoint


class LiDAR:

    color_map = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "grey": (128, 128, 128),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
    }

    def __init__(
        self,
        map: pg.surface.Surface,
        uncertainity: Tuple[float] = (0.5, 0.01),
        range: float = 120,
        resolution: int = 100,
    ):
        # Rounds per second
        self.speed = 4
        self.map = map
        self.range = range
        self.resolution = resolution
        self.sigma = np.array(uncertainity)
        self.position = CartesianPoint(x=0, y=0)
        self.map_w, self.map_h = pg.display.get_surface().get_size()
        self.point_cloud = []

    def add_uncertainity(self, point: RotaryPoint) -> List[float]:
        mean = np.array([point.distance, point.angle])
        covariance = np.diag(self.sigma**2)
        distance, angle = np.random.multivariate_normal(mean, covariance)
        uncertain_point = RotaryPoint(
            distance=max(distance, 0),
            angle=max(angle, 0),
        )
        return point

    def sense(self) -> List[Tuple[CartesianPoint, CartesianPoint]]:
        data = []
        for angle in np.linspace(0, 2 * math.pi, self.resolution, False):

            point2 = CartesianPoint(
                x=int(self.position.x + self.range * math.cos(angle)),
                y=int(self.position.y - self.range * math.sin(angle)),
            )

            for iter in range(self.resolution):
                u = iter / 100
                point3 = CartesianPoint(
                    x=int(point2.x * u + self.position.x * (1 - u)),
                    y=int(point2.y * u + self.position.y * (1 - u)),
                )

                if not ((0 < point3.x < self.map_w) and (0 < point3.y < self.map_h)):
                    continue

                color = tuple(self.map.get_at(point3.to_tuple()))[:3]
                if not (color == self.color_map.get("black")):
                    continue

                distance = Point.euclidean_distance(point3, self.position)
                point = RotaryPoint(distance=distance, angle=angle)
                point = self.add_uncertainity(point).to_cartesian()
                data.append((point, self.position))
                break

        return data
