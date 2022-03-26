import pygame as pg
from settings import *


class HUD:
    # iterate through a sprite group of text objects
    # printnn
    # pass an image into __init__ for background
    def __init__(self, game):
        self.game = game
        self.state = 'uninitialized'
        # Surface and rect for the background
        self.surf = pg.Surface((WIDTH, 64)) # TODO this should be in settings
        self.rect = self.surf.get_rect(topleft=(0,0))
        self.all_sprites = pg.sprite.LayeredDirty()
        self.score = Text('Score: 0000', game.button_font, 10, 10)
        self.all_sprites.add(self.score)

    def new(self):
        # draw background - blit and update rect
        self.surf.fill((0,0,0)) # TODO this should be a variable
        self.game.screen.blit(self.surf, self.rect)
        pg.display.update(self.rect)
        
        # dynamically generated text

    def update(self):
        bb = self.game.possible_states['playing']
        if self.score.value != bb.score:
            self.score.update_message(f'Score: {bb.score:04d}')
        self.all_sprites.update()

    def draw(self, surface):
        if self.state == 'uninitialized':
            self.state = 'initialized'
            self.new()
        for sprite in self.all_sprites:
            if sprite.dirty == 1:
                sprite.dirty = 0
                surface.blit(self.score.image, self.score.rect)
                pg.display.update(self.score.rect)


class Text(pg.sprite.DirtySprite):
    def __init__(self, message, font, x, y):
        super().__init__()
        self.font = font
        self.value = 0 # TEMP
        self.update_message(message)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update_message(self, message):
        self.image = self.font.render(message, True, (255, 255, 255), (0,0,0))
        self.dirty = 1

    def update(self):
        pass


