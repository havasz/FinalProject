import pygame as py

class Settings:
    def __init__(self):
        "Initialize the game's settings"
        # Screen settings
        self.screen_width = 600
        self.screen_height = 400
        self.bg = py.image.load("images/bg.png")

        # ddg/mh60 settings
        self.ddg_speed = 0.5
        self.mh60_speed = 1.5
        self.health = 500

        # weapons settings
        self.torpedo_speed = 5.0
        self.torpedo_height = 10
        self.torpedo_width = 80
        self.torpedo_color = (54 ,54 , 54)
        self.torpedos_allowed = 1

        self.missile_speed = 2.5
        self.missile_height = 5
        self.missile_width = 20
        self.missile_color = (100, 1, 1)
        self.missiles_allowed = 2

        # change dynamic settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        # boat/drone settings
        self.boat_speed = 1.0
        self.drone_speed_x = 1.0
        self.drone_speed_y = 1.5
        self.drone_direction = -1.0
        self.boat_points = 100
        self.drone_points = 50

    def increase_speed(self):
        self.boat_speed *= self.speedup_scale
        self.drone_speed_x *= self.speedup_scale
        self.drone_speed_y *= self.speedup_scale
        self.drone_direction *= self.speedup_scale
        self.boat_points = int(self.boat_points * self.score_scale)
        self.drone_points = int(self.drone_points * self.score_scale)
