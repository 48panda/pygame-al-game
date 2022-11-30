import engine.character as character
import random

class NPC(character.Character):
  player = False
  clockcycle = 30
  def __init__(self, *args, home=None, npc=None, **kwargs):
    self.homex = home
    self.npc = npc
    super().__init__(*args, **kwargs)
    self.direction = "still"
    self.time = 10
    self.x = self.homex
    self.y = self.world.get_surface_level(self.x, self.world.surface)
    self.last_x = self.x+1
    self.last_y = self.y+1
    self.last_dir = self.direction
    self.time_in_step = 0
  def onupdate(self):
    self.time -= 1
    self.time_in_step += 1
    if self.time == 0:
      if self.x > self.homex + 3:
        self.direction = "left"
        self.flipped = False
      elif self.x < self.homex - 3:
        self.direction = "right"
        self.flipped = True
      else:
        self.direction = random.choice(list(filter(lambda x: x != self.direction, ["left", "right", "still"])))
        if self.direction == "left":
          self.flipped = False
        elif self.direction == "right":
          self.flipped = True
      self.time = random.randint(50, 300)
      self.time_in_step = 0

    if self.direction == "left" and not self.out_of_frame:
      self.vx = -0.03
    if self.direction == "right" and not self.out_of_frame:
      self.vx+= 0.03
    super().onupdate()
    if self.direction != "still":
      if self.pos[0] > 0:
        if self.last_x == self.x:
          if self.last_y == self.y:
            if not self.out_of_frame:
              if self.time_in_step > 10:
                self.vy = -2
                self.time = max(100, self.time)
    self.last_x = self.x
    self.last_dir = self.direction
    self.last_y = self.y
  def update2(self):
    self.pos = self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly
    self.update(callupdate=False)