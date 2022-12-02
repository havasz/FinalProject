import pygame as py
from pygame.sprite import Sprite

class Torpedo(Sprite):
    "class to manage torpedos"
    def __init__(self, dd_game):
        super().__init__()
        self.screen = dd_game.screen
        self.settings = dd_game.settings
        self.color = self.settings.torpedo_color

        # create torpedo at (0,0) then correct position
        self.rect = py.Rect(0,0,self.settings.torpedo_width,self.settings.torpedo_height)
        self.rect.midright = dd_game.ddg.rect.midright
        self.rect.y = dd_game.ddg.rect.y + 80

        # store position as decimal
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        "move torpedo right"
        # update decimal position
        self.x += self.settings.torpedo_speed
        #update rect position
        self.rect.x = self.x

    def draw_torpedo(self):
        "draw torpedo on screen"
        py.draw.rect(self.screen, self.color, self.rect)