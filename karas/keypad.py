import pygame

CIRCLE = pygame.image.load("assets/gui/circle.png").convert_alpha()
FILLEDCIRCLE = pygame.image.load("assets/gui/filledcircle.png").convert_alpha()
GREENCIRCLE = pygame.image.load("assets/gui/greencircle.png").convert_alpha()
FILLEDGREENCIRCLE = pygame.image.load("assets/gui/filledgreencircle.png").convert_alpha()
REDCIRCLE = pygame.image.load("assets/gui/redcircle.png").convert_alpha()
FILLEDREDCIRCLE = pygame.image.load("assets/gui/filledredcircle.png").convert_alpha()

class Keypad:
  def __init__(self, surface):
    self.game = surface
    self.enabled = False
    self.width = 160
    self.height = 250
    self.font = pygame.font.SysFont("Calibri", 30) 
    self.keys = [CIRCLE.copy() for _ in range(10)]
    self.hover_keys = [FILLEDCIRCLE.copy() for _ in range(10)]
    self.cancel_pos = (0,0)
    self.go_pos = (0,0)
    self.pos = []
    self.dest = ""
    for i in range(10):
      text = self.font.render(str(i), True, (0, 141, 163))
      r = text.get_rect()
      r.center = (20, 20)
      self.keys[i].blit(text, r)
      self.hover_keys[i].blit(text, r)
  
  def enable(self):
    self.enabled = True

  def disable(self):
    self.enabled = False
  
  def if_button(self, pos):
    return self.if_near(pos,pygame.mouse.get_pos(), 20)
  def if_near(self, pos, pos2, dist):
    return ((pos[0]-pos2[0])**2 + (pos[1]-pos2[1])**2) <= dist**2

  def draw(self):
    if self.enabled:
      r = pygame.Rect(0, 0, self.width, self.height)
      r.center = self.game.get_rect().center
      pygame.draw.rect(self.game, (0, 57, 66), r)
      pygame.draw.rect(self.game, (0, 194, 224), r, width = 2)
      self.pos = [(r.centerx, r.bottom - 30)]
      for y in range(3):
        for x in range(3):
          self.pos.append(((r.left + 30 + 50*x), (r.bottom - 50 + 20 - 50*(3-y))))
          if (((r.left + 30 + 50*x)-pygame.mouse.get_pos()[0])**2 + ((r.bottom - 50 + 20 - 50*(3-y))-pygame.mouse.get_pos()[1])**2) <= 400:
            self.game.blit(self.hover_keys[1 + x + 3*y], (r.left + 10 + 50*x, r.bottom - 50 - 50*(3-y)))
          else:
            self.game.blit(self.keys[1 + x + 3*y], (r.left + 10 + 50*x, r.bottom -50 - 50*(3-y)))
      if (((r.centerx)-pygame.mouse.get_pos()[0])**2 + ((r.bottom - 30)-pygame.mouse.get_pos()[1])**2) <= 400:
        self.game.blit(self.hover_keys[0], (r.centerx - 20, r.bottom - 50))
      else:
        self.game.blit(self.keys[0], (r.centerx - 20, r.bottom - 50))
      self.go_pos = (r.centerx - 20 + 70, r.bottom - 30)
      self.cancel_pos = (r.centerx - 20 - 30, r.bottom - 30)
      if self.if_button(self.go_pos):
        self.game.blit(FILLEDGREENCIRCLE, (self.go_pos[0]-20,self.go_pos[1]-20))
      else:
        self.game.blit(GREENCIRCLE, (self.go_pos[0]-20,self.go_pos[1]-20))
      if self.if_button(self.cancel_pos):
        self.game.blit(FILLEDREDCIRCLE, (self.cancel_pos[0]-20,self.cancel_pos[1]-20))
      else:
        self.game.blit(REDCIRCLE, (self.cancel_pos[0]-20,self.cancel_pos[1]-20))
      
      if self.dest:
        if 0 < int(self.dest) < 2150:
          text = self.font.render(self.dest, True, (0, 224, 45))
        else:
          text = self.font.render(self.dest, True, (224, 0, 0))
        tr = text.get_rect()
        tr.midtop = r.midtop
        tr.top += 5
        self.game.blit(text, tr)

  def event(self, event):
    if self.enabled:
      if event.type == pygame.MOUSEBUTTONDOWN:
        for b in range(10):
          if self.if_near(self.pos[b],event.pos, 20):
            self.dest += str(b)
            if len(self.dest) >= 4:
              self.dest = self.dest[-4:]
            return True
        if self.if_near(self.cancel_pos,event.pos, 20):
          self.dest = ""
          return True
        if self.if_near(self.go_pos, event.pos, 20):
          if 0 < int(self.dest) < 2150:
            self.disable()
            self.world.travel(self.dest)
          return True
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.dest = ""
          self.disable()
          return True