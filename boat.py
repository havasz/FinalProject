import pygame as py
from pygame.sprite import Sprite

class Boat(Sprite):
    "class represent one boat"
    def __init__(self, dd_game):
        super().__init__()
        self.screen = dd_game.screen
        self.settings = dd_game.settings
        self.screen_rect = dd_game.screen.get_rect()

        #load boat image and rect attributes
        self.image = py.image.load("images/boat.png")
        self.rect = self.image.get_rect()

        # start position bottom right screen
        self.rect.right = self.screen_rect.right
        self.rect.bottom = self.screen_rect.bottom

        #store boats horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        self.screen.rect = self.screen.get_rect()
        if self.rect.bottom >= self.screen_rect.bottom or self.rect.top <= 0:
            return True

    def update(self):
        "move boat left"
        self.x -= self.settings.boat_speed
        self.rect.x = self.x
