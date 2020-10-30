import pygame as pg
import sys
import math
import utility as util
import csv
import time

from os import path
from sprites import *
from settings import *
from menu import *



class BrickBreaker:
    def __init__(self, game):
        self.game = game
        self.bg = game.bg
        self.playing = False

    def new(self):
        if self.playing:
            pg.mixer.music.unpause()
        else:
            self.playing = True
            self.score = 0
            self.level = 5
            pg.mixer.music.load(path.join(self.game.sound_dir,
                                          'Afterburner.ogg'))
            pg.mixer.music.play(loops=-1)
            # Initialize Sprites
            self.all_sprites = pg.sprite.Group()
            self.bricks = pg.sprite.Group()
            self.player = Paddle(self.game, WIDTH/2, HEIGHT-BRICK_HEIGHT)
            # TODO Ball shouldn't need both Game and BrickBreaker
            self.ball = Ball(self.game, self)
            self.all_sprites.add(self.ball, self.player)
            self.load_level()

    def load_level(self):
        """
        Generate bricks from a tilemap
        """
        level_location = path.join(self.game.dir,
                                   'levels/level_{}.csv'.format(self.level))
        with open(level_location) as file:
            level = csv.reader(file)
            for i, row in enumerate(level):
                for j, image_number in enumerate(row):
                    if int(image_number) != -1:
                        brick = Brick(self.game, 
                            j * 64,  
                            i * 32,
                            int(image_number))
                        self.bricks.add(brick)
                        self.all_sprites.add(brick)
                        # Helps display level text for set period of time
                        self.level_displayed = False

    def update(self):
        pg.mouse.set_visible(False)
        if self.playing == False:
            pg.mixer.music.play(loops=-1)
            self.new()

        # Check if gameover
        if self.player.lives == 0:
            self.playing = False
            self.show_gameover()

        # Player Collision
        if self.ball.rect.colliderect(self.player.rect):
            self.game.paddle_sound.play()
            self.ball.rect.bottom = self.player.rect.top
            self.ball.vel = util.controlled_deflect(self.ball, self.player)

        #Ball collides with Bricks
        hits = pg.sprite.spritecollide(self.ball, self.bricks, False)
        if hits:
            self.game.brick_sound.play()
            for brick in hits: 
                self.score += 1
                brick.kill()
            collision_side = util.collision_helper_AABB(hits[0], self.ball)
            if collision_side == 'left' or collision_side == 'right':
                self.ball.vel.x = -self.ball.vel.x
            elif collision_side == 'top' or collision_side == 'bottom':
                self.ball.vel.y = -self.ball.vel.y

        # Ball Goes off screen
        if self.ball.rect.top > HEIGHT:
            self.player.lives -= 1
            self.ball.serving = True

        # Level Complete
        if len(self.bricks) == 0:
            self.ball.serving = True
            self.player.rect.center = (WIDTH/2, HEIGHT * .95)
            self.level += 1
            self.load_level()
            self.show_level()

        self.all_sprites.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.mixer.music.pause()
                    self.game.pause_sound.play()
                    self.game.change_state('pause')
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button  == 1:
                    if self.ball.serving == True:
                        self.ball.serving = False

    def draw(self):
        self.game.screen.blit(self.bg, (0, 0))
        self.all_sprites.draw(self.game.screen)

        # Heads up display
        pg.draw.rect(self.game.screen, (0,0,0), (0, 0, WIDTH, HUD_SIZE))
        lives_text = 'Lives: {}'.format(self.player.lives)
        self.game.draw_text(
            lives_text, 20, (255, 255, 255), WIDTH / 4, HUD_SIZE / 2)
        score_text = 'Score: {}'.format(self.score)
        self.game.draw_text(
            score_text, 32, (255, 255, 255), WIDTH / 2, HUD_SIZE / 2)
        level_text = 'Level: {}'.format(self.level)
        self.game.draw_text(
            level_text, 20, (255, 255, 255), WIDTH * 3/4, HUD_SIZE / 2)

        # Text showing current level displayed at the start of each level
        if self.level_displayed == False:
            self.level_displayed = pg.time.get_ticks()
        elif pg.time.get_ticks() - self.level_displayed < 2000:
            self.show_level() 
        pg.display.flip()

    def show_level(self):
        text = 'Level {}'.format(self.level)
        self.game.draw_text(text, 64, (255, 255, 255), WIDTH/2, HEIGHT*5/8)
        pg.display.flip()

    def show_gameover(self):
        pg.mixer.music.stop()
        self.game.gameover_sound.play()
        self.game.draw_text('GAME OVER', 86, (255, 255, 255), WIDTH/2, HEIGHT/2)
        pg.display.flip()
        pg.time.wait(500)
        self.game.wait_for_key()
        self.game.change_state('main_menu')




