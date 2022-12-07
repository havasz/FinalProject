import pygame

pygame.mixer.init()

bg_sound = pygame.mixer.Sound("sounds/epic.mp3")
missile_sound = pygame.mixer.Sound("sounds/miss.mp3")
torpedo_sound = pygame.mixer.Sound("sounds/torp.mp3")
explosion = pygame.mixer.Sound("sounds/exp.mp3")