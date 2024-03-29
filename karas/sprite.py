import pygame
import karas.utils

class Sprite(pygame.sprite.Sprite):
  # Base class for sprites
  hover = False
  width = 50
  height = 50
  bottomLeftAligned = False
  topLeftAligned = False
  spritesheet = False
  spritewidth = 0
  spriteheight = 0
  num_sprites = 0
  def __init__(self, *args,rectoffset=(0,0), **kwargs):
    self.rect = pygame.Rect(0,0,0,0)
    self.rectoffset = rectoffset
    super().__init__()
    self.im = pygame.Surface([self.width, self.height])
    self.hoverim = pygame.Surface([self.width, self.height])
    self.pos = 0, 0
    self.init(*args, **kwargs)
    if self.spritesheet:
      self.flipped = False
    self.spritenum = 0
  
  def fromSpriteSheet(self, sheet):
    # Spritesheet to list of images
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
  # Set sprite from spritesheet
  def setSprite(self, num, flipped = False):
    if self.spritesheet:
      self.spritenum = num
      if not flipped:
        self.im = self.sprites[num]
      else:
        self.im = self.flippedsprites[num]
  
  # Functions children define
  def postupdate(self, *args, **kwargs): ...
  def init(self, *args, **kwargs): ...
  def onupdate(self, *args, **kwargs): ...
  
  def update(self, *args, callupdate=True, **kwargs):
    self.rect = self.im.get_rect()
    # set rect position
    if self.bottomLeftAligned:
      self.rect.bottomleft = self.pos
    elif self.topLeftAligned:
      self.rect.topleft = self.pos
    else:
      self.rect.center = self.pos
    # Update child class
    if callupdate:
      self.onupdate(*args, **kwargs)
    # Get new rect and align
    self.rect = self.im.get_rect()
    if self.bottomLeftAligned:
      self.rect.bottomleft = self.pos
    elif self.topLeftAligned:
      self.rect.topleft = self.pos
    else:
      self.rect.center = self.pos
    # set to hover image if needed
    if self.hover:
      if self.rect.collidepoint((pygame.mouse.get_pos()[0] - self.rectoffset[0], pygame.mouse.get_pos()[1] - self.rectoffset[1])):
        self.image = self.hoverim
      else:
        self.image = self.im
    else:
      self.image = self.im
    self.postupdate()

class Button(Sprite):
  # A text button
  hover = True
  bottomLeftAligned = True
  def init(self, text, color, pos=(100, 100), border_radius=5,padding=10, size=40, darker_text=False, darker_hover=False, font=None, text_color=None, onClick=None):
    # set font
    font = font or pygame.font.SysFont("Ariel", size)
    self.onclick = onClick
    # Draw unhover button
    if darker_text:
      text_color = text_color or karas.utils.darken_color(*color, factor = 0.5)
    else:
      text_color = text_color or karas.utils.lighten_color(*color, factor = 0.5)
    text_surface = font.render(text, True, text_color)
    padded_text = pygame.rect.Rect(0, 0, text_surface.get_width() + padding*2, text_surface.get_height() + padding*2)
    padded_surface = pygame.Surface(padded_text.size, pygame.SRCALPHA)
    padded_surface.fill((255,255,255,0))
    karas.utils.draw_rounded_rect(padded_surface, padded_text, color, border_radius)
    padded_surface.blit(text_surface, (padding, padding))
    self.im = padded_surface
    # Draw hover button
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
    padded_surface.fill((255,255,255,0))
    karas.utils.draw_rounded_rect(padded_surface, padded_text, color, border_radius)
    padded_surface.blit(text, (padding, padding))
    self.hoverim = padded_surface

    self.pos = pos
  
  def event(self, event):
    # if clicked call onclick
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        if self.rect.collidepoint((event.pos[0] - self.rectoffset[0], event.pos[1] - self.rectoffset[1])):
          if self.onclick:
            self.onclick()
          return True