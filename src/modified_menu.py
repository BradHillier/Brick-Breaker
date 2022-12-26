import pygame as pg
from settings import *
from os import path


class Button:
    """
    Simple button that swaps background and foreground 
    color when moused over
    """
    # TODO 
    # remove game, this class should be autonomous 
    # currently used for - font, sound, global colors
    def __init__(self, game, text, x, y, w=200, h=50):
        self.game = game
        self.state = 'default'
        # Background 
        self.image = pg.Surface((w, h))
        self.image.fill(TEXT_BG)
        self.rect = self.image.get_rect(center=(x,y))
        # Text
        self.font = self.game.button_font
        self.text = text
        self.set_text_color(TEXT_FG)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center

    def update(self):
        if self.mouse_over():
            # Invert Buton colors on mouse hover
            if self.state != 'mouse_over':
                self.state = 'mouse_over'
                # TODO Remove sound this doesn't belong here
                self.game.menu_hover.play()
                self.set_text_color(TEXT_BG)
                self.image.fill(TEXT_FG)
        elif self.state != 'default':
            self.state = 'default'
            self.set_text_color(TEXT_FG)
            self.image.fill(TEXT_BG)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def mouse_over(self):
        mouse_position = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            return True

    def set_text_color(self, color):
        self.text_surface = self.font.render(self.text, True, color)

class Knob:

    def __init__(self, parent, track_rect):
        super().__init__()
        self.parent = parent
        self.track_rect = track_rect
        self.image = pg.Surface((self.track_rect.width/20, 50))
        self.image.fill(TEXT_FG)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.prev = self.rect.copy()

    def update(self):
        if self.prev.center != self.rect.center:
            self.parent.game.clear_image(self.image, self.prev, self.parent.surf)
        self.prev = self.rect.copy()

    def draw(self):
        self.image.fill(TEXT_FG)
        self.parent.game.screen.blit(self.image, self.rect)



class Slider:
    # TODO 
    # remove game param, only used for fonn
    # add value as a parameter 
    def __init__(self, game, label, x, y, w, h):
        self.game = game
        self.state = 'default'
        self.value = 50
        self.padding = 200
        self.font = game.button_font
        self.surf = pg.Surface((w, h))
        self.surf.fill((0,0,0))
        self._root = self.surf.get_rect(topleft = (x, y))
        # label
        self.label = label
        self.text_surf = self.font.render(self.label, True, TEXT_FG)
        self.text_rect = self.text_surf.get_rect(x=x, y=y)
        self.text_rect.centery = self._root.centery
        # Track
        self.track_surf = pg.Surface((w - self.padding, h/4))
        self.track_surf.fill(TEXT_FG)
        self.track_rect = self.track_surf.get_rect()
        self.track_rect.x = x + self.padding
        self.track_rect.centery = self._root.centery
        # Knob
        self.knob = Knob(self, self.track_rect)

    def update(self):
        # Mouse interaction
        self.knob.update()
        mouse_position = pg.mouse.get_pos()
        left_mouse, middle_mouse, right_mouse = pg.mouse.get_pressed()
        if self._root.collidepoint(mouse_position) and left_mouse == True:
            self.state = 'selected'
            self.knob.rect.x = mouse_position[0]
            self.knob.draw()
        elif self.state == 'selected' and left_mouse == True:
            self.knob.rect.x = mouse_position[0]
        else:
            self.state = 'default'

        # Keep Knob inside of track
        if self.knob.rect.x > self.track_rect.right:
            self.knob.rect.x = self.track_rect.right
        if self.knob.rect.x < self.track_rect.left:
            self.knob.rect.x = self.track_rect.left
        self.value = (self.knob.rect.x - self.track_rect.left) / self.track_rect.width

    def draw(self, surface):
        surface.blit(self.text_surf, self.text_rect)
        surface.blit(self.track_surf, self.track_rect)


class Menu:
    def __init__(self, game):
        self.game = game
        self.buttons = []



class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        # TODO SHOULD NOT LOAD BG HERE
        self.bg = pg.image.load("assets/space.png")
        self.starty = HEIGHT*2/3
        # Title
        self.title_surface = self.game.title_font.render(
            'Brick Breaker', True, TEXT_FG)
        self.title_rect = self.title_surface.get_rect()
        self.title_rect.center = (WIDTH/2, HEIGHT/3)
        # Buttons
        self.buttons = []
        self.play = Button(game, 'Play', WIDTH/2, self.starty)
        self.options = Button(game, 'Options', WIDTH/2, self.starty+BUTTON_HEIGHT)
        self.quit = Button(game, 'Quit', WIDTH/2, self.starty + 2*BUTTON_HEIGHT)
        self.buttons.append(self.play)
        self.buttons.append(self.options)
        self.buttons.append(self.quit)

    def __eq__(self, other):
        if 'main_menu' == other: return True

    def new(self):
        pg.mouse.set_visible(True)
        if self.game.prev_state == 'playing' or self.game.prev_state == None:
            pg.mixer.music.load(path.join(self.game.sound_dir, "Blind Shift.ogg"))
            pg.mixer.music.play(loops=-1, start=23)

    def update(self):
        for button in self.buttons: button.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.QUIT()
            # Button Events
            if event.type == pg.MOUSEBUTTONDOWN and event.button ==1:
                if self.play.mouse_over():
                    self.game.menu_select.play()
                    self.game.change_state('playing')
                if self.options.mouse_over():
                    self.game.change_state('options_menu')
                if self.quit.mouse_over():
                    self.game.running = False

    def draw(self):
        self.game.screen.blit(self.bg, (0,0))
        self.game.screen.blit(self.title_surface, self.title_rect)
        for button in self.buttons: button.draw(self.game.screen)
        pg.display.flip()


class PauseMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.starty = HEIGHT/2
        self.resume = Button(game, 'Continue', WIDTH/2, self.starty)
        self.options = Button(
            game, 'Options', WIDTH/2,self.starty + BUTTON_HEIGHT)
        self.main_menu = Button(
            game, 'Main Menu', WIDTH/2, self.starty + 2*BUTTON_HEIGHT)
        self.buttons.append(self.resume)
        self.buttons.append(self.options)
        self.buttons.append(self.main_menu)
        self._create_surface()

    def __eq__(self, other):
        if other == 'pause': return True

    def _create_surface(self):
        padding = 50
        self.surf = pg.Surface((
            BUTTON_WIDTH + padding * 2, 
            BUTTON_HEIGHT * len(self.buttons) + padding * 2)
        )
        self.rect = self.surf.get_rect(topleft = (
            WIDTH / 2 - padding - BUTTON_WIDTH / 2, 
            self.starty - padding - BUTTON_HEIGHT / 2,))
        self.game.screen.blit(self.surf, self.rect)

    def new(self):
        pg.mouse.set_visible(True)
        self.surf.fill((0,0,0))
        self.game.screen.blit(self.surf, self.rect)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.QUIT()

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.resume.mouse_over():
                    self.game.menu_select.play()
                    pg.mixer.music.unpause()
                    self.game.clear_image(self.surf, self.rect)
                    self.game.change_state('playing')
                if self.options.mouse_over():
                    self.game.menu_select.play()
                    self.game.change_state('options_menu')
                if self.main_menu.mouse_over():
                    self.game.menu_select.play()
                    self.game.possible_states['playing'].playing = False
                    self.game.change_state('main_menu')

    def update(self):
        for button in self.buttons: button.update()

    def draw(self):
        # Buttons
        for button in self.buttons: button.draw(self.game.screen)
        pg.display.flip()


class OptionsMenu(Menu):

    def __init__(self, game):
        super().__init__(game)
        self.buttons = []
        self.bg = self.game.space_bg
        self.volume = Slider(game, 'Volume', WIDTH/2-200, HEIGHT/2, 400, 20)
        self.back = Button(game, 'Back', WIDTH/2, HEIGHT*2/3)
        self.buttons.append(self.back)
        self.buttons.append(self.volume)
        self._create_surface()

    def __eq__(self, other):
        if other == 'options_menu': return True

    def _create_surface(self):
        padding = 50
        self.surf = pg.Surface((500, 400))
        self.rect = self.surf.get_rect(topleft=(
            WIDTH / 2 - 250, HEIGHT/4))

    def new(self):
        self.surf.fill((0,0,0))
        self.game.screen.blit(self.surf, self.rect)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.QUIT()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.back.mouse_over():
                    self.game.menu_select.play()
                    self.game.clear_image(self.surf, self.rect, self.game.bg)
                    self.game.change_state(prev=True)

    def update(self):
        for button in self.buttons: button.update()
        pg.mixer.music.set_volume(self.volume.value)

    def draw(self):
        for button in self.buttons: button.draw(self.game.screen)
