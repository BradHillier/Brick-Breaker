import pygame as pg
from settings import *
from os import path

# TODO Create pre built themes (dicts) that can be passed to menus 
# and compenents


class MenuBase:
    # TODO Properly handle different color backgrounds

    def __init__(self, game, w, h, x, y, **kwargs):
        self.args = {
            'padding': 100,
            'border': False,
            'bg': None
        }
        self.args.update(kwargs)
        self.game = game
        self._widgets = []
        # Background
        if isinstance(self.args['bg'], pg.Surface):
            self.args['bg'] = pg.transform.scale(self.args['bg'], (w, h))
            self.surf = self.args['bg'].copy()
        else:
            self.surf = pg.Surface((w, h))
        self.rect = self.surf.get_rect(center=(x, y))

    def add(self, widget):
        self._widgets.append(widget)

    def clear(self, image, sprites=None):
        for x in range(self.rect.left, self.rect.right):
            for y in range(self.rect.top, self.rect.bottom):
                bg_pixel = image.get_at((x, y))
                self.surf.set_at((x - self.rect.left, y - self.rect.y),
                                 bg_pixel)
        self.game.screen.blit(self.surf, self.rect)
        pg.display.update(self.rect)

        # Re-render sprites that were covered by the menu so they are visible
        if sprites is not None:
            dirty_sprites = pg.sprite.LayeredDirty()
            for sprite in sprites:
                if self.rect.colliderect(sprite.rect):
                    sprite.dirty = 1
                    dirty_sprites.add(sprite)
            dirty_rects = dirty_sprites.draw(self.game.screen)
            pg.display.update(dirty_rects)

    def new(self):
        pg.mouse.set_visible(True)

        # Initialize window
        if self.args['bg'] != None:
            self.surf = self.args['bg'].copy()
        else:
            self.surf.fill((0,0,0))
        self.game.screen.blit(self.surf, self.rect)
        pg.display.update(self.rect)

        # Position widgets
        for idx, widget in enumerate(self._widgets):
            widget.state = 'pre-rendered'
            widget.rect.centerx = self.rect.centerx
            widget.rect.centery = self.rect.top + self.args['padding']+ 100 * idx

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.QUIT()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for widget in self._widgets:
                    if type(widget) == Button:
                        if widget.mouse_over():
                            self.game.sfx['menu_select'].play()
                            widget.action()

    def update(self):
        for widget in self._widgets: widget.update()

    def draw(self, surface):
        for widget in self._widgets:
            if widget.dirty == 1:
                widget.draw(surface)
                pg.display.update(widget.rect)


class Button:
    """
    Button dynamically positioned by it's parent
    """
    def __init__(self, 
                 parent: MenuBase,
                 label: str, 
                 font: pg.font.Font,
                 action: callable, 
                 hover_sound: pg.mixer.Sound = None,
                 w: int = 200, 
                 h: int = 50,
                 fg: pg.Color = (255, 255, 255),
                 bg: pg.Color = (0,0,0)
                ):
        self.parent = parent
        self.action = action
        self.hover_sound = hover_sound
        # pre-rendered avoids setting dirty to 0 in first pass of update
        self.state = 'pre-rendered'
        self.dirty = 1
        # Colors
        self.fg = fg
        self.bg = bg
        # Background 
        self.image = pg.Surface((w, h))
        self.rect = self.image.get_rect()
        self.image.fill(bg)
        # Text
        self.label = label
        self.font = font
        self.set_text_color(fg)
        self.label_rect = self.label_surf.get_rect()

    def update(self):
        """
        Swap foreground and background colors if moused over
        """
        if self.mouse_over():
            if self.state != 'mouse_over':
                self.state = 'mouse_over'
                self.image.fill(self.fg)
                self.set_text_color(self.bg)
                self.dirty = 1
                if self.hover_sound != None:
                    self.hover_sound.play()
            else:
                self.dirty = 0
        elif self.state != 'default':
            self.state = 'default'
            self.image.fill(self.bg)
            self.set_text_color(self.fg)
            self.dirty = 1
        else:
            self.dirty = 0

    def draw(self, surface):
        """
        Should only be called if dirty is equal to 1
        """
        # Background
        surface.blit(self.image, self.rect)
        # Foreground
        self.label_rect.center = self.rect.center
        surface.blit(self.label_surf, self.label_rect)
        # Re-render area of the screen button exists in
        pg.display.update(self.rect)

    def mouse_over(self):
        mouse_position = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            return True

    def set_text_color(self, color):
        self.label_surf = self.font.render(self.label, True, color)


