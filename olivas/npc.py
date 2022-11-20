import engine.character as character
import random

class NPC(character.Character):
  player = False
  clockcycle = 30
  def __init__(self, *args, home=None, **kwargs):
    self.homex = home
    super().__init__(*args, **kwargs)
    self.direction = "still"
    self.time = 10
    self.x = self.homex
    self.y = self.world.get_surface_level(self.x, self.world.surface)
  def onupdate(self):
    self.time -= 1
    if self.time == 0:
      if self.x > self.homex + 10:
        self.direction = "left"
        self.flipped = False
      elif self.x < self.homex - 10:
        self.direction = "right"
        self.flipped = True
      else:
        self.direction = random.choice(list(filter(lambda x: x != self.direction, ["left", "right", "still"])))
        if self.direction == "left":
          self.flipped = False
        elif self.direction == "right":
          self.flipped = True

      self.time = random.randint(50, 300)

    if self.direction == "left":
      self.vx = -0.03
    if self.direction == "right":
      self.vx+= 0.03
    super().onupdate()
  def update2(self):
    self.pos = self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly
    self.update(callupdate=False)