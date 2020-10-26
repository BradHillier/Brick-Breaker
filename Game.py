import pygame
import sys
from BrickBreaker import *
from sprites import *
from settings import *
from menu import *
from time import sleep

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

class Game:
    """
    State machine for handling overall game state
    """
    def __init__(self):
        pygame.init()
        self.running = True
        # Set up the window
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font_name = pygame.font.match_font('arial')
        self.possible_states = {
            'playing': BrickBreaker(self),
        }
        self.state = self.possible_states['playing']

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.state.update()
            self.state.events()
            self.state.draw()

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


def main():
    game = Game()
    game.run()
    pygame.quit()

if __name__ == '__main__':
    main()
