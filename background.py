import pygame as py

class Background:
    def __init__(self, dd_game):
        self.screen = dd_game.screen
        self.bg = py.image.load('AnimatedStreet.png')
        self.rect = self.bg.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rect.height
        self.bgX2 = 0

        self.movingUpSpeed = 5

    def update(self):
        self.bgY1 -= self.movingUpSpeed
        self.bgY2 -= self.movingUpSpeed
        if self.bgY1 <= -self.rect.height:
            self.bgY1 = self.rect.height
        if self.bgY2 <= -self.rect.height:
            self.bgY2 = self.rect.height

    def render(self):
        self.screen.blit(self.bg, (self.bgX1, self.bgY1))
        self.screen.blit(self.bg, (self.bgX2, self.bgY2))
