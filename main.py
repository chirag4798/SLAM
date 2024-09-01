import pygame as pg

from slam.sensor import LiDAR
from slam.environment import Environment
from slam.geometry.point import CartesianPoint

environment = Environment(map_file="maps/2.jpg")
environment.original_map = environment.map.copy()
sensor = LiDAR(map=environment.original_map)
environment.map.fill(environment.color_map.get("black"))
environment.info_map = environment.map.copy()
running = True


while running:
    sensor_on = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if pg.mouse.get_focused():
            sensor_on = True
        elif not pg.mouse.get_focused():
            sensor_on = False

        if sensor_on:
            position = pg.mouse.get_pos()
            sensor.position = CartesianPoint.from_tuple(position)
            sensor_data = sensor.sense()
            environment.store(sensor_data)
            environment.show()

        environment.map.blit(environment.info_map, (0, 0))
        pg.display.update()

    pg.display.update()
