import engine.character as character
import random

# NPC that moves from go_left and go_right functions

class NPC(character.Character):
  player = False
  clockcycle = 30
  def __init__(self, *args, pos=(0,0), **kwargs):
    super().__init__(*args, **kwargs)
    self.direction = "still"
    self.time = 10
    self.x = pos[0]
    self.y = pos[1]
    self.last_x = self.x+1
    self.last_y = self.y+1
    self.last_dir = self.direction
    self.time_in_step = 0
    self.speed = 1
  def onupdate(self):
    self.time_in_step += 1
    if self.time <= 0:
      self.direction = "still"
      self.time_in_step = 0

    if self.direction == "left" and not self.out_of_frame:
      self.vx = -0.03 * self.speed
      self.flipped = False
    if self.direction == "right" and not self.out_of_frame:
      self.vx+= 0.03 * self.speed
      self.flipped = True
    super().onupdate()
    if self.direction != "still":
      if self.pos[0] > 0:
        if self.last_x == self.x:
          if self.last_y == self.y:
            if not self.out_of_frame:
              if self.time_in_step > 10:
                self.vy = -2
  
    self.last_x = self.x
    self.last_dir = self.direction
    self.last_y = self.y
  def go_left(self, time, speed):
    self.time = time
    self.direction = "left"
    self.time_in_step = 0
    self.speed = speed
    self.clockcycle = 30 / speed
  
  def go_right(self, time, speed):
    self.time = time
    self.direction = "right"
    self.time_in_step = 0
    self.speed = speed
    self.clockcycle = 30 / speed
  
  def clock_tick(self, time):
    self.time -= time

  def update2(self):
    self.pos = self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly
    self.update(callupdate=False)