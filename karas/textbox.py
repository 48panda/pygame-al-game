import karas.sprite
import pygame
import time

class TextInput(karas.sprite.Sprite):
  topLeftAligned = True
  def init(self, font, pos, color, width, rectColor):
    self.text = ""
    self.rectColor = rectColor
    self.pos = pos
    self.font = font
    self.color = color
    self.maxwidth = width
    self.focused = False
    self.im = pygame.Surface((self.maxwidth, font.render("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", True, color).get_height()))
    self.im.fill(self.rectColor)
    self.im.blit(font.render(self.text, True, color), (0,0))
    self.cursor = pygame.Surface((5, self.im.get_height()))
    self.cursor.fill(color)
  
  def onupdate(self):
    self.im.fill(self.rectColor)
    txt = self.font.render(self.text, True, self.color)
    self.im.blit(txt, (0,0))
    if self.focused and time.time() % 1 < 0.5:
      self.im.blit(self.cursor, self.cursor.get_rect(midleft=txt.get_rect().midright).topleft)
  
  def event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        if pygame.Rect(self.pos[0], self.pos[1], self.maxwidth, self.rect.height).collidepoint(event.pos):
          self.focused = not self.focused
          return True
        else:
          self.focused = False
      else:
        self.focused = False
    elif event.type == pygame.KEYDOWN:
      if self.focused:
        if event.key == pygame.K_BACKSPACE:
          self.text = self.text[:-1]
        if event.unicode in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_- ":
          self.text += event.unicode
          if self.font.render(self.text, True, self.color).get_width() > self.maxwidth:
            self.text = self.text[:-1]
        return True