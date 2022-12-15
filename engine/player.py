import engine.character
import engine.inventory
import engine.items
import pygame

class Player(engine.character.Character):
  player = True
  def init(self, hasBeenLoaded=False):
    if not hasBeenLoaded:
      self.inventory = engine.inventory.Inventory([[engine.items.WOODEN_PICKAXE, 1], [engine.items.OBSIDIAN, 16]], self, self.world.game)
    else:
      self.inventory.__init__([[engine.items.WOODEN_PICKAXE, 1], [engine.items.OBSIDIAN, 16]], self, self.world.game, hasBeenLoaded=True)
    self.left = False
    self.right = False
  def render(self):
    self.inventory.render()
  def onupdate(self):
    if self.left:
      self.vx -= 0.15
      self.flipped = False
    if self.right:
      self.vx += 0.15
      self.flipped = True
    super().onupdate()
    self.inventory.update()
  
  def __getstate__(self):
    #print("write", (1, self.inventory, self.cstring, self.x, self.y, "test"))
    return (1, self.inventory, self.cstring, self.x, self.y)
  
  def __setstate__(self, state):
    if state[0] == 1:
      _, self.inventory, self.cstring, self.x, self.y = state
      #print("read", state)

  def event(self, event):
    if self.inventory.event(event): return True
    if event.type == pygame.KEYDOWN:
      if event.key in [pygame.K_w, pygame.K_SPACE]:
        if self.vy == 0.0:
          self.vy = -2
          return True
      if event.key == pygame.K_a:
        self.left = True
        return True
      if event.key == pygame.K_d:
        self.right = True
        return True
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_a:
        self.left = False
        return True
      if event.key == pygame.K_d:
        self.right = False
        return True
    return False
def postupdate(self):
  self.world.game.zoompos = self.rect.center