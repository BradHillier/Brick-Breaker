import pygame as pg
import sys
import math
import random
import utility as util
import csv
import time
from hud import *

from os import path
from sprites import *
from settings import *
from menu import *



# TODO: Maybe make brickbreaker inherit from game, that kind of makes more
# sense to me
class BrickBreaker:
    def __init__(self, game):
        self.game = game
        self.bg = game.bg
        self.playing = False

    def new(self):
        if type(self.game.prev_state) != PauseMenu:
            self.playing = True
            self.score = 0
            self.level = 0
            pg.mixer.music.load(path.join(self.game.sound_dir,
                                          'Afterburner.ogg'))
            pg.mixer.music.play(loops=-1)
            # Initialize Sprites
            self.all_sprites = pg.sprite.LayeredDirty()
            self.all_bricks = pg.sprite.LayeredDirty()
            self.powerups = pg.sprite.LayeredDirty()
            self.balls = pg.sprite.LayeredDirty()
            self.breakable_bricks = pg.sprite.LayeredDirty()
            self.player = Paddle(self.game, WIDTH/2, HEIGHT-BRICK_HEIGHT)
            # Text sprites
            self.level_text = Text(self.game, f'level {self.level}', 48,
                                   WIDTH/2,HEIGHT*5/8)
            self.all_sprites.add(self.level_text)
            self.hud = HUD(self.game)
            # TODO Ball shouldn't need both Game and BrickBreaker
            # this would be fixed by making brick breaker inherit from game
            self.ball = Ball(self.game, self)
            self.balls.add(self.ball)
            self.all_sprites.add(self.ball, self.player)
            self.all_sprites.clear(self.game.screen, self.game.bg)
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
                            j * BRICK_WIDTH,  
                            i * BRICK_HEIGHT,
                            int(image_number))
                        if int(image_number) != 26:
                            self.breakable_bricks.add(brick)
                        self.all_bricks.add(brick)
                        self.all_sprites.add(brick)
                        self.all_sprites.move_to_back(brick)
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

        # Ball collides with Player
        ball_collisions = pg.sprite.spritecollide(self.player, self.balls,
                                                  False)
        if ball_collisions:
            for ball in ball_collisions:
                self.game.sfx['paddle_sound'].play()
                ball.rect.bottom = self.player.rect.top
                ball.vel = util.controlled_deflect(ball, self.player)

        # Player collides with power up
        powerup_collisions = pg.sprite.spritecollide(self.player,
                                                     self.powerups, False)
        if powerup_collisions:
            self.game.sfx['menu_hover'].play()
            for powerup in powerup_collisions:
                powerup.action(self.balls.sprites()[0].rect.center)
                powerup.kill()

        # Power up off screen
        for powerup in self.powerups:
            if powerup.rect.top > HEIGHT:
                powerup.kill()

        # Ball collides with Bricks
        for ball in self.balls:
            hits = pg.sprite.spritecollide(ball, self.all_bricks, False)
            if hits:
                self.game.sfx['brick_sound'].play()
                for brick in hits: 
                    if brick in self.breakable_bricks:
                        self.score += 1
                        brick.kill()
                        # TODO: the chance a brick is a power up should
                        # go in settings and atleast be a variable
                        if random.randint(0, 5) == 0:
                            powerup = PowerUp(self.game, brick.rect.center)
                            self.all_sprites.add(powerup)
                            self.powerups.add(powerup)
                collision_side = util.collision_helper_AABB(hits[0], ball)
                if collision_side == 'left' or collision_side == 'right':
                    ball.vel.x = -ball.vel.x
                elif collision_side == 'top' or collision_side == 'bottom':
                    ball.vel.y = -ball.vel.y
                elif collision_side == 'corner':
                    ball.vel.y = -ball.vel.y
                    ball.vel.x = -ball.vel.x

            # Ball Goes off screen
            if ball.rect.top > HEIGHT:
                if len(self.balls) == 1:
                    self.player.lives -= 1
                    ball.serving = True
                    ball.reset_speed()
                else:
                    ball.kill()


        # This is ran before level complete check as new bricks
        # are only flagged to render one time: when they are created
        # TODO BUG - bricks will get destroyed if ball is over top when they
        # are rendered, ball needs to be updated before bricks rendered
        self.all_sprites.update()
        self.hud.update()

        # Level Complete
        if len(self.breakable_bricks) == 0:
            # Clear all unbreakable bricks
            for brick in self.all_bricks:
                brick.kill()
            self.ball.serving = True
            self.player.rect.center = (WIDTH/2, HEIGHT * .95)
            self.level += 1
            self.load_level()
            self.level_displayed = False
            self.level_text.kill()
            self.level_text = Text(self.game, f'level {self.level}', 48,
                                   WIDTH/2,HEIGHT*5/8)
            self.all_sprites.add(self.level_text)
            self.all_sprites.move_to_front(self.level_text)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.change_state('pause')
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button  == 1:
                    for ball in self.balls:
                        if ball.serving == True:
                            ball.serving = False

    def draw(self, surface):

        rects = self.all_sprites.draw(surface)
        
        # Text showing current level displayed at the start of each level
        if self.level_displayed == False:
            self.level_displayed = pg.time.get_ticks()
        elif pg.time.get_ticks() - self.level_displayed > 2000:
            self.level_text.kill()
        pg.display.update(rects)
        self.hud.draw(surface)

    def show_gameover(self):
        pg.mixer.music.stop()
        self.game.sfx['gameover_sound'].play()
        self.game.draw_text('GAME OVER', 86, (255, 255, 255), WIDTH/2, HEIGHT/2)
        pg.display.flip()
        pg.time.wait(500)
        self.game.wait_for_key()
        self.game.change_state('main_menu')
