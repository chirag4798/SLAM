import math
import pygame as pg

from typing import Tuple, List


class Environment:

    color_map = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "grey": (128, 128, 128),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
    }

    def __init__(self, map_file: str = "maps/2.jpg"):
        pg.init()
        self.point_cloud = []
        self.external_map = pg.image.load(map_file)
        self.map_w = self.external_map.get_width()
        self.map_h = self.external_map.get_height()

        self.window_name = "SLAM 2D"
        pg.display.set_caption(self.window_name)

        self.map = pg.display.set_mode((self.map_w, self.map_h))
        self.map.blit(self.external_map, (0, 0))

    @staticmethod
    def ad_to_pos(distance: float, angle: float, position: Tuple[int]) -> Tuple[int]:
        x = int(distance * math.cos(angle) + position[0])
        y = int(-distance * math.sin(angle) + position[1])
        return (x, y)

    def store(self, data: List[List[float]]):
        for ele in data:
            point = self.ad_to_pos(*ele)
            if point not in self.point_cloud:
                self.point_cloud.append(point)

    def show(self):
        self.info_map = self.map.copy()
        for point in self.point_cloud:
            self.info_map.set_at(point, self.color_map.get("red"))
