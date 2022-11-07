import engine.tiles

class World:
  def __init__(self, game):
    self.level = [[0] * 200] * 40 + [[1,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1] * 16] + [[1] * 200] * 30
    self.game = game
    self.scrollx = 0
    self.scrolly = 0

  def render(self):
    tile_x = self.scrollx//16
    tile_y = self.scrolly//16
    offset_x = -(self.scrollx%16)
    offset_y = -(self.scrolly%16)
    for x in range(121):
      if x + tile_x < 0:
        continue
      if x + tile_x >= len(self.level[0]):
        continue
      for y in range(68):
        tile = self.level[y + tile_y][x + tile_x]
        if tile == 0:
          continue
        if tile == 1:
          if y==0 or self.level[y-1 + tile_y][x + tile_x]:
            todraw = engine.tiles.DIRT
          else:
            todraw = engine.tiles.GRASS
        else:
          continue
        self.game.game.blit(todraw, (x*16+offset_x, y*16+offset_y))
  
  def update(self, player):
    self.scrollx = -960 + int(player.x * 16)
    self.scrollx = max(0, self.scrollx)
    self.scrollx = min(len(self.level[0]) * 16 - 1920, self.scrollx)
    #self.scrolly = 0 - player.y
