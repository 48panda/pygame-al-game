import pygame
import karas
import math
import PIL
from PIL import Image
import numpy as np

CHARACTER = Image.open("assets/player/template.png")
data = np.array(CHARACTER)
red, green, blue, alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
dark = 88
#Image.fromarray(alpha, mode="L").show()
#Image.fromarray(alpha>=245, mode="L").show()
light = 195
maskdark = (dark - 10 < red) & (red < dark + 10) & (dark - 10 < green) & (green < dark + 10) & (dark - 10 < blue) & (blue < dark + 10) & (alpha > 1)
masklight = (light - 10 < red) & (red < light + 10) & (light - 10 < green) & (green < light + 10) & (light - 10 < blue) & (blue < light + 10) & (alpha > 1)

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode)

def hueSkinColor(color):
  darker = (color[0]//2, color[1]//2, color[2]//2)#karas.utils.darken_color(*color, factor=0.7)
  this = np.copy(data)
  this[:,:,:3][maskdark] = darker
  this[:,:,:3][masklight] = color
  return pilImageToSurface(Image.fromarray(this))

def scale2x(im):
  return pygame.transform.scale(im, (im.get_width() * 2, im.get_height() * 2))

class placeholderSprite(pygame.sprite.Sprite):
  def __init__(self, rect):
    super().__init__()
    self.rect = rect

class Character(karas.sprite.Sprite):
  bottomLeftAligned = True
  spritesheet = True
  spritewidth = 40
  spriteheight = 56
  num_sprites = 4
  def __init__(self, world, *args, **kwargs):
    self.world = world
    super().__init__(*args, **kwargs)
    self.x = 0
    self.y = 40
    self.fromSpriteSheet(scale2x(hueSkinColor((255, 184, 184))))
    self.vx = 0
    self.vy = 0
    self.jump = 0
    self.flipped = True
    self.walktimer = 0

  def update(self, *args, **kwargs):
    super().update(*args, **kwargs)
    new = self.rect
    self.vy += 0.15
    new.bottomleft = self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly
    c = new.centerx
    new.width = 26
    new.centerx = c
    new.left = (self.x + self.vx) * 16 - self.world.scrollx + 7
    #new.left = max(new.left, 7)
    if len(new.collidelistall(self.world.rects)) != 0:
      new.bottom -= 16
      if len(new.collidelistall(self.world.rects)) != 0:
        new.bottom += 16
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
    if self.vy != 0:
      self.setSprite(3, self.flipped)
    elif self.vx == 0:
      self.setSprite(0, self.flipped)
    elif self.vx != 0:
      if self.walktimer < 5:
        self.setSprite(1, self.flipped)
      else:
        self.setSprite(2, self.flipped)
      self.walktimer = (self.walktimer + 1) %10
  def postupdate(self):
    self.world.game.zoompos = self.rect.center