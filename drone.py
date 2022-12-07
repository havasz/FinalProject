import pygame as py
from pygame.sprite import Sprite
import random

class Drone(Sprite):
    "class represent one drone"
    def __init__(self, dd_game):
        super().__init__()
        self.screen = dd_game.screen
        self.settings = dd_game.settings
        self.screen_rect = dd_game.screen.get_rect()

        #load drone image and rect attributes
        # load mh60 image original and get rect + resize
        self.original_image = py.image.load("images/drone.png")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        # resize
        res_image = py.transform.scale(self.image, (55, 25))
        res_rect = res_image.get_rect(center=self.rect.center)
        self.image = res_image
        self.rect = res_rect

        # start position top left screen
        self.rect.right = self.screen_rect.right
        z = random.randint(0, dd_game.settings.screen_height)
        self.rect.y = z

        #store drones horizontal/vertical position
        self.x = float(self.rect.x)
        # self.y = float(self.rect.y)

    def update(self):
        "move boat left/up/down"
        self.x -= self.settings.drone_speed_x
        self.rect.x = self.x
        # self.y += (self.settings.drone_speed_y * self.settings.drone_direction)
        # self.rect.y = self.y
