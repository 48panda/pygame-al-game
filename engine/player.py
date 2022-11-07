import pygame
import karas
import math

PLAYER = pygame.image.load("assets/player/template.png")

class Player(karas.sprite.Sprite):
  bottomLeftAligned = True
  def init(self, world):
    
    self.world = world
    self.x = 0
    self.y = 40
    self.im = PLAYER
    self.vx = 0
    self.vy = 0

  def onupdate(self):
    self.y += self.vy
    if self.world.level[int(self.y)][int(self.x)] == 0:
      self.vy += 0.1
    if self.world.level[int(self.y)][int(self.x)] != 0 and self.vy > 0:
      self.vy = 0
      self.y = int(self.y)
    self.x += self.vx
    if self.world.level[math.ceil(self.y)-1][int(self.x)+1] != 0 and self.vx > 0:
      self.vx = 0
      self.x = int(self.x)
    if self.world.level[math.ceil(self.y)-1][math.ceil(self.x)-1] != 0 and self.vx < 0:
      self.vx = 0
      self.x = math.ceil(self.x)
    self.vx *= 0.7
    self.vy *= 0.7
    self.x = min(len(self.world.level[0]) - 1, max(0, self.x))
    self.pos = self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly