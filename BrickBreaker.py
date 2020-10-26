import pygame
import sys
from sprites import *
from settings import *
from menu import *
from time import sleep

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

class BrickBreaker:
    def __init__(self, game):
        self.game = game

    def new(self):
        self.score = 0
        self.level = 1
        # Initialize player
        self.all_sprites = pygame.sprite.Group()
        self.player = Paddle(self,
            width = BRICK_WIDTH,
            height = HEIGHT/25, 
            x = WIDTH/2, 
            y = HEIGHT * .95
        )
        self.all_sprites.add(self.player)
        self.ball = Ball(self)
        self.all_sprites.add(self.ball)

        self.bricks = pygame.sprite.Group()
        self.generate_bricks()
        self.animate_bricks()
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.draw()

    def generate_bricks(self):
        for i in range(ROWS):
            for j in range(COLUMNS):
                self.bricks.add(Brick(
                    width = BRICK_WIDTH - BRICK_PADDING / 2,
                    height = BRICK_HEIGHT - BRICK_PADDING / 2, 
                    # Haif of brick padding in x centers bricks on screen
                    x = PADDING + BRICK_PADDING / 2 + j * BRICK_WIDTH ,
                    y = HUD_SIZE + PADDING + i * BRICK_HEIGHT,
                    color = (i) % len(BRICK_COLORS)
                ))

    def animate_bricks(self):
        self.screen.fill(BG_COLOR)
        for brick in self.bricks:
            self.clock.tick(30)
            self.screen.blit(brick.surface, brick.rect)
            pygame.display.flip()

    def update(self):

        # Check for collisions
        if self.ball.rect.colliderect(self.player.rect):
            if self.ball.rect.bottom > self.player.rect.top:
                self.ball.rect.bottom = self.player.rect.top
            self.ball.dy = -self.ball.dy
        hits = pygame.sprite.spritecollide(self.ball, self.bricks, True)
        if hits:
            for brick in hits: 
                brick.kill()
                self.score += 1
            self.ball.dy = -self.ball.dy
        # Ball Goes off screen
        if self.ball.rect.top > HEIGHT:
            self.player.lives -= 1
            self.ball.serving = True
            if self.player.lives == 0:
                self.playing = False
        # Level Complete
        if len(self.bricks) == 0:
            self.ball.serving = True
            self.player.rect.center = (WIDTH/2, HEIGHT * .95)
            self.generate_bricks()
            self.level += 1
            self.animate_bricks()

        self.all_sprites.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.ball.serving == True:
                        self.ball.serving = False
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.playing = False

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.player.surface, self.player.rect)
        self.screen.blit(self.ball.surface, self.ball.rect)
        lives_text = 'Lives: {}'.format(self.player.lives)
        self.draw_text(lives_text, 28, (255, 255, 255), WIDTH / 4, HUD_SIZE / 2)
        score_text = 'Score: {}'.format(self.score)
        self.draw_text(score_text, 28, (255, 255, 255), WIDTH / 2, HUD_SIZE / 2)
        level_text = 'Level: {}'.format(self.level)
        self.draw_text(level_text, 28, (255, 255, 255), WIDTH * 3/4, HUD_SIZE / 2)
        for brick in self.bricks:
            self.screen.blit(brick.surface, brick.rect)
        pygame.display.flip()

    def show_gameover(self):
        self.screen.fill(BG_COLOR)
        self.draw_text('GAME OVER', 86, (255, 255, 255), WIDTH / 2, HEIGHT / 3)
        pygame.display.flip()
        sleep(1)
        self.wait_for_key()

    def show_title(self):
        self.screen.fill(BG_COLOR)
        self.draw_text('Brick Breaker', 64, (255, 255, 255), WIDTH / 2, HEIGHT / 3)
        self.draw_text('Press any key to play!', 28, (255, 255, 255), WIDTH / 2, HEIGHT/ 2)
        pygame.display.flip()
        sleep(0.5)
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                if event.type == pygame.KEYUP:
                    waiting = False
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


