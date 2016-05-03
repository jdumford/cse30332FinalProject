import pygame
from pygame.locals import *
 
class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


"""if __name__ == '__main__':
    pygame.init()
    img_size = 33
    rows = 10
    columns = 10
    mx = 100
    my = 100
    screen = pygame.display.set_mode(((img_size+1)*columns, (img_size+1)*rows))

    watersheet = spritesheet("sprites/water.png")
    water = watersheet.image_at((50, 50, img_size, img_size))

    firesheet = spritesheet("sprites/fire.png")
    fire = firesheet.image_at((415, 20, img_size, img_size))

    misssheet = spritesheet("sprites/miss.png")
    miss = misssheet.image_at((455, 182, img_size, img_size))

    #boat = pygame.image.load("sprites/BattleShip.png").convert()
    boatsheet = spritesheet("sprites/battleships.png")
    battleship = boatsheet.image_at((93, 130, img_size, 100))
    battleship2 = boatsheet.image_at((249, 128, img_size, 66))

    #winsheet = spritesheet("sprites/win.png")
    win = pygame.image.load("sprites/win.png").convert()
    lose = pygame.image.load("sprites/lose.png").convert()

    while(1):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()

        screen.fill((0,0,0))
        for x in range(0, columns):
            for y in range(0, rows):
                screen.blit(water, ((img_size+1)*x, (img_size+1)*y))
        screen.blit(fire, (img_size+1, img_size+1))
        screen.blit(battleship, (mx, my))
        screen.blit(battleship2, (200, 200))
        screen.blit(miss, (100, 100))
        screen.blit(win, (20, 100))
        screen.blit(lose, (20, 200))

        pygame.display.flip()

"""
