import pygame as py
from pygame.sprite import Sprite

class Missile(Sprite):
    "class to manage missiles"
    def __init__(self, dd_game):
        super().__init__()
        self.screen = dd_game.screen
        self.settings = dd_game.settings
        self.color = self.settings.missile_color

        # create missile at (0,0) then correct position
        self.rect = py.Rect(0,0,self.settings.missile_width,self.settings.missile_height)
        self.rect.midright = dd_game.mh60.rect.midright
        self.rect.y = dd_game.mh60.rect.y + 20

        # store position as decimal
        self.x = float(self.rect.x)

    def update(self):
        "move missile right"
        # update decimal position
        self.x += self.settings.missile_speed
        #update rect position
        self.rect.x = self.x

    def draw_missile(self):
        "draw misslie on screen"
        py.draw.rect(self.screen, self.color, self.rect)