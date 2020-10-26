import pygame
from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, menu, text, function):
        super().__init__()
        self.menu = menu
        self.text = text
        self.function = function


class Menu:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.buttons.append(Button(self, 'Play', self.play))
        self.buttons.append(Button(self, 'Quit', pygame.QUIT))
        self.selected = self.buttons[0]

    def run(self):
        self.viewing = True
        while self.viewing:
            self.game.clock.tick(FPS)
            self.update()
            self.events()
            self.draw()

    def update(self):
        pass

    def play(self):
        self.viewing = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                # Exit menu and start game
                if event.key == pygame.K_RETURN:
                    self.selected.function()
                if event.key == pygame.K_s:
                    current_idx = self.buttons.index(self.selected)
                    self.selected = self.buttons[(current_idx + 1) %
                                                 len(self.buttons)]
                if event.key == pygame.K_d:
                    current_idx = self.buttons.index(self.selected)
                    self.selected = self.buttons[(current_idx - 1) %
                                                 len(self.buttons)]


    def draw(self):
        self.game.screen.fill(BG_COLOR)
        for idx, item in enumerate(self.buttons):
            color = (255, 0, 0) if item == self.selected else TEXT_COLOR
            self.game.draw_text(item.text, 28, color, WIDTH / 2, HEIGHT/2 + 50* idx)

        pygame.display.flip()


