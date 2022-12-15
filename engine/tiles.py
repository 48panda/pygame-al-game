import pygame
grassunder = pygame.image.load("assets/tiles/grassunder.png").convert_alpha()
grassdark = pygame.image.load("assets/tiles/grassdark.png").convert_alpha()
grass = pygame.image.load("assets/tiles/grass.png").convert_alpha()

LEAVES = pygame.image.load("assets/tiles/leaves.png").convert()
TREE = pygame.image.load("assets/tiles/tree.png").convert()
BEDROCK = pygame.image.load("assets/tiles/bedrock.png").convert()
OBSIDIAN = pygame.image.load("assets/tiles/obsidian.png").convert()
DIRT = pygame.image.load("assets/tiles/dirt.png").convert()
RADIANITE = pygame.image.load("assets/tiles/stone.png").convert()
RADIANITE.blit(pygame.image.load("assets/tiles/radianite.png").convert_alpha(), (0,0))
STONE = pygame.image.load("assets/tiles/stone.png").convert()
GRASS = pygame.image.load("assets/tiles/dirt.png").convert()
PLANKS = pygame.image.load("assets/tiles/planks.png").convert()
SAND = pygame.image.load("assets/tiles/sand.png").convert()
SANDSTONE = pygame.image.load("assets/tiles/sandstone.png").convert()
STONEBRICKS = pygame.image.load("assets/tiles/stonebricks.png").convert()
GRASS.blit(grassunder, (0,0))
GRASS.blit(grassdark, (0,0))
GRASS.blit(grass, (0,0))
GRASS_l = pygame.image.load("assets/tiles/dirt.png").convert()
GRASS_l.blit(grassunder, (0,0))
GRASS_l.blit(pygame.transform.rotate(grassunder, 90), (0,0))
GRASS_l.blit(grassdark, (0,0))
GRASS_l.blit(pygame.transform.rotate(grassdark, 90), (0,0))
GRASS_l.blit(grass, (0,0))
GRASS_l.blit(pygame.transform.rotate(grass, 90), (0,0))
GRASS_r = pygame.image.load("assets/tiles/dirt.png").convert()
GRASS_r.blit(grassunder, (0,0))
GRASS_r.blit(pygame.transform.rotate(grassunder, 270), (0,0))
GRASS_r.blit(grassdark, (0,0))
GRASS_r.blit(pygame.transform.rotate(grassdark, 270), (0,0))
GRASS_r.blit(grass, (0,0))
GRASS_r.blit(pygame.transform.rotate(grass, 270), (0,0))
GRASS_b = pygame.image.load("assets/tiles/dirt.png").convert()
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