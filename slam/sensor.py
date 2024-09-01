import math
import numpy as np
import pygame as pg

from typing import Tuple, List


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
        resolution: int = 30,
    ):
        # Rounds per second
        self.speed = 4
        self.map = map
        self.range = range
        self.position = (0, 0)
        self.resolution = resolution
        self.sigma = np.array(uncertainity)
        self.map_w, self.map_h = pg.display.get_surface().get_size()
        self.point_cloud = []

    def euclidean_distance(self, point: Tuple[int]) -> float:
        px = (point[0] - self.position[0]) ** 2
        py = (point[1] - self.position[1]) ** 2
        return math.sqrt(px + py)

    def add_uncertainity(self, distance: float, angle: float) -> List[float]:
        mean = np.array([distance, angle])
        covariance = np.diag(self.sigma**2)
        distance, angle = np.random.multivariate_normal(mean, covariance)
        distance = max(distance, 0)
        angle = max(angle, 0)
        return [distance, angle]

    def sense(self) -> List[List[float]]:
        data = []
        x1, y1 = self.position
        for angle in np.linspace(0, 2 * math.pi, self.resolution, False):
            x2, y2 = (x1 + self.range * math.cos(angle)), (
                y1 - self.range * math.sin(angle)
            )
            for i in range(100):
                u = i / 100
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))

                if not ((0 < x < self.map_w) and (0 < y < self.map_h)):
                    continue

                color = tuple(self.map.get_at((x, y)))[:3]
                if not (color == self.color_map.get("black")):
                    continue

                distance = self.euclidean_distance((x, y))
                output = self.add_uncertainity(distance, angle)
                output.append(self.position)
                data.append(output)
                break

        return data
