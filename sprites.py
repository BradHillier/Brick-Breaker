import pygame
from settings import *
from random import choice
from pygame.locals import (
    K_LEFT,
    K_RIGHT
)


class Brick(pygame.sprite.Sprite):

    def __init__(self, width, height, x, y, color):
        super().__init__()
        self.surface = pygame.Surface((width, height))
        color = BRICK_COLORS[color]
        self.surface.fill(color)
        self.rect = self.surface.get_rect(topleft=(x, y))


class Paddle(pygame.sprite.Sprite):

    def __init__(self, game, width, height, x, y):
        super().__init__()
        self.game = game
        self.surface = pygame.Surface((width, height))
        self.surface.fill((255, 255, 255))
        self.rect = self.surface.get_rect(center=(x, y))
        self.lives = 3

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a]:
            self.rect.move_ip(-15, 0)
        if pressed_keys[pygame.K_h]:
            self.rect.move_ip(15, 0)
        # Keep player on screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Ball(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.surface = pygame.Surface((20, 20))
        self.surface.fill((255, 255, 255))
        self.rect = self.surface.get_rect(
                midbottom=self.game.player.rect.midtop
        )
        # Start in random direction
        self.dx = 10
        self.dy = -10
        self.serving = True

    def update(self):

        # Bounce ball off edge of screen
        if self.rect.top < HUD_SIZE:
            self.rect.top = HUD_SIZE
            self.dy = - self.dy
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx = - self.dx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.dx = - self.dx

        # Update position
        if self.serving:
            self.rect.midbottom = self.game.player.rect.midtop
            self.rect.y -= 2
        else:
            self.rect.move_ip(self.dx, self.dy)
