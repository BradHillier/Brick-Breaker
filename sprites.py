import pygame as pg
from settings import *
from random import choice, randint
from math import sqrt
from os import path


class PowerUp(pg.sprite.DirtySprite):
    def __init__(self, game, pos):
        super().__init__()
        self.game = game
        self.num = randint(0, 4)
        sprite = game.powerup_sheet.image_at(self.num, (0,0,0))
        self.image = pg.transform.scale(sprite, (32, 32))
        self.rect = self.image.get_rect(center = pos)
        # Choose image based on image_number or dict key

    def update(self):
        "Move towards the bottom of the screen"
        self.rect.y += 2
        self.dirty = 1

    def action(self, pos):
        playing = self.game.possible_states['playing']
        if self.num == 0:
            playing.player.lives += 1
        if self.num == 1:
            playing.player.lives -= 1
        if self.num == 2:
            # speed up ball
            for ball in playing.balls:
                speed = sqrt(ball.vel.x ** 2 + ball.vel.y ** 2)
                new_speed = speed + 1
                ball.vel.x = (ball.vel.x * new_speed) / speed
                ball.vel.y = (ball.vel.y * new_speed) / speed
        if self.num == 3:
            # slow down ball
            for ball in playing.balls:
                speed = sqrt(ball.vel.x ** 2 + ball.vel.y ** 2)
                new_speed = speed - 1
                ball.vel.x = (ball.vel.x * new_speed) / speed
                ball.vel.y = (ball.vel.y * new_speed) / speed
        if self.num == 4:
            # new ball
            new_ball = Ball(self.game, playing)
            new_ball.serving = False
            new_ball.pos = pos
            new_ball.vel.x = randint(1, floor(BALL_SPEED - 1))
            new_ball.vel.y = BALL_SPEED - new_ball.vel.x
            playing.balls.add(new_ball)
            playing.all_sprites.add(new_ball)


class Brick(pg.sprite.DirtySprite):

    def __init__(self, game, x, y, image_number):
        super().__init__()
        self.game = game
        sprite = self.game.brick_sheet.image_at(image_number, (0,0,0))
        self.image = pg.transform.scale(sprite, (BRICK_WIDTH, BRICK_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.breakable = True if image_number != 26 else False


class Paddle(pg.sprite.DirtySprite):
    # TODO sprite should only be dirty if it has moved since prev frame
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.set_sprite(14)
        self.rect = self.image.get_rect(center=(x, y))
        # TODO this should be moved to BrickBreaker
        self.lives = 3

    def set_sprite(self, image_number):
        sprite = self.game.paddle_sheet.image_at(image_number, (0,0,0))
        self.image = pg.transform.scale(sprite, (PADDLE_WIDTH, PADDLE_HEIGHT))

    def update(self):
        self.dirty = 1
        mouse_x = pg.mouse.get_pos()[0]
        self.rect.x = mouse_x

        # Keep player on screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Ball(pg.sprite.DirtySprite):

    def __init__(self, assets, game):
        super().__init__()
        self.assets = assets # this is the Game object
        self.game = game
        self.set_sprite(4)
        self.rect = self.image.get_rect()
        self.pos = pg.math.Vector2(self.game.player.rect.midtop)
        self.reset_speed()
        # TODO should be moved to BrickBreaker
        self.serving = True

    def set_sprite(self, image_number):
        sprite = self.assets.ball_sheet.image_at(image_number, (0,0,0))
        self.image = pg.transform.scale(sprite, (BALL_WIDTH, BALL_HEIGHT))

    def reset_speed(self):
        self.vel = pg.math.Vector2(0, -BALL_SPEED)

    def update(self):
        self.prev = self.rect.copy()

        # Bounce ball off edge of screen
        if self.rect.top < HUD_SIZE:
            self.rect.top = HUD_SIZE
            self.vel.y = -self.vel.y
            self.assets.sfx['wall_sound'].play()
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel.x = -self.vel.x
            self.assets.sfx['wall_sound'].play()
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vel.x = -self.vel.x
            self.assets.sfx['wall_sound'].play()

        # Update position
        if self.serving:
            self.pos.update(self.game.player.rect.midtop)
            self.pos.y -= BALL_HEIGHT / 2
        else:
            self.pos += self.vel
        self.rect.center = self.pos
        if self.pos != self.prev:
            self.dirty = 1


class Text(pg.sprite.DirtySprite):
    
    # TODO pass in an existing font
    def __init__(self, game, text, size, x, y):
        super().__init__()
        self.font = pg.font.Font(path.join(game.font_dir, 'Gameplay.ttf'), size)
        self.pos = (x, y)
        self.update_message(text)
        self.rect = self.image.get_rect(center=self.pos)
        self.dirty = 1

    def update_message(self, message):
        self.image = self.font.render(message, True, (255,255,255))
        self.dirty = 1
