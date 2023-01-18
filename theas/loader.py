import pygame

pygame.font.init()

# Simple loading screen Pumps events in times of heavy computing need
class LoadingScreen:
  def __init__(self, screen, text="Booting..."):
    self.text = text
    self.screen = screen
    self.font = pygame.font.SysFont("Calibri", 50)
    self.timetext = ""
    self.timefont = pygame.font.SysFont("Calibri", 200)
    self.update()
  
  def update(self, newText=None, timeText =None):
    if newText:
      self.text = newText
    if timeText is not None:
      self.timetext = timeText
    self.screen.fill((0,0,0))
    self.screen.blit(self.font.render(self.text, True, (255, 255, 255)), (0, 1080 - 50))
    txt = self.timefont.render(self.timetext, True, (0, 196, 190))
    r = txt.get_rect()
    r.center = self.screen.get_rect().center
    self.screen.blit(txt, r.topleft)
    pygame.display.update()
    pygame.event.pump()