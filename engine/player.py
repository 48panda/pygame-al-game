import engine.character
import engine.inventory
import engine.items
import pygame

class Player(engine.character.Character):
  def init(self):
    self.inventory = engine.inventory.Inventory([engine.items.WOODEN_PICKAXE], self, self.world.game)
  def render(self):
    self.inventory.render()
  def update(self):
    super().update()
    self.inventory.update()
  def event(self, event):
    if self.inventory.event(event): return True
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_w:
        if self.vy == 0.0:
          self.vy = -2
    return False