# Screen
WIDTH = 1280
HEIGHT = 800
PADDING = 20
HUD_SIZE = 75
FPS = 30
BG_COLOR= (28, 28, 28)
TEXT_COLOR = (255,255,255)

# Bricks
ROWS = 6
COLUMNS = 9
BRICK_PADDING = 10
BRICK_WIDTH = (WIDTH - PADDING * 2) / COLUMNS
BRICK_HEIGHT = (HEIGHT / 2 - PADDING * 2 - HUD_SIZE) / ROWS
BRICK_COLORS = [
    (187, 1, 67),       # Red
    (253, 151, 31),     # Orange 
    (230, 219, 116),    # Yellow
    (169, 192, 63),     # Green 
    (102, 217, 239),    # Blue
    (174, 129, 255),    # Magenta 
]
