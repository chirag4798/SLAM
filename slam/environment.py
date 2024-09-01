import math
import pygame as pg

from typing import Tuple, List
from slam.geometry.point import CartesianPoint


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
        self.point_cloud = set()
        self.external_map = pg.image.load(map_file)
        self.map_w = self.external_map.get_width()
        self.map_h = self.external_map.get_height()

        self.window_name = "SLAM 2D"
        pg.display.set_caption(self.window_name)

        self.map = pg.display.set_mode((self.map_w, self.map_h))
        self.map.blit(self.external_map, (0, 0))

    def store(self, data: List[Tuple[CartesianPoint, CartesianPoint]]):
        for ele in data:
            uncertain_point, position = ele
            uncertain_point = uncertain_point.to_cartesian()
            point = CartesianPoint(
                x=position.x + uncertain_point.x,
                y=position.y + uncertain_point.y,
            )
            self.point_cloud.add(point.to_tuple())

    def show(self):
        self.info_map = self.map.copy()
        for point in self.point_cloud:
            self.info_map.set_at(point, self.color_map.get("red"))
