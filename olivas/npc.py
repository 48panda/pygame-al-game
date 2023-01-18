import engine.character as character
import random
import pygame
import constants

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
    self.y = self.world.get_surface_level(self.x)
    self.last_x = self.x+1
    self.last_y = self.y+1
    self.last_dir = self.direction
    self.time_in_step = 0

  def onupdate(self):
    self.time -= 1
    self.time_in_step += 1
    if self.time == 0: # If need to change direction
      # Go to home if not close
      if self.x > self.homex + 3:
        self.direction = "left"
        self.flipped = False
      elif self.x < self.homex - 3:
        self.direction = "right"
        self.flipped = True
      else:
        # or pick randomly
        self.direction = random.choice(list(filter(lambda x: x != self.direction, ["left", "right", "still"])))
        # set flipped to make them face the right way
        if self.direction == "left":
          self.flipped = False
        elif self.direction == "right":
          self.flipped = True
      # time to spend in this direction
      self.time = random.randint(50, 300)
      self.time_in_step = 0

    # move
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
              if self.time_in_step > 10: # Bunch of condition to see if they can and need to jump. If they do, jump.
                self.vy = -2
                self.time = max(100, self.time)
    self.last_x = self.x
    self.last_dir = self.direction
    self.last_y = self.y
  def update2(self):
    self.pos = self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly
    self.update(callupdate=False)
  
  def event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        tile_x = self.world.scrollx//16
        tile_y = self.world.scrolly//16
        offset_x = -(self.world.scrollx%16)
        offset_y = -(self.world.scrolly%16)
        blockx, blocky = self.world.game.unzoompoint(*event.pos)
        distance = ((self.world.player.x - self.x)**2 + (self.world.player.y - self.y)**2)**0.5
        if distance > 10:
          return False
        # If player clicks on them
        if self.rect.collidepoint(blockx, blocky):
          has_special = False
          if "special_dialog" in self.npc:
            for dialog in self.npc["special_dialog"]:
              if dialog["year"] == self.world.time and dialog["quest_id"] == self.world.book.quest_id:
                # If they have special dialogue for them play it
                has_special = True
                self.world.book.linearSpeech.add(dialog["interaction"], (255, 255, 255), speaker=self.npc["name"])
                if dialog["completes_quest"]:
                  self.world.book.next_quest()
          if not has_special: # Else play a random greeting
            message = ""
            for i in constants.CHAT_DATA["greeting"]:
              message += random.choice(i)
            self.world.book.linearSpeech.add([message], (255, 255, 255), speaker=self.npc["name"])
            