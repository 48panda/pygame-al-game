import pygame
from karas.types import QuitTriggered
from karas.sprite import Sprite
import karas.keypad
import constants
import theas

class Game:
  def __init__(self, clock,savename, window_size = None, exit_key = pygame.K_ESCAPE, colour = (255, 255, 255), hasBeenLoaded=False):
    # Setup window
    pygame.init()
    size = (1920,1080)
    if type(window_size) == tuple:
      size = window_size
    else:
      flags = pygame.FULLSCREEN | pygame.SCALED
    # Initialise attributes
    self.game = pygame.display.set_mode(size, flags)
    self.exit_key = exit_key
    self.colour = colour
    self.clock = clock
    self.zoom = pygame.surface.Surface([1920, 1080])
    self.nozoom = pygame.surface.Surface([1920, 1080], pygame.SRCALPHA)
    self.zoompos = (1920//2, 1080//2)
    self.zoomamount = 1
    self.actualzoom = (0,0)
    self.keypad = karas.keypad.Keypad(self.nozoom)
    self.loadingScreen = None
    self.exit_to_title = False
    self.savename = savename
    if not hasBeenLoaded:
      self.world = None
  
  def __getstate__(self):
    return (1,self.world)
  
  def __setstate__(self, state):
    if state[0] == 1:
      _, self.world = state
  
  def assign_world(self, world):
    self.world = world
    self.keypad.world = world

  def assign_loading_screen(self, loadingScreen):
    self.loadingScreen = loadingScreen

  def quit(self):
    pygame.quit()
    raise QuitTriggered() # just go straight to main.py. essentially equivalent to purposefully dropping something and catching it at the last minute instead of lowering it carefully 
  
  def event(self, event):
    if self.keypad.event(event): return True # Relay event to keypad
    if event.type == pygame.QUIT:
      self.quit()
    if event.type == pygame.KEYDOWN:
      if event.key == self.exit_key:
        action = theas.esc.do_esc_screen(self.game, self.clock, self.loadingScreen)
        if action == "cont":
          return True
        elif action == "save":
          theas.saver.save(self)
          self.exit_to_title = True
          return True
      # zoom
      if event.key == pygame.K_i:
        self.zoomamount += 0.1
        self.zoomamount = max(min(self.zoomamount, 4), 1)
        return True
      if event.key == pygame.K_o:
        self.zoomamount -= 0.1
        self.zoomamount = max(min(self.zoomamount, 4), 1)
        return True

  def render(self):
    # area to show (zoom)
    area = pygame.Rect(0, 0, 1920 // self.zoomamount, 1080 // self.zoomamount)
    area.center = self.zoompos[0], self.zoompos[1]
    if hasattr(self.world, "player"):
      area.center = self.world.player.rect.center
    # make zoom area be inbounds
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
    # zoom
    cropped = pygame.Surface(area.size)
    cropped.blit(self.zoom, (0,0), area=area)
    pygame.transform.scale(cropped, (1920, 1080), dest_surface=self.game)
    # draw stuff
    self.zoom.fill((149, 255, 255))
    self.game.blit(self.nozoom, (0,0))
    self.nozoom.fill((0, 0, 0, 0))
    # update screen
    pygame.display.update()
  
  def unzoompoint(self, x, y):
    #screen coords to unzoomed screen coords
    tx, ty = self.actualzoom
    s = self.zoomamount
    return x/s + tx, y/s + ty