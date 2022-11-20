import pygame
import karas
import math
import PIL
from PIL import Image
import numpy as np
from zipfile import ZipFile
import io

def extract_zip(input_zip):
    input_zip=ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}

player_assets = {}

for name, data in extract_zip(r"assets\player\player.tc").items():
  if name.endswith(".png") and name!="Thumbnail.png":
    layerName = name.split(",")[3]
    if layerName == "Background":
      CHARACTER = Image.open(io.BytesIO(data))
    else:
      player_assets[layerName] = np.array(Image.open(io.BytesIO(data)))


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

def hueOther(color, name):
  img = player_assets[name]
  d = 0
  l = 255
  r, g, b, a = img[:,:,0], img[:,:,1], img[:,:,2], img[:,:,3]
  md = (r == d) & (g == d) & (b == d) & (a > 1)
  ml = (r == l) & (g == l) & (b == l) & (a > 1)
  im = np.copy(img)
  im[:,:,:3][md] = (color[0]//2, color[1]//2, color[2]//2)
  im[:,:,:3][ml] = color
  return pilImageToSurface(Image.fromarray(im))

def hueEye(color, name):
  img = player_assets[name]
  d = 0
  r, g, b, a = img[:,:,0], img[:,:,1], img[:,:,2], img[:,:,3]
  md = (r == d) & (g == d) & (b == d) & (a > 1)
  im = np.copy(img)
  im[:,:,:3][md] = color
  return pilImageToSurface(Image.fromarray(im))

def scale2x(im):
  return pygame.transform.scale(im, (im.get_width() * 2, im.get_height() * 2))

class placeholderSprite(pygame.sprite.Sprite):
  def __init__(self, rect):
    super().__init__()
    self.rect = rect

class Color:
  def __init__(self, r, g, b):
    self.r = r
    self.g = g
    self.b = b
  
  change = __init__

  def get(self):
    return (self.r, self.g, self.b)
  
  def __str__(self):
    return hex(self.r)[2:].zfill(2) + hex(self.g)[2:].zfill(2) + hex(self.b)[2:].zfill(2)

MALE_HAIR = [1,3]
FEMALE_HAIR = [2]
MAX_TOP = 3

EYE_COLORS = [(99,78,52), (46,83,111), (61,103,29), (28,120,71), (73,118,101)]
HAIR_COLORS = [(45, 10, 0), (57, 29, 0), (137, 85, 20), (250, 240, 190)]
SKIN_COLORS = [(141, 85, 36), (198, 134, 66), (224, 172, 105), (241, 194, 125), (255, 219, 172)]

class CharacterCreationValues:
  def __init__(self, string = None):
    self.hair = 3
    self.top = 1
    self.eyecolor = Color(0, 0, 0)
    self.topcolor = Color(0, 255, 0)
    self.haircolor = Color(255, 0, 255)
    self.skincolor = Color(200,200,200)
    self.legcolor = Color(0,0,255)
    if string:
      version = string[0]
      if version == "1": # Check for version here for backwards compatibility. Version increments every release that allows game saves and changes the format (unofficial releases may break when updating)
        self.hair = int(string[1])
        self.top = int(string[2])
        self.eyecolor  = Color(int(string[3:5], 16), int(string[5:7], 16), int(string[7:9], 16))
        self.topcolor  = Color(int(string[9:11], 16), int(string[11:13], 16), int(string[13:15], 16))
        self.haircolor = Color(int(string[15:17], 16), int(string[17:19], 16), int(string[19:21], 16))
        self.skincolor = Color(int(string[21:23], 16), int(string[23:25], 16), int(string[25:27], 16))
        self.legcolor  = Color(int(string[27:29], 16),
         int(string[29:31], 16),
          int(string[31:33], 16))
  
  def __str__(self):
    return f"1{str(self.hair)}{str(self.top)}{str(self.eyecolor)}{str(self.topcolor)}{str(self.haircolor)}{str(self.skincolor)}{str(self.legcolor)}"
  
  def getImage(self):
    skin = hueSkinColor(self.skincolor.get())
    eyes = hueEye(self.eyecolor.get(), f"Eyes1")
    top = hueOther(self.topcolor.get(), f"Top{self.top}")
    hair = hueOther(self.haircolor.get(), f"Hair{self.hair}")
    leg = hueOther(self.legcolor.get(), f"Legs1")
    skin.blit(eyes, (0, 0))
    skin.blit(top, (0, 0))
    skin.blit(hair, (0, 0))
    skin.blit(leg, (0, 0))
    return scale2x(skin)


class Character(karas.sprite.Sprite):
  bottomLeftAligned = True
  spritesheet = True
  spritewidth = 40
  spriteheight = 56
  num_sprites = 4
  player = False
  clockcycle = 10
  def __init__(self, world, *args, cstring=None, **kwargs):
    self.world = world
    super().__init__(*args, **kwargs)
    self.x = 100
    self.y = 40
    c = CharacterCreationValues(string=cstring)
    self.fromSpriteSheet(c.getImage())
    self.vx = 0
    self.vy = 0
    self.jump = 0
    self.flipped = True
    self.walktimer = 0

  def onupdate(self, *args, **kwargs):
    if self.pos[0] < 0 or self.pos[0] > 1920:
      return
    new = self.rect
    self.vy += 0.15
    new.bottomleft = self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly
    c = new.midbottom
    new.width = 26
    new.height = 48
    new.midbottom = c
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

    d = new.midbottom
    new.height = 56
    new.width = 40
    new.midbottom = d
    self.x = (new.left + self.world.scrollx) / 16
    self.y = (new.bottom + self.world.scrolly) / 16
    
    
    self.vx *= 0.7
    self.vy *= 0.9
    if abs(self.vx) < 0.01:
      self.vx = 0
    self.x = min(len(self.world.level[0]) - 1 - (self.spritewidth / 16), max(0, self.x))
    if self.player:
      self.world.update()
    self.pos = self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly
    if self.vy != 0:
      self.setSprite(3, self.flipped)
    elif self.vx == 0:
      self.setSprite(0, self.flipped)
    elif self.vx != 0:
      if self.walktimer < self.clockcycle/2:
        self.setSprite(1, self.flipped)
      else:
        self.setSprite(2, self.flipped)
      self.walktimer = (self.walktimer + 1) % self.clockcycle
      
  def postupdate(self):
    pass