import pygame
import karas

class timedText(karas.sprite.Sprite):
  def init(self, text, font, color, pos, time):
    self.text = text
    self.font = font
    self.color = color
    self.pos = pos
    full = font.render(text, True, color)
    self.im = pygame.Surface(full.get_rect().size, pygame.SRCALPHA)
    self.time = time
    self.elapsed = 0
    self.char = 0
  def onupdate(self):
    if self.char >= len(self.text):
      return
    self.elapsed += 1
    if self.elapsed % self.time == 0:
      self.char += 1
      while self.char < len(self.text) and self.text[self.char] == " ":
        self.char += 1
      self.im.blit(self.font.render(self.text[:self.char], True, self.color), (0,0))
  def reset(self, newText=None):
    if newText:
      self.text = newText
    self.elapsed = 0