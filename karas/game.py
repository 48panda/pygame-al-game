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
    self.zoom = pygame.surface.Surface([1920, 1080])
    self.nozoom = pygame.surface.Surface([1920, 1080], pygame.SRCALPHA)
    self.zoompos = (1920//2, 1080//2)
    self.zoomamount = 1
    self.actualzoom = (0,0)
    print("START")

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
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:
          self.zoomamount += 0.1
        if event.button == 5:
          self.zoomamount -= 0.1
        self.zoomamount = max(min(self.zoomamount, 2), 1)
    
  def get_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == self.exit_key:
          self.quit()
        self.triggerevent(Enums.KEYPRESS, pygame.key.name(event.key))
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:
          self.zoomamount += 0.1
        if event.button == 5:
          self.zoomamount -= 0.1
        self.zoomamount = max(min(self.zoomamount, 2), 1)
          
      yield event

  def render(self):
    zoomed = pygame.transform.scale(self.zoom, (1920 * self.zoomamount, 1080*self.zoomamount))
    self.zoom.fill((255, 255, 255))
    area = pygame.Rect(0, 0, 1920, 1080)
    area.center = self.zoompos[0] * self.zoomamount, self.zoompos[1] * self.zoomamount
    if area.left < 0:
      area.left = 0
    if area.top < 0:
      area.top = 0
    if area.bottom > 1080*self.zoomamount:
      area.bottom = 1080*self.zoomamount
    if area.right > 1920*self.zoomamount:
      area.right = 1920*self.zoomamount
    self.actualzoom = area.topleft
    self.game.blit(zoomed, (0,0), area=area)
    #self.game.blit(self.nozoom, (0,0))
    pygame.display.update()
  
  def unzoompoint(self, x, y):
    tx, ty = self.actualzoom
    s = self.zoomamount
    return (x + tx)/s, (y + ty)/s