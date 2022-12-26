from math import floor
import pygame as pg

# TODO wtf are all the hardcoded numbers in here supposed to mean

pg.init()

# Screen
WIDTH, HEIGHT = pg.display.Info().current_w, pg.display.Info().current_h
HUD_SIZE = 64 # TODO maybe make this proportional to the screen size?
FPS = 120
TEXT_FG = (255,255,255)
TEXT_BG = (0, 0, 0)

# Ball
# TODO v I literally have no idea how I came up with this formula
BALL_SPEED =  (800/FPS) * WIDTH/1280 # scales ball speed with screen width
BALL_WIDTH = floor(WIDTH/80)
BALL_HEIGHT = floor(WIDTH/80)

# Buttons
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Bricks
BRICK_WIDTH = floor(WIDTH/20)
BRICK_HEIGHT = floor(HEIGHT/25)

# Paddle
PADDLE_WIDTH = floor(WIDTH/10)
PADDLE_HEIGHT = floor(HEIGHT/20)
