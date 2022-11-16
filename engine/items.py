import karas
import pygame

ITEMS_IMG = pygame.image.load("assets/items/items.png")

DIRT = 1
WOODEN_PICKAXE = 2
TREE = 3

PICKAXES = [WOODEN_PICKAXE]

SPRITESHEET = pygame.transform.scale(ITEMS_IMG, (ITEMS_IMG.get_size()[0]*2, ITEMS_IMG.get_size()[1]*2))

NUM_SPRITES = 4

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
  def init(self, world, pos, vel, worldwidth, sprite):
    self.fromSpriteSheet(SPRITESHEET)
    self.setSprite(sprite)
    self.sprite = sprite
    self.pos = world.tileToScreenPos(*pos)
    self.coords = pos
    self.vel = vel
    self.world = world
    self.worldwidth = worldwidth

  def onupdate(self, rects):
    newrect = pygame.Rect((0,0), (20, 20))
    scale = 0.9
    self.coords = [ scale * ( self.coords[0] - self.world.player.x ) + self.world.player.x,
    scale * ( self.coords[1] - self.world.player.y ) + self.world.player.y]

    newrect.center = self.world.tileToScreenPos(*self.coords)

    newrect.top += self.vel[1]
    for c in newrect.collidelistall(rects):
      if self.vel[1] > 0:
        newrect.bottom = min(rects[c].top, newrect.bottom)
      elif self.vel[1] < 0:
        newrect.top = max(rects[c].bottom, newrect.top)
      self.vel[1] = 0
      self.vel[0] = 0
    self.vel[1] *= 0.9
    self.vel[1] += 0.5

    newrect.left += self.vel[0]
    if newrect.left < 0:
      newrect.left = - newrect.left
      self.vel[0] = -self.vel[0]
    if newrect.right > self.worldwidth:
      newrect.right = self.worldwidth - (newrect.right - self.worldwidth)
      self.vel[0] = -self.vel[0]

    for c in newrect.collidelistall(rects):
      if self.vel[0] > 0:
        newrect.right = min(rects[c].left, newrect.right)
      elif self.vel[0] < 0:
        newrect.left = max(rects[c].right, newrect.left)
      self.vel[0] = 0
    self.vel[0] *= 0.95
    self.pos = newrect.center
    self.coords = self.world.screenToTilePos(*self.pos)
  def postupdate(self):
    if self.rect.colliderect(self.world.player.rect):
      self.kill()
      self.world.player.inventory.give(self.sprite)
