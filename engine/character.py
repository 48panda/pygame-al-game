import pygame
import karas
import math
from zipfile import ZipFile
import io
def extract_zip(input_zip):
  """Extract files from a zip
  """
  input_zip=ZipFile(input_zip)
  return {name: input_zip.read(name) for name in input_zip.namelist()}

player_assets = {}
#                                      /------/---VS Code highlights these but the r" means it doesn't escape.
#                                      v      v
for name, data in extract_zip(r"assets\player\player.tc").items():
  if name.endswith(".png") and name!="Thumbnail.png":
    layerName = name.split(",")[3]
    if layerName == "Background":
      # The skin
      CHARACTER = pygame.image.load(io.BytesIO(data)).convert_alpha()
    else:
      # load assets
      player_assets[layerName] = pygame.image.load(io.BytesIO(data)).convert_alpha()



def replace(surface, mappings):
    # Replace colours in surface as specified by mappings ({ colour_from : colour_to ... })
    w, h = surface.get_size()
    for x in range(w):
        for y in range(h):
          # This is probably really slow for large images but this is only on 100x40ish
          # And is either only called once or if called per frame, it is the only (large)
          # thing it has to achieve in the frame
          if surface.get_at((x, y))[3] > 128:
            prev = surface.get_at((x, y))[:3]
            if prev in mappings:
              surface.set_at((x,y), pygame.Color(*mappings[prev]))


