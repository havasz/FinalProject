import pygame as py
from pygame.sprite import Sprite

class MH60(Sprite):
    "class for MH60"
    def __init__(self, dd_game):
        super().__init__()
        # initizalize mh60 and starting position
        self.screen = dd_game.screen
        self.settings = dd_game.settings
        self.screen_rect = dd_game.screen.get_rect()

        # load mh60 image original and get rect + resize
        self.original_image = py.image.load("images/mh60.png")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        # resize
        res_image = py.transform.scale(self.image, (100,30))
        res_rect = res_image.get_rect(center = self.rect.center)
        self.image = res_image
        self.rect =  res_rect

        # start position left/middle
        self.rect.left = self.screen_rect.left
        self.rect.top = self.screen_rect.top
        # store decimal value for mh60 horizontal position
        self.x = 0
        self.y = self.screen_rect.height / 2

        #movement flags
        self.moving_r = False
        self.moving_l = False
        self.moving_u = False
        self.moving_d = False


    def update(self):
        "update position based on movement flags"
        # update rect object from self.x/self.y
        if self.moving_r and self.rect.right < self.screen_rect.right:
            self.x += self.settings.mh60_speed
        if self.moving_l and self.rect.left > 0:
            self.x -= self.settings.mh60_speed
        if self.moving_u and self.rect.top > 0:
            self.y -= self.settings.mh60_speed
        if self.moving_d and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.mh60_speed
        # update rect object from self.x/self.y
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        "draw at current location"
        self.screen.blit(self.image, self.rect)

    def center_mh60(self):
        "reset mh60 to bottom left of screen"
        self.rect.y = self.screen_rect.height / 2
        self.rect.left = self.screen_rect.left
