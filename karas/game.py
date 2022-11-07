import pygame
from karas.types import Enums
from karas.types import QuitTriggered
from karas.sprite import Sprite

class Game:
  def __init__(self,window_size = None, exit_key = pygame.K_ESCAPE, color = (255, 255, 255)):
    pygame.init()
    size = (1920,1080)
    if type(window_size) == tuple:
      size = window_size
    else:
      flags = pygame.FULLSCREEN | pygame.SCALED
    self.game = pygame.display.set_mode(size, flags)
    self.keybinds = {}
    self.exit_key = exit_key
    self.color = color

  def triggerevent(self, event, *args, **kwargs):
    if not event in self.keybinds:
      return False
    self.keybinds[event](*args, **kwargs)
    return True

  def bind(self, event, callback):
    self.keybinds[event] = callback

  def quit(self):
    pygame.quit()
    raise QuitTriggered()

  def events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == self.exit_key:
          self.quit()
        self.triggerevent(Enums.KEYPRESS, pygame.key.name(event.key))
    
  def get_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == self.exit_key:
          self.quit()
        self.triggerevent(Enums.KEYPRESS, pygame.key.name(event.key))
      yield event

  def render(self):
    pygame.display.update()