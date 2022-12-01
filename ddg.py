import pygame as py
from pygame.sprite import Sprite

class DDG(Sprite):
    "class for DDG"
    def __init__(self, dd_game):
        super().__init__()
        # initizalize ddg and starting position
        self.screen = dd_game.screen
        self.settings = dd_game.settings
        self.screen_rect = dd_game.screen.get_rect()

        # load ddg image original and get rect + resize
        self.original_image = py.image.load("images/ddg.png")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        # resize
        res_image = py.transform.scale(self.image, (300,100))
        res_rect = res_image.get_rect(center = self.rect.center)
        self.image = res_image
        self.rect =  res_rect

        # start position left/bottom
        self.rect.left = self.screen_rect.left
        self.rect.bottom = self.screen_rect.bottom
        # store decimal value for ddg horizontal position
        self.x = float(self.rect.x)

        #movement flags
        self.moving_r = False
        self.moving_l = False

    def update(self):
        "update position based on movement flags"
        if self.moving_r and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ddg_speed
        if self.moving_l and self.rect.left > 0:
            self.x -= self.settings.ddg_speed
        #update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        "draw at current location"
        self.screen.blit(self.image, self.rect)

    def center_ddg(self):
        "reset ddg to bottom left of screen"
        self.rect.bottom = self.screen_rect.bottom
        self.rect.left = self.screen_rect.left
