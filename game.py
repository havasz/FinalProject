import pygame
import pygame as py
from pygame.locals import *
import sys
# import time
from settings import Settings
from button import Button
from scoreboard import Scoreboard
from game_stats import GameStats
from ddg import DDG
from mh60 import MH60
from boat import Boat
from drone import Drone
from torpedo import Torpedo
from missile import Missile
import sound_effects as se


class DdgDefense:
    """overall class to manage all game aspects and behaviors"""
    def __init__(self):
        """initialize game and create all resources"""
        py.init()  # initilize
        # music and sound effects

        # screen and background
        self.settings = Settings()
        self.screen = py.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.bg = py.image.load("images/bg.png")
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.bg = py.transform.scale(self.bg, (self.settings.screen_width,self.settings.screen_height))
        self.i = 0
        py.display.set_caption("DDG Defense")
        # stores games stats and creates scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # reference my classes
        self.ddg = DDG(self)
        self.mh60 = MH60(self)
        self.boats = py.sprite.Group()
        self.drones = py.sprite.Group()
        self.torpedos = py.sprite.Group()
        self.missiles = py.sprite.Group()
        # makes play button
        self.play_button = Button(self, "Play")
        self.play_game = False
        self.show_instructions = False
        self.show_start = True
        # background music
        se.bg_sound.play()

    def run_game(self):
        """main loop for game"""
        while True:
            self.check_events()
            if self.play_game:
                self.game()
            elif self.show_instructions:
                self.instructions()
            elif self.show_start:
                self.start_screen()

    def check_events(self):
        """responses to pressing key or clicking mouse"""
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == py.KEYUP:
                self.check_keyup_events(event)
            elif event.type == py.MOUSEBUTTONDOWN:
                mouse_pos = py.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def start_screen(self):
        self.screen.fill((0, 0, 0))
        start = py.image.load("images/start.png")
        start = py.transform.scale(start, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(start,(0,0))
        py.display.flip()

    def instructions(self):
        self.screen.fill((0,0,0))
        instructions = py.image.load("images/instructions.png")
        instructions = py.transform.scale(instructions, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(instructions, (0,0))
        py.display.flip()

    def game(self):
        if self.stats.game_active:
            # self.check_events()
            self.ddg.update()
            self.mh60.update()
            self.update_boats()
            self.update_drones()
            self.update_torpedos()
            self.update_missiles()
        self.update_screen()

    def check_play_button(self, mouse_pos):
        """start new game when player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            # reset game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_health()
            # delete remaining boats/drones and missiles/torpedos
            self.boats.empty()
            self.drones.empty()
            self.missiles.empty()
            self.torpedos.empty()
            # center ddg/mh60 and create enemy attack
            self.create_attack()
            self.ddg.center_ddg()
            self.mh60.center_mh60()
            # hides mouse cursor
            pygame.mouse.set_visible(False)

    def check_keydown_events(self, event):
        if event.key == py.K_RIGHT:
            self.ddg.moving_r = True
        elif event.key == py.K_LEFT:
            self.ddg.moving_l = True
        elif event.key == py.K_w:
            self.mh60.moving_u = True
        elif event.key == py.K_s:
            self.mh60.moving_d = True
        elif event.key == py.K_a:
            self.mh60.moving_l = True
        elif event.key == py.K_d:
            self.mh60.moving_r = True
        elif event.key == py.K_q:
            sys.exit()
        elif event.key == py.K_p:
            self.play_game = True
        elif event.key == py.K_i:
            self.show_instructions = True
        elif event.key == py.K_SPACE:
            self.fire_torpedos()
        elif event.key == py.K_f:
            self.fire_missiles()

    def check_keyup_events(self, event):
        if event.key == py.K_RIGHT:
            self.ddg.moving_r = False
        elif event.key == py.K_LEFT:
            self.ddg.moving_l = False
        elif event.key == py.K_w:
            self.mh60.moving_u = False
        elif event.key == py.K_s:
            self.mh60.moving_d = False
        elif event.key == py.K_a:
            self.mh60.moving_l = False
        elif event.key == py.K_d:
            self.mh60.moving_r = False

    def fire_missiles(self):
        """create missile and add to missile group"""
        if len(self.missiles) < self.settings.missiles_allowed:
            new_missile = Missile(self)
            self.missiles.add(new_missile)
            se.missile_sound.play()

    def update_missiles(self):
        """update position and get rid of old missiles"""
        self.missiles.update()
        for missile in self.missiles.copy():
            if missile.rect.left >= self.screen.get_width():
                self.missiles.remove(missile)
        self.check_missile_collisions()

    def check_missile_collisions(self):
        """ respond to missile collisions with drones / boats """
        collision_boat_missile = pygame.sprite.groupcollide(self.missiles, self.boats, True, True)
        if collision_boat_missile:
            self.stats.score += self.settings.boat_points
            self.sb.prep_score()
            self.sb.check_high_score()
            se.explosion.play()
        collision_drone_missile = pygame.sprite.groupcollide(self.missiles, self.drones, True, True)
        if collision_drone_missile:
            self.stats.score += self.settings.drone_points
            self.sb.prep_score()
            self.sb.check_high_score()
            se.explosion.play()

    def fire_torpedos(self):
        """create torpedo and add to torpedo group"""
        if len(self.torpedos) < self.settings.torpedos_allowed:
            new_torpedo = Torpedo(self)
            self.torpedos.add(new_torpedo)
            se.torpedo_sound.play()

    def update_torpedos(self):
        """update position and get rid of old torpedo"""
        self.torpedos.update()
        for torpedo in self.torpedos.copy():
            if torpedo.rect.left >= self.screen.get_width():
                self.torpedos.remove(torpedo)
        self.check_torpedo_collisions()

    def check_torpedo_collisions(self):
        """respond to torpedo collisions with boats """
        collision_boat_torpedo = pygame.sprite.groupcollide(self.torpedos, self.boats, True, True)
        if collision_boat_torpedo:
            self.stats.score += self.settings.boat_points
            self.sb.prep_score()
            self.sb.check_high_score()
            se.explosion.play()
        collision_drone_torpedo = pygame.sprite.groupcollide(self.torpedos, self.drones, True, True)
        if collision_drone_torpedo:
            self.stats.score += self.settings.drone_points
            self.sb.prep_score()
            self.sb.check_high_score()
            se.explosion.play()

    def update_boats(self):
        """check for boat and ddg/hm60 collisions"""
        self.boats.update()
        if py.sprite.spritecollideany(self.ddg, self.boats):
            self.boat_ddg_hit()
        elif py.sprite.spritecollideany(self.mh60, self.boats):
            self.boat_mh60_hit()

    def update_drones(self):
        """check for drone and ddg/hm60 collisions"""
        if py.sprite.spritecollideany(self.ddg, self.drones):
            self.drone_ddg_hit()
        elif py.sprite.spritecollideany(self.mh60, self.drones):
            self.drone_mh60_hit()

    def boat_ddg_hit(self):
        """respond to boat ddg collison"""
        se.explosion.play()
        if self.stats.health > 0:
            # decrease health points and update scoreboard
            self.stats.health -= 10
            self.sb.prep_health()
            for self.boat in self.boats:
                self.boats.remove(self.boat)
        if self.stats.health <= 0:
            self.stats.game_active = False
            # delete remaining boats/drones and missiles/torpedos
            self.boats.empty()
            self.drones.empty()
            self.missiles.empty()
            self.torpedos.empty()
            # center ddg/mh60 and create enemy attack
            self.create_attack()
            self.ddg.center_ddg()
            self.mh60.center_mh60()
            py.mouse.set_visible(True)

    def drone_ddg_hit(self):
        """respond to drone ddg collison"""
        se.explosion.play()
        if self.stats.health > 0:
            # decrease health points and update scoreboard
            self.stats.health -= 5
            self.sb.prep_health()
            for self.drone in self.drones:
                self.drones.remove(self.drone)
        if self.stats.health <= 0:
            self.stats.game_active = False
            # delete remaining boats/drones and missiles/torpedos
            self.boats.empty()
            self.drones.empty()
            self.missiles.empty()
            self.torpedos.empty()
            # center ddg/mh60 and create enemy attack
            self.create_attack()
            self.ddg.center_ddg()
            self.mh60.center_mh60()
            py.mouse.set_visible(True)

    def boat_mh60_hit(self):
        """respond to boat mh60 collison"""
        se.explosion.play()
        if self.stats.health > 0:
            # decrease health points and update scoreboard
            self.stats.health -= 25
            self.sb.prep_health()
            for self.boat in self.boats:
                self.boats.remove(self.boat)
        if self.stats.health <= 0:
            self.stats.game_active = False
            # delete remaining boats/drones and missiles/torpedos
            self.boats.empty()
            self.drones.empty()
            self.missiles.empty()
            self.torpedos.empty()
            # center ddg/mh60 and create enemy attack
            self.create_attack()
            self.ddg.center_ddg()
            self.mh60.center_mh60()
            py.mouse.set_visible(True)

    def drone_mh60_hit(self):
        """respond to drone mh60 collison"""
        se.explosion.play()
        if self.stats.health > 0:
            # decrease health points and update scoreboard
            self.stats.health -= 15
            self.sb.prep_health()
            for self.drone in self.drones:
                self.drones.remove(self.drone)
        if self.stats.health <= 0:
            self.stats.game_active = False
            # delete remaining boats/drones and missiles/torpedos
            self.boats.empty()
            self.drones.empty()
            self.missiles.empty()
            self.torpedos.empty()
            # center ddg/mh60 and create enemy attack
            self.create_attack()
            self.ddg.center_ddg()
            self.mh60.center_mh60()
            py.mouse.set_visible(True)

    def update_screen(self):
        """update images on the screen and flip to new screen"""
        # scrolling background thank you Eli
        self.screen.blit(self.bg,(self.i, 0))
        self.screen.blit(self.bg, (self.settings.screen_width + self.i, 0))
        if self.i == -self.settings.screen_width:
            self.screen.blit(self.bg, (self.settings.screen_width + self.i, 0))
            self.i = 0
        self.i -= 0.5
        self.ddg.blitme()
        self.mh60.blitme()
        for missile in self.missiles.sprites():
            missile.draw_missile()
        for torpedo in self.torpedos.sprites():
            torpedo.draw_torpedo()
        self.update_boats()
        self.boats.draw(self.screen)
        self.update_drones()
        self.drones.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        py.display.flip()

    def create_attack(self):
        boat = Boat(self)
        self.boats.add(boat)
        drone = Drone(self)
        self.drones.add(drone)


if __name__ == "__main__":
    dd = DdgDefense()
    dd.run_game()