import pygame as pg
from settings import *
from os import path


class Button(pg.sprite.Sprite):
    def __init__(self, menu, text, x, y, function):
        super().__init__()
        self.menu = menu
        self.text = text
        self.x = x
        self.y = y
        self.font = self.menu.game.button_font
        self.function = function

    def update(self):

    def draw(self):
        bg_color = TEXT_FG if self == self.menu.selected else TEXT_BG
        text_color = TEXT_BG if self == self.menu.selected else TEXT_FG
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect()

        # Draw button centered at (x, y)
        pg.draw.rect(self.menu.game.screen, bg_color, 
                     (self.x - BUTTON_WIDTH/2, 
                      self.y - BUTTON_HEIGHT/2, 
                      BUTTON_WIDTH, 
                      BUTTON_HEIGHT))
        text_rect.center = (self.x, self.y)
        self.menu.game.screen.blit(text_surface, text_rect)

class Menu:
    def __init__(self, game):
        self.game = game
        self.all_sprites = pg.sprite.Group()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.QUIT()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.change_state('playing')
                if event.key == pg.K_RETURN:
                    self.selected.function()
                # Navigation
                if event.key == pg.K_s:
                    # TODO FIX THIS SPAGHETTI - move sound
                    self.game.menu_hover.play()
                    current_idx = self.buttons.index(self.selected)
                    self.selected = self.buttons[(current_idx + 1) %
                                                 len(self.buttons)]
                if event.key == pg.K_d:
                    self.game.menu_hover.play()
                    current_idx = self.buttons.index(self.selected)
                    self.selected = self.buttons[(current_idx - 1) %
            if event.type == pg.KEYDOWN:
                                                 len(self.buttons)]

    def update(self):
        pass


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.starty = HEIGHT*2/3
        self.bg = pg.image.load("assets/space.png")
        self.buttons.append(Button(
            self, 'Play', WIDTH/2, self.starty, self.play))
        self.buttons.append(Button(
            self, 'Quit', WIDTH/2, self.starty +BUTTON_HEIGHT, self.quit))
        for button in self.buttons:
            self.all_sprites.add(button)
        self.selected = self.buttons[0]

    def new(self):
        pg.mixer.music.load(path.join(self.game.sound_dir, "Blind Shift.ogg"))
        pg.mixer.music.play(loops=-1, start=23)

    def draw(self):
        self.game.screen.blit(self.bg, (0,0))
        # Draw title
        title_surface = self.game.title_font.render(
            'Brick Breaker', True, TEXT_FG)
        title_rect = title_surface.get_rect()
        title_rect.center = (WIDTH/2, HEIGHT/3)
        self.game.screen.blit(title_surface, title_rect)
        # Buttons
        for button in self.buttons:
            button.draw()
        pg.display.flip()


    def play(self):
        self.game.menu_select.play()
        self.game.change_state('playing')

    def quit(self):
        self.game.running = False


class PauseMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.starty = HEIGHT/2
        self.buttons.append(Button(
            self, 'Continue', WIDTH/2, self.starty, self.play))
        self.buttons.append(Button(
            self, 'Main Menu', WIDTH/2, self.starty + BUTTON_HEIGHT, self.main_menu))
        self.selected = self.buttons[0]

    def new(self):
        pass

    def draw(self):
        # Border around buttons
        padding = 50
        pg.draw.rect(self.game.screen, TEXT_BG, (
            WIDTH/2 - padding - BUTTON_WIDTH/2, 
            self.starty - padding - BUTTON_HEIGHT/2, 
            BUTTON_WIDTH + padding*2, 
            BUTTON_HEIGHT*len(self.buttons) + padding*2)
        )
        pg.draw.rect(self.game.screen, TEXT_FG, (
            WIDTH/2 - padding - BUTTON_WIDTH/2, 
            self.starty - padding - BUTTON_HEIGHT/2, 
            BUTTON_WIDTH + padding*2, 
            BUTTON_HEIGHT*len(self.buttons) + padding*2),
            5
        )
        # Buttons
        for button in self.buttons:
            button.draw()
        pg.display.flip()

    def play(self):
        self.game.menu_select.play()
        self.game.change_state('playing')

    def main_menu(self):
        self.game.menu_select.play()
        self.game.possible_states['playing'].playing = False
        self.game.change_state('main_menu')
