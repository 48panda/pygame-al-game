import engine.character
import engine.inventory
import engine.items

class Player(engine.character.Character):
  def init(self):
    self.inventory = engine.inventory.Inventory([engine.items.WOODEN_PICKAXE, engine.items.DIRT], self, self.world.game)
  def render(self):
    self.inventory.render()
  def update(self):
    super().update()
    self.inventory.update()
  def event(self, event):
    if self.inventory.event(event): return True
    return False