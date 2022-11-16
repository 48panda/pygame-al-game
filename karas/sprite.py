import pygame
import karas.utils

class Sprite(pygame.sprite.Sprite):
  hover = False
  width = 50
  height = 50
  bottomLeftAligned = False
  spritesheet = False
  spritewidth = 0
  spriteheight = 0
  num_sprites = 0
  def __init__(self, *args, **kwargs):
    self.rect = pygame.Rect(0,0,0,0)
    super().__init__()
    self.im = pygame.Surface([self.width, self.height])
    self.hoverim = pygame.Surface([self.width, self.height])
    self.pos = 0, 0
    self.init(*args, **kwargs)
    if self.spritesheet:
      self.flipped = False
    self.spritenum = 0
  
  def fromSpriteSheet(self, sheet):
    if not self.spritesheet:
      self.im = sheet
      return
    sprites = []
    for i in range(self.num_sprites):
      sprite = pygame.Surface((self.spritewidth, self.spriteheight), pygame.SRCALPHA)
      sprite.blit(sheet, (0,0), area=(i*self.spritewidth, 0, self.spritewidth, self.spriteheight))
      sprites.append(sprite)
    self.sprites = sprites
    self.flippedsprites = [pygame.transform.flip(i, True, False) for i in sprites]

  def setSprite(self, num, flipped = False):
    if self.spritesheet:
      self.spritenum = num
      if not flipped:
        self.im = self.sprites[num]
      else:
        self.im = self.flippedsprites[num]
  def postupdate(self):
    pass
  def init(self):
    pass
  
  def update(self, *args, **kwargs):
    self.rect = self.im.get_rect()
    if self.bottomLeftAligned:
      self.rect.bottomleft = self.pos
    else:
      self.rect.center = self.pos
    self.onupdate(*args, **kwargs)
    self.rect = self.im.get_rect()
    if self.bottomLeftAligned:
      self.rect.bottomleft = self.pos
    else:
      self.rect.center = self.pos
    if self.hover:
      if self.rect.collidepoint(pygame.mouse.get_pos()):
        self.image = self.hoverim
      else:
        self.image = self.im
    else:
      self.image = self.im
    self.postupdate()
  def onupdate(self):
    pass

class Group(pygame.sprite.Group):
  def __init__(self, spriteClass):
    super().__init__()
    self.spriteClass = spriteClass
  def createNew(self, *args, **kwargs):
    return self.add(self.spriteClass(*args, **kwargs))

class Button(Sprite):
  hover = True
  def init(self, text, color, pos=(100, 100), border_radius=5,padding=10, size=40, darker_text=False, darker_hover=False):
    font = pygame.font.SysFont("Ariel", size)
    if darker_text:
      text_color = karas.utils.darken_color(*color, factor = 0.5)
    else:
      text_color = karas.utils.lighten_color(*color, factor = 0.5)
    text_surface = font.render(text, True, text_color)
    padded_text = pygame.rect.Rect(0, 0, text_surface.get_width() + padding*2, text_surface.get_height() + padding*2)
    padded_surface = pygame.Surface(padded_text.size, pygame.SRCALPHA)
    padded_surface.fill((255,255,255,255))
    karas.utils.draw_rounded_rect(padded_surface, padded_text, color, border_radius)
    padded_surface.blit(text_surface, (padding, padding))
    self.im = padded_surface

    if darker_hover:
      color = karas.utils.darken_color(*color, factor = 0.3)
    else:
      color = karas.utils.lighten_color(*color, factor = 0.3)

    if darker_text:
      text_color = karas.utils.darken_color(*color, factor = 0.5)
    else:
      text_color = karas.utils.lighten_color(*color, factor = 0.5)
    text = font.render(text, True, text_color)
    padded_text = pygame.rect.Rect(0, 0, text.get_width() + padding*2, text.get_height() + padding*2)
    padded_surface = pygame.Surface(padded_text.size, pygame.SRCALPHA)
    padded_surface.fill((255,255,255,255))
    karas.utils.draw_rounded_rect(padded_surface, padded_text, color, border_radius)
    padded_surface.blit(text, (padding, padding))
    self.hoverim = padded_surface

    self.pos = pos


class TransparentButton(Sprite):
  hover = True
  def init(self, text, color=(0,0,0), hover_color=(89, 92, 0), pos=(100, 100), size=40):
    font = pygame.font.SysFont("Ariel", size)
    self.im = font.render(text, True, color)
    self.hoverim = font.render(text, True, hover_color)
    self.pos = pos