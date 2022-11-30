import pygame
from karas.types import Enums
from karas.types import QuitTriggered
from karas.sprite import Sprite
import karas.keypad

class Game:
  def __init__(self,window_size = None, exit_key = pygame.K_ESCAPE, color = (255, 255, 255)):
    pygame.init()
    size = (1920,1080)
    if type(window_size) == tuple:
      size = window_size
    else:
      flags = pygame.FULLSCREEN | pygame.SCALED
    self.game = pygame.display.set_mode(size)#, flags)
    self.exit_key = exit_key
    self.color = color
    self.zoom = pygame.surface.Surface([1920, 1080])
    self.nozoom = pygame.surface.Surface([1920, 1080], pygame.SRCALPHA)
    self.zoompos = (1920//2, 1080//2)
    self.zoomamount = 1
    self.actualzoom = (0,0)
    self.keypad = karas.keypad.Keypad(self.nozoom)
    self.world = None
  
  def assign_world(self, world):
    self.world = world
    self.keypad.world = world

  def quit(self):
    pygame.quit()
    raise QuitTriggered()    
  
  def event(self, event):
    if self.keypad.event(event): return True
    if event.type == pygame.QUIT:
      self.quit()
      return True
    if event.type == pygame.KEYDOWN:
      if event.key == self.exit_key:
        self.quit()
        return True
      if event.key == pygame.K_i:
        self.zoomamount += 0.1
        self.zoomamount = max(min(self.zoomamount, 4), 1)
        return True
      if event.key == pygame.K_o:
        self.zoomamount -= 0.1
        self.zoomamount = max(min(self.zoomamount, 4), 1)
        return True

  def render(self):
    area = pygame.Rect(0, 0, 1920 // self.zoomamount, 1080 // self.zoomamount)
    area.center = self.zoompos[0], self.zoompos[1]
    if hasattr(self.world, "player"):
      area.center = self.world.player.rect.center
    if area.left < 0:
      area.left = 0
    if area.top < 0:
      area.top = 0
    if area.bottom > 1080:
      area.bottom = 1080
    if area.right > 1920:
      area.right = 1920
    self.actualzoom = area.topleft
    self.keypad.draw()
    cropped = pygame.Surface(area.size)
    cropped.blit(self.zoom, (0,0), area=area)
    pygame.transform.scale(cropped, (1920, 1080), dest_surface=self.game)
    #self.game.blit(self.zoom, (0,0))
    self.zoom.fill((149, 255, 255))
    self.game.blit(self.nozoom, (0,0))
    self.nozoom.fill((0, 0, 0, 0))
    pygame.display.update()
  
  def unzoompoint(self, x, y):
    tx, ty = self.actualzoom
    s = self.zoomamount
    return x/s + tx, y/s + ty