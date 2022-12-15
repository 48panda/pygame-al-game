import pygame

class Checkbox:
  def __init__(self, pos, default, size=10, outline=(0,0,255), fill=(255,255,255), border=2):
    self.state = default
    self.pos = pos
    self.rect = pygame.Rect(self.pos[0], self.pos[1], size, size)
    self.on = pygame.Surface((size,size))
    self.off = pygame.Surface((size,size), pygame.SRCALPHA)
    pygame.draw.rect(self.on, fill, (0,0,size,size))
    pygame.draw.rect(self.on, outline, (0,0,size,size), border)
    pygame.draw.rect(self.off, outline, (0,0,size,size), border)
  
  def event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        if self.rect.collidepoint(event.pos):
          self.state = not self.state
  
  def draw(self):
    if self.state:
      return self.on
    return self.off
  
  def __call__(self):
    return self.state

if __name__ == "__main__":
  screen = pygame.display.set_mode((500,225))
  cBox = Checkbox((100,100),True)
  while True:
    for event in pygame.event.get():
      if cBox.event(event): continue
    if cBox():
      screen.fill((0,255,0))
    else:
      screen.fill((255,0,0))
    screen.blit(cBox.draw(), (100,100))
    pygame.display.update()