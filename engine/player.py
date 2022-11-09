import pygame
import karas
import math

PLAYER = pygame.image.load("assets/player/template.png")

class placeholderSprite(pygame.sprite.Sprite):
  def __init__(self, rect):
    super().__init__()
    self.rect = rect

class Player(karas.sprite.Sprite):
  bottomLeftAligned = True
  spritesheet = True
  spritewidth = 40
  spriteheight = 56
  num_sprites = 3
  def init(self, world):
    
    self.world = world
    self.x = 0
    self.y = 40
   
    self.fromSpriteSheet(pygame.transform.scale(PLAYER, (PLAYER.get_size()[0]*2, PLAYER.get_size()[1]*2)))
    self.vx = 0
    self.vy = 0
    self.jump = 0
    self.flipped = True
    self.walktimer = 0
  #def getDirection(self, c, block):
  #  changex = c[0] - self.rect.center[0]
  #  changey = c[1] - self.rect.center[1]
  #  if changey == 0:
  #    if changex > 0:
  #      return "+x"
  #    return "-x"
  #  if changex == 0:
  #    if changey > 0:
  #      return "+y"
  #    return "-y"
  #  if changex > 0:
  #    if changey > 0:




  def onupdate(self):
    if self.jump > 0:
      self.vy -= 0.7
      self.jump -=1
    new = self.rect
    self.vy += 0.1
    new.bottomleft = self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly
    c = new.centerx
    new.width = 26
    new.centerx = c
    new.left = (self.x + self.vx) * 16 - self.world.scrollx + 7
    #new.left = max(new.left, 7)
    if len(new.collidelistall(self.world.rects)) != 0:
      for coll in new.collidelistall(self.world.rects):
        block = self.world.rects[coll]
        if self.vx > 0:
          new.right = min(new.right, block.left)
        elif self.vx < 0:
          new.left = max(new.left, block.right)
      self.vx = 0
    new.bottom = (self.y + self.vy) * 16 - self.world.scrolly
    if len(new.collidelistall(self.world.rects)) != 0:
      for coll in new.collidelistall(self.world.rects):
        block = self.world.rects[coll]
        if self.vy > 0:
          new.bottom = min(new.bottom, block.top)
        else:
          new.top = max(new.top, block.bottom)
      self.vy = 0

    d = new.center
    new.width = 40
    new.center = d
    self.x = (new.left + self.world.scrollx) / 16
    self.y = (new.bottom + self.world.scrolly) / 16
    
    
    self.vx *= 0.7
    self.vy *= 0.9
    if abs(self.vx) < 0.01:
      self.vx = 0
    self.x = min(len(self.world.level[0]) - 1 - (self.spritewidth / 16), max(0, self.x))
    self.world.update(self)
    self.pos = self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly
    if self.vx == 0:
      self.setSprite(0, self.flipped)
    if self.vx != 0:
      if self.walktimer < 5:
        self.setSprite(1, self.flipped)
      else:
        self.setSprite(2, self.flipped)
      self.walktimer = (self.walktimer + 1) %10
  def postupdate(self):
    self.world.game.zoompos = self.rect.center