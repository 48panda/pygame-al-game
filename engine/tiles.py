import pygame
grassunder = pygame.image.load("assets/tiles/grassunder.png")
grassdark = pygame.image.load("assets/tiles/grassdark.png")
grass = pygame.image.load("assets/tiles/grass.png")

LEAVES = pygame.image.load("assets/tiles/leaves.png")
TREE = pygame.image.load("assets/tiles/tree.png")
SHIP = pygame.image.load("assets/buildings/ship.png")
SHIP = pygame.transform.scale(SHIP, (SHIP.get_width()*2, SHIP.get_height()*2))
DIRT = pygame.image.load("assets/tiles/dirt.png")
GRASS = pygame.image.load("assets/tiles/dirt.png")
GRASS.blit(grassunder, (0,0))
GRASS.blit(grassdark, (0,0))
GRASS.blit(grass, (0,0))
GRASS_l = pygame.image.load("assets/tiles/dirt.png")
GRASS_l.blit(grassunder, (0,0))
GRASS_l.blit(pygame.transform.rotate(grassunder, 90), (0,0))
GRASS_l.blit(grassdark, (0,0))
GRASS_l.blit(pygame.transform.rotate(grassdark, 90), (0,0))
GRASS_l.blit(grass, (0,0))
GRASS_l.blit(pygame.transform.rotate(grass, 90), (0,0))
GRASS_r = pygame.image.load("assets/tiles/dirt.png")
GRASS_r.blit(grassunder, (0,0))
GRASS_r.blit(pygame.transform.rotate(grassunder, 270), (0,0))
GRASS_r.blit(grassdark, (0,0))
GRASS_r.blit(pygame.transform.rotate(grassdark, 270), (0,0))
GRASS_r.blit(grass, (0,0))
GRASS_r.blit(pygame.transform.rotate(grass, 270), (0,0))
GRASS_b = pygame.image.load("assets/tiles/dirt.png")
GRASS_b.blit(grassunder, (0,0))
GRASS_b.blit(pygame.transform.rotate(grassunder, 90), (0,0))
GRASS_b.blit(pygame.transform.rotate(grassunder, 270), (0,0))
GRASS_b.blit(grassdark, (0,0))
GRASS_b.blit(pygame.transform.rotate(grassdark, 90), (0,0))
GRASS_b.blit(pygame.transform.rotate(grassdark, 270), (0,0))
GRASS_b.blit(grass, (0,0))
GRASS_b.blit(pygame.transform.rotate(grass, 90), (0,0))
GRASS_b.blit(pygame.transform.rotate(grass, 270), (0,0))

BLUE = pygame.Surface((16,16))
BLUE.fill((0,0,255))