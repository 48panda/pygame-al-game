import karas
import pygame

ITEMS_IMG = pygame.image.load("assets/items/items.png")

DIRT = 1
WOODEN_PICKAXE = 2

PICKAXES = [WOODEN_PICKAXE]

class Item(karas.sprite.Sprite):
  spritesheet = True
  spritewidth = 32
  spriteheight = 32
  num_sprites = 3
  def init(self, pos):
    self.pos = pos
    self.fromSpriteSheet(pygame.transform.scale(ITEMS_IMG, (ITEMS_IMG.get_size()[0]*2, ITEMS_IMG.get_size()[1]*2)))