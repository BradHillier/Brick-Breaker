import pygame
from brick_breaker import *
from menu import *

def main():
    brick_breaker = Game()
    brick_breaker.show_title()
    while brick_breaker.running:
        brick_breaker.main_menu.run()
        brick_breaker.new()
        brick_breaker.show_gameover()
    pygame.QUIT()


if __name__ == '__main__':
    main()

