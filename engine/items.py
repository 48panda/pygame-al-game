import karas
import pygame

ITEMS_IMG = pygame.image.load("assets/items/items.png")

DIRT = 1
WOODEN_PICKAXE = 2
TREE = 3
OBSIDIAN = 4

PLACABLE = [DIRT, OBSIDIAN]
PICKAXES = [WOODEN_PICKAXE]

SPRITESHEET = pygame.transform.scale(ITEMS_IMG, (ITEMS_IMG.get_size()[0]*2, ITEMS_IMG.get_size()[1]*2))

NUM_SPRITES = 5

class Item(karas.sprite.Sprite):
  spritesheet = True
  spritewidth = 32
  spriteheight = 32
  num_sprites = NUM_SPRITES
  def init(self, pos):
    self.pos = pos
    self.fromSpriteSheet(SPRITESHEET)
    

class InWorldItem(karas.sprite.Sprite):
  spritesheet = True
  spritewidth = 32
  spriteheight = 32
  num_sprites = NUM_SPRITES
  def init(self, world, pos, sprite):
    self.fromSpriteSheet(SPRITESHEET)
    self.setSprite(sprite)
    self.sprite = sprite
    self.pos = world.tileToScreenPos(*pos)
    self.world = world
  def onupdate(self, rects):
    newrect = pygame.Rect((0,0), (20, 20))
    scale = 0.85

    px = self.world.player.rect.centerx
    py = self.world.player.rect.centery
    mx = self.pos[0]
    my = self.pos[1]

    self.pos =  (scale * (mx - px) + px, scale * (my - py) + py)

  def postupdate(self):
    if self.rect.colliderect(self.world.player.rect):
      self.kill()
      self.world.player.inventory.give(self.sprite)