def hueSkinColor(colour):
  # Get skin colour mappings from colour
  darker = (colour[0]//2, colour[1]//2, colour[2]//2, 255)#karas.utils.darken_colour(*colour, factor=0.7)
  dark = 88
  light = 195
  this = CHARACTER.convert_alpha()
  replace(this, {(dark, dark, dark): darker, (light, light, light): colour})
  return this

def hueEye(colour, name):
  # Get Eye mappings from colour
  img = player_assets[name].convert_alpha()
  d = 0  
  replace(img, {(d,d,d):colour}) 
  return img

def hueOther(colour, name):
  # Get mappings for any other part from colour
  img = player_assets[name].convert_alpha()
  d = 0
  l = 255
  replace(img, {(d,d,d):(colour[0]//2, colour[1]//2, colour[2]//2, 255), (l,l,l):colour}) 
  return img

def scale2x(im):
  return pygame.transform.scale(im, (im.get_width() * 2, im.get_height() * 2))

class Color:
  """Class holding r, g, b value which can be turned into a string easily. (to save)
  """
  def __init__(self, r, g, b):
    self.r = r
    self.g = g
    self.b = b
  
  change = __init__

  def get(self):
    return (self.r, self.g, self.b, 255)
  
  def rgb(self, rgb):
    self.r , self.g, self.b = rgb
  
  def __str__(self):
    return hex(self.r)[2:].zfill(2) + hex(self.g)[2:].zfill(2) + hex(self.b)[2:].zfill(2)

# Define number of hairs and tops
MALE_HAIR = [1,3]
FEMALE_HAIR = [2]
MAX_HAIR = 3
MAX_TOP = 3

# Presets for color pickers (todo: add more?)
EYE_COLORS = [(99,78,52), (46,83,111), (61,103,29), (28,120,71), (73,118,101)]
HAIR_COLORS = [(45, 10, 0), (57, 29, 0), (137, 85, 20), (250, 240, 190)]
SKIN_COLORS = [(141, 85, 36), (198, 134, 66), (224, 172, 105), (241, 194, 125), (255, 219, 172)]

class CharacterCreationValues:
  """A Class that fully describes a character and can be easily converted to/from a string to save.
  """
  def __init__(self, string = None):
    self.hair = 3
    self.top = 1
    self.eyecolour = Color(*EYE_COLORS[0])
    self.topcolour = Color(0, 255, 0)
    self.haircolour = Color(*HAIR_COLORS[0])
    self.skincolour = Color(*SKIN_COLORS[0])
    self.legcolour = Color(0,0,255)
    if string:
      version = string[0]
      if version == "1": # Check for version here for backwards compatibility. Version increments every release that allows game saves and changes the format (unofficial releases may break when updating)
        self.hair = int(string[1])
        self.top = int(string[2])
        self.eyecolour  = Color(int(string[3:5], 16), int(string[5:7], 16), int(string[7:9], 16))
        self.topcolour  = Color(int(string[9:11], 16), int(string[11:13], 16), int(string[13:15], 16))
        self.haircolour = Color(int(string[15:17], 16), int(string[17:19], 16), int(string[19:21], 16))
        self.skincolour = Color(int(string[21:23], 16), int(string[23:25], 16), int(string[25:27], 16))
        self.legcolour  = Color(int(string[27:29], 16),
         int(string[29:31], 16),
          int(string[31:33], 16))
  
  def __str__(self):
    return f"1{str(self.hair)}{str(self.top)}{str(self.eyecolour)}{str(self.topcolour)}{str(self.haircolour)}{str(self.skincolour)}{str(self.legcolour)}"
  
  def getImage(self):
    # Get texture from this.
    skin = hueSkinColor(self.skincolour.get())
    eyes = hueEye(self.eyecolour.get(), f"Eyes1")
    top = hueOther(self.topcolour.get(), f"Top{self.top}")
    hair = hueOther(self.haircolour.get(), f"Hair{self.hair}")
    leg = hueOther(self.legcolour.get(), f"Legs1")
    skin.blit(eyes, (0, 0))
    skin.blit(top, (0, 0))
    skin.blit(hair, (0, 0))
    skin.blit(leg, (0, 0))
    return scale2x(skin)


class Character(karas.sprite.Sprite):
  """Base class for all character types.
  """
  bottomLeftAligned = True
  spritesheet = True
  spritewidth = 40
  spriteheight = 56
  num_sprites = 4
  player = False
  clockcycle = 10 # for running animation
  def __init__(self, world, *args, cstring=None, hasBeenLoaded=False,  **kwargs):
    self.world = world
    super().__init__(*args, hasBeenLoaded=hasBeenLoaded, **kwargs)
    if not hasBeenLoaded:
      # If loading from save file, correct values already are loaded here
      self.x = 100
      self.y = 40 # Default value (overridden at some point)
      self.cstring=cstring
    c = CharacterCreationValues(string=self.cstring)
    self.fromSpriteSheet(c.getImage())
    self.vx = 0
    self.vy = 0
    self.jump = 0
    self.flipped = True
    self.walktimer = 0
    self.out_of_frame = False

  def onupdate(self, *args, **kwargs):
    # Do collision. It is quite a mess tbh
    self.pos = self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly
    # Get screen position
    if self.pos[0] < -80 or self.pos[0] > 1920:
      self.out_of_frame = True
      # Unloads characters not visible to stop them falling out of the map (which took a while to figure out!)
      return
    self.out_of_frame = False
    new = self.rect
    self.vy += 0.15 # Gravity
    new.bottomleft = self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly
    # Rect on screen

    # Reduce hitbox for collision detection -- lots of the width is unused.
    c = new.midbottom
    new.width = 26
    new.height = 40
    new.midbottom = c

    new.left = (self.x + self.vx) * 16 - self.world.scrollx + 7
    # Move along x axis first (to know which way to move if thyre is a collision)
    if len(new.collidelistall(self.world.rects)) != 0 and not self.out_of_frame:
      if self.vy == 0.15:
        # Allows the character to automatically move up a tile
        new.bottom -= 16
      if self.vy != 0.15 or len(new.collidelistall(self.world.rects)) != 0 and not self.out_of_frame:
        # If still collisions after moving up a tile
        if self.vy == 0.15:
          # move down if moved up
          new.bottom += 16
        # Move as far as can without colliding
        for coll in new.collidelistall(self.world.rects):
          block = self.world.rects[coll]
          if self.vx > 0:
            new.right = min(new.right, block.left)
          elif self.vx < 0:
            new.left = max(new.left, block.right)
        self.vx = 0
    # Move along Y axis
    new.bottom = (self.y + self.vy) * 16 - self.world.scrolly
    if len(new.collidelistall(self.world.rects)) != 0 and not self.out_of_frame:
      # Move as far as can without colliding
      for coll in new.collidelistall(self.world.rects):
        block = self.world.rects[coll]
        if self.vy > 0:
          new.bottom = min(new.bottom, block.top)
        elif self.vy < 0:
          new.top = max(new.top, block.bottom)
      self.vy = 0

    # reset width after collision detection
    d = new.midbottom
    new.height = 56
    new.width = 40
    new.midbottom = d

    # Convert back to block coordinates
    self.x = (new.left + self.world.scrollx) / 16
    self.y = (new.bottom + self.world.scrolly) / 16
    
    
    self.vx *= 0.7 # Apply Drag
    self.vy *= 0.9 # Apply drag
    if abs(self.vx) < 0.01: # If the player is essentially stopped, set to 0.
      self.vx = 0
    if self.player:
      # Stops the player going out of bounds horizontally
      self.x = min(len(self.world.level[0]) - 1 - (self.spritewidth / 16), max(0, self.x))
      # Update the world for scroll related reasons
      self.world.update()
    # Set sprite position for rendering
    self.pos = self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly
    # Choose which sprite to display base off of velocity.
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