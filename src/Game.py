import pygame as pg
import sys
from BrickBreaker import *
from Spritesheet import *
from sprites import *
from settings import *
from menu import *
from time import sleep
from os import path


class Game:

    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.toggle_fullscreen()

        self.dir = path.dirname(path.abspath(__file__)) + "/../"
        self.sound_dir = path.join(self.dir, 'assets/sound')
        self.font_dir = path.join(self.dir, 'assets/fonts')
        self.sprite_sheet_dir = path.join(self.dir, 'assets/spritesheet')
        pg.mixer.init()
        pg.mixer.music.set_volume(0.5)
        self.load_assets()

        self.possible_states = {
            'playing': BrickBreaker(self),
            'main_menu': MainMenu(self, WIDTH, HEIGHT, WIDTH/2, HEIGHT/2),
            'pause': PauseMenu(self, 500, 400, WIDTH/2, HEIGHT/2),
            'options_menu': OptionsMenu(self, 500, 400, WIDTH/2, HEIGHT/2)
        }
        self.state = None
        self.change_state('main_menu')
        self.running = True

    def load_assets(self):

        # Spritesheets
        self.brick_sheet = Sheet(path.join(self.sprite_sheet_dir, 'bricks'))
        self.paddle_sheet = Sheet(path.join(self.sprite_sheet_dir, 'paddles'))
        self.ball_sheet = Sheet(path.join(self.sprite_sheet_dir, 'balls'))
        self.powerup_sheet = Sheet(path.join(self.sprite_sheet_dir, 'powerups'))

        # Sounds
        load_sound = lambda x: pg.mixer.Sound(path.join(self.sound_dir, x))
        load_font = lambda x, s: pg.font.Font(path.join(self.font_dir, x), s)
        load_image = lambda x: pg.image.load(path.join(self.dir, x)).convert()
        try:
            self.sfx = {
                'brick_sound': load_sound("brick.wav"),
                'paddle_sound': load_sound("pop1.ogg"),
                'wall_sound': load_sound("pop2.ogg"),
                'menu_hover': load_sound("vgmenuhighlight.ogg"),
                'menu_select': load_sound("vgmenuselect.ogg"),
                'pause_sound': load_sound("pause2.wav"),
                'unpause_sound': load_sound("unpause.wav"),
                'gameover_sound': load_sound("GameOver.ogg")
            }
        except:
            # TODO: run each file individually through the try catch
            # would be good to have some way of showing error messages to the
            # player
            print('Unable to load audio file')

        # Fonts
        self.title_font = load_font('Retronoid.ttf', 160)
        self.button_font = load_font('Gameplay.ttf', 18)

        # Background Images
        self.bg = load_image("assets/images/background.png")
        self.menu_bg = load_image("assets/images/menu.png")
        self.space_bg = load_image("assets/images/space.png")
        self.bg = pg.transform.scale(self.bg, (WIDTH, HEIGHT))

    def run(self):
        """
        Game Loop
        """
        while self.running:
            self.clock.tick(FPS)
            self.state.events()
            self.state.update()
            self.state.draw(self.screen)

    def change_state(self, state=None, prev=False):
        if prev == True:
            temp = self.state
            self.state = self.prev_state
            self.prev_state = temp
        else:
            self.prev_state = self.state
            self.state = self.possible_states[state]
        self.state.new()

    # TODO: find out why this function is here and not somewhere else?
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    self.playing = False
                if event.type == pg.KEYUP:
                    waiting = False

    # TODO A modified version of this should go in utility.py
    # it should return Tuple(text_surf, text_rect)
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(path.join(self.font_dir, 'Gameplay.ttf'), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


