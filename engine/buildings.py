import pygame

def scale2x(im):
  return pygame.transform.scale(im, (im.get_width()*2, im.get_height()*2))

SHIP =scale2x(pygame.image.load("assets/buildings/ship.png").convert_alpha())
HOUSE0000 = scale2x(pygame.image.load("assets/buildings/fossilhouse.png").convert_alpha())
HOUSE0450 = scale2x(pygame.image.load("assets/buildings/almostfossilhouse.png").convert_alpha())
HOUSE0793 = scale2x(pygame.image.load("assets/buildings/lessfossilhouse.png").convert_alpha())
HOUSE1066 = scale2x(pygame.image.load("assets/buildings/notveryfossilhouse.png").convert_alpha())
HOUSE1485 = scale2x(pygame.image.load("assets/buildings/oldhouse.png").convert_alpha())
HOUSE1603 = scale2x(pygame.image.load("assets/buildings/lessoldhouse.png").convert_alpha())
HOUSE1837 = scale2x(pygame.image.load("assets/buildings/slightlylessoldhouse.png").convert_alpha())
HOUSE1902 = scale2x(pygame.image.load("assets/buildings/house.png").convert_alpha())
DESK = pygame.image.load("assets/buildings/desk.png").convert_alpha()
BILLBOARD = pygame.image.load("assets/buildings/billboard.png").convert_alpha()