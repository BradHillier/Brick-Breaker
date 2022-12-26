import pygame
import math
import untangle


class Sheet(object):
    """ 
    Load sprites with the aid of a tsx file
    """
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename + '.png').convert()
            with open(filename + '.tsx') as f:
                self.meta = untangle.parse(filename + '.tsx').tileset
        except pygame.error:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit 

    def image_at(self, img_num, colorkey = None):
        """
        Load an image from it's associated tile map number
        """
        # Determine image position
        image_column = (img_num % int(self.meta['columns']))
        image_row = math.floor(img_num / int(self.meta['columns']))
        x = image_column * int(self.meta['tilewidth'])
        y = image_row * int(self.meta['tileheight'])

        # Load image from x, y, x+offset, y+offset
        rect = pygame.Rect(
            x, y, int(self.meta['tilewidth']), int(self.meta['tileheight']))
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey ==  -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
