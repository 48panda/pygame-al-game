import engine.character
import engine.inventory
import engine.items
import pygame

class Player(engine.character.Character):
  def init(self):
    self.inventory = engine.inventory.Inventory([engine.items.WOODEN_PICKAXE, engine.items.DIRT], self, self.world.game)
  def render(self):
    self.inventory.render()
  def update(self):
    super().update()
    self.inventory.update()
  def event(self, event):
    print("Hi!")
    if self.inventory.event(event): return True
    print("Hi", event)
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_w:
        print(self.vy)
        if self.vy == 0.0:
          print(self.vy)  
          self.vy = -2
          print(self.vy)  
    return False