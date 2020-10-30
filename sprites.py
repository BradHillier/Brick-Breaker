import pygame
from settings import *
from random import choice
from pygame.locals import (
    K_LEFT,
    K_RIGHT
)


class Brick(pygame.sprite.Sprite):

    def __init__(self, game, x, y, color):
        super().__init__()
        self.game = game
        sprite = self.game.brick_sheet.image_at(color, (0,0,0))
        self.image = pygame.transform.scale(sprite, (64, 32))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.last_update = pygame.time.get_ticks()

    def update(self):
        pass

    def flash(self):
        pass


class Paddle(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        sprite = self.game.paddle_sheet.image_at(9, (0,0,0))
        self.image = pygame.transform.scale(sprite, (128, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.lives = 3

    def update(self):
        mouse_x = pygame.mouse.get_pos()[0]
        self.rect.x = mouse_x

        # Keep player on screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Ball(pygame.sprite.Sprite):

    def __init__(self, assets, game):
        super().__init__()
        self.game = game
        sprite = assets.ball_sheet.image_at(4, (0,0,0))
        self.image = pygame.transform.scale(sprite, (16, 16))
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(self.game.player.rect.midtop)
        self.reset_speed()
        self.serving = True

    def reset_speed(self):
        self.vel = pygame.math.Vector2(0, -BALL_SPEED)
        self.dx = 0
        self.dy = -BALL_SPEED

    def update(self):

        self.prev = self.rect.copy()

        # Bounce ball off edge of screen
        if self.rect.top < HUD_SIZE:
            self.rect.top = HUD_SIZE
            self.vel.y = -self.vel.y
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel.x = -self.vel.x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vel.x = -self.vel.x

        # Update position
        if self.serving:
            self.pos.update(self.game.player.rect.midtop)
            self.pos.y -= 10
        else:
            self.pos += self.vel
        self.rect.center = self.pos
