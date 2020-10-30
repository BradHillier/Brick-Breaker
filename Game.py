import pygame
import sys
from BrickBreaker import *
from Spritesheet import *
from sprites import *
from settings import *
from menu import *
from time import sleep
from os import path

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT
)

class Game:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.dir = path.dirname(path.abspath(__file__))
        self.sound_dir = path.join(self.dir, 'assets/sound')
        self.font_dir = path.join(self.dir, 'assets/fonts')
        pygame.mixer.init()
        pg.mixer.music.set_volume(0.5)
        self.load_assets()

        self.possible_states = {
            'playing': BrickBreaker(self),
            'main_menu': MainMenu(self),
            'pause': PauseMenu(self)
        }
        self.change_state('main_menu')
        self.running = True

    def load_assets(self):

        # Spritesheets
        self.brick_sheet = Sheet(path.join(self.dir, 'assets/bricks'))
        self.paddle_sheet = Sheet(path.join(self.dir, 'assets/paddles'))
        self.ball_sheet = Sheet(path.join(self.dir, 'assets/balls'))

        # Sounds
        load_sound = lambda x: pg.mixer.Sound(path.join(self.sound_dir, x))
        try:
            self.brick_sound = load_sound("brick.wav")
            self.paddle_sound = load_sound("paddle.wav")
            self.menu_hover = load_sound("vgmenuhighlight.ogg")
            self.menu_select = load_sound("vgmenuselect.ogg")
            self.pause_sound = load_sound("pause2.wav")
            self.unpause_sound = load_sound("unpause.wav")
            self.gameover_sound = load_sound("GameOver.ogg")
        except:
            print('Unable to load audio file')
            raise SystemExit

        # Fonts
        self.title_font = pg.font.Font(path.join(self.font_dir,
                                                 'Retronoid.ttf'), 160)
        self.button_font = pg.font.Font(path.join(self.font_dir,
                                                 'Gameplay.ttf'), 18)
        # Background Images
        self.bg = pg.image.load(path.join(self.dir, "assets/background.png"))
        self.bg = pg.transform.scale(self.bg, (WIDTH, HEIGHT))

    def run(self):
        """
        Game Loop
        """
        while self.running:
            self.clock.tick(FPS)
            self.state.events()
            self.state.update()
            self.state.draw()

    def change_state(self, state):
        self.state = self.possible_states[state]
        self.state.new()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    self.playing = False
                if event.type == KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(path.join(self.font_dir, 'Gameplay.ttf'), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


