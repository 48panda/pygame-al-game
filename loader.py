import pygame

pygame.font.init()

class LoadingScreen:
  def __init__(self, screen, text="Booting..."):
    self.text = text
    self.screen = screen
    self.font = pygame.font.SysFont("Calibri", 50)
    self.update()
  
  def update(self, newText=None):
    if newText:
      self.text = newText
    
    self.screen.fill((0,0,0))
    self.screen.blit(self.font.render(self.text, True, (255, 255, 255)), (0, 1080 - 50))
    pygame.display.update()
    pygame.event.get()