class Slider:
    """
    Slider dynamimally positioned by it's parent
    """
    def __init__(self, 
                 parent: MenuBase,
                 label: str, 
                 font: pg.font.Font,
                 value: float,
                 on_change: callable,
                 min: float = 0.0,
                 max: float = 1.0,
                 w: int = 400,
                 h: int = 50
                ):
        self.state = 'pre-rendered'
        self.value = value
        self.min = min
        self.max = max

        self.padding = 200
        self.surf = pg.Surface((w, h))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect()
        self.on_change = on_change # Tempeeeeee

        # label
        self.label = label
        self.font = font
        self.text_surf = self.font.render(self.label, True, TEXT_FG)
        self.text_rect = self.text_surf.get_rect()

        # Track
        self.track_surf = pg.Surface((self.rect.width - self.padding,
                                self.rect.height/20))
        self.track_surf.fill(TEXT_FG)
        self.track_rect = self.track_surf.get_rect()

        # Knob
        self.knob_surf = pg.Surface((self.track_rect.width/20, 20))
        self.knob_surf.fill(TEXT_FG)
        self.knob_rect = self.knob_surf.get_rect()

    def _convert_value_to_x_axis(self):
        return self.track_rect.width * self.value/self.max + self.track_rect.left

    def _move_knob(self, mouse_position):
        """
        Move Knob to current mouse position, flag for re-render if updated
        """
        knob_prev_pos = self.knob_rect.center
        self.knob_rect.x = mouse_position[0]
        if self.knob_rect.center != knob_prev_pos:
            self.dirty = 1
        else:
            self.dirty = 0

    def _position_components(self):
        """ 
        Position text, track and knob inside of self.rect
        """
        self.text_rect.left = self.rect.left
        self.text_rect.centery = self.rect.centery
        self.track_rect.x = self.rect.centerx
        self.track_rect.centery = self.rect.centery
        self.knob_rect.x = self._convert_value_to_x_axis()
        self.knob_rect.centery = self.rect.centery

    def update(self):
        mouse_position = pg.mouse.get_pos()
        left_mouse, middle_mouse, right_mouse = pg.mouse.get_pressed()

        # Initial render
        if self.state == 'pre-rendered':
            self.state = 'default'
            self._position_components()
            self.dirty = 1

        # Update knob position
        elif left_mouse == False:
            if self.state != 'default':
                self.state = 'default'
                self.dirty = 1
            else:
                self.dirty = 0
        elif self.rect.collidepoint(mouse_position):
            self.state = 'clicked'
            self._move_knob(mouse_position)
        elif self.state == 'clicked':
            self._move_knob(mouse_position)

        # Keep Knob inside of track_rect
        if self.knob_rect.right > self.track_rect.right:
            self.knob_rect.right = self.track_rect.right
        if self.knob_rect.x < self.track_rect.left:
            self.knob_rect.x = self.track_rect.left
        self.value = (self.knob_rect.x - self.track_rect.left) / self.track_rect.width
        self.on_change(self.value)

    def draw(self, surface):
        if self.dirty == 1:
            surface.blit(self.surf, self.rect)
            surface.blit(self.text_surf, self.text_rect)
            surface.blit(self.track_surf, self.track_rect)
            # Black border on left and right of knob
            pg.draw.rect(surface, (0,0,0), (
                self.knob_rect.x - 3,
                self.knob_rect.y,
                self.knob_rect.width + 6,
                self.knob_rect.height))
            surface.blit(self.knob_surf, self.knob_rect)
            pg.display.update(self.rect)


class OptionsMenu(MenuBase):
    def __init__(self, game, w, h, x, y):
        super().__init__(game, w, h, x, y, 
                         bg=game.menu_bg)
        self.add(Slider(self, 'Music', game.button_font,
                     pg.mixer.music.get_volume(), pg.mixer.music.set_volume))
        self.add(Slider(self, 'Sound FX', game.button_font,
                     0.5, self.sound_fx))
        self.add(Button(self, 'Back', game.button_font, self.back, 
                        hover_sound = game.sfx['menu_hover']))

    def new(self):
        super().new()

    def sound_fx(self, volume):
        for sound in self.game.sfx.values():
            sound.set_volume(volume)


    def back(self):
        self.game.change_state(prev=True)


class MainMenu(MenuBase):
    def __init__(self, game, w, h, x, y):
        super().__init__(game, w, h, x, y, 
                        padding=500,
                        bg=game.space_bg)
        self.add(Button(self, 'Play', game.button_font, self.play,
                        hover_sound = game.sfx['menu_hover']))
        self.add(Button(self, 'Options', game.button_font, self.options,
                        hover_sound = game.sfx['menu_hover']))
        self.add(Button(self, 'Quit', game.button_font, self.quit,
                        hover_sound = game.sfx['menu_hover']))

    def new(self):
        super().new()
        # Title
        title = self.game.title_font.render(
            'Brick Breaker', True, TEXT_FG)
        title_rect = title.get_rect()
        title_rect.center = (WIDTH/2, HEIGHT/3)
        self.game.screen.blit(title, title_rect)
        pg.display.update(title_rect)
        # Music
        if type(self.game.prev_state) != OptionsMenu:
            pg.mixer.music.load(path.join(self.game.sound_dir, 'Blind Shift.ogg'))
            pg.mixer.music.play(loops=-1, start=23)

    def play(self):
        self.game.change_state('playing')

    def options(self):
        self.game.change_state('options_menu')

    def quit(self):
        self.game.running = False


class PauseMenu(MenuBase):
    def __init__(self, game, w, h, x, y):
        super().__init__(game, w, h, x, y,
                        bg=game.menu_bg)
        self.add(Button(self, 'Resume', game.button_font, self.resume,
                        hover_sound = game.sfx['menu_hover']))
        self.add(Button(self, 'Options', game.button_font, self.options,
                        hover_sound = game.sfx['menu_hover']))
        self.add(Button(self, 'Main Menu', game.button_font, self.main_menu,
                        hover_sound = game.sfx['menu_hover']))

    def new(self):
        super().new()
        self.game.sfx['pause_sound'].play()
        pg.mixer.music.pause()

    def resume(self):
        self.clear(self.game.bg, self.game.possible_states['playing'].all_sprites)
        pg.mixer.music.unpause()
        self.game.change_state('playing')

    def options(self):
        self.game.change_state('options_menu')

    def main_menu(self):
        self.game.change_state('main_menu')
