import engine.tiles
import random
import math
import numpy as np
import pygame

class World:
  def __init__(self, game, seed):
    self.level = np.array([])
    self.game = game
    self.scrollx = 0
    self.scrolly = 0
    self.width = 200
    self.height = 80
    self.surfacelevel = 40
    self.seed = seed
    self.rects = []

    self.generate_level(seed)
  def generate_level(self, seed):
    random.seed(seed)
    level = np.ones((self.height, self.width))

    surface = ((random.randint(30, 70), random.randint(1, 5)),(random.randint(40, 60), random.randint(2, 6)))

    for x in range(self.width):
      level[:self.get_surface_level(x, surface), x] = 0

    self.level = level
    #self.to_png()

  def get_surface_level(self, x, surface):
    height = self.surfacelevel
    for wave in surface:
      height += round(wave[1] * math.sin(x/wave[0]))
    return height
  
  def to_png(self):
    from PIL import Image
    from matplotlib import cm
    im = Image.fromarray(np.uint8(cm.gist_earth(self.level)*255))
    pygame.quit()
    im.show()
  
  def assign_player(self, player):
    self.player = player

  def render(self):
    self.rects = []
    tile_x = self.scrollx//16
    tile_y = self.scrolly//16
    offset_x = -(self.scrollx%16)
    offset_y = -(self.scrolly%16)
    mouseScaledDown = self.game.unzoompoint(*pygame.mouse.get_pos())
    for x in range(121):
      if x + tile_x < 0:
        continue
      if x + tile_x + 1 >= self.width:
        continue
      for y in range(68):
        tile = self.level[y + tile_y][x + tile_x]
        rect = pygame.Rect(x*16+offset_x, y*16+offset_y, 16, 16)
        if tile == 0:
          continue
        elif tile == 1:
          if y==0 or self.level[y-1 + tile_y][x + tile_x] != 0:
            todraw = engine.tiles.DIRT
          else:
            if x==0 or self.level[y + tile_y][x + tile_x-1] != 0:
              if x==len(self.level[y+tile_y]) or self.level[y + tile_y][x + tile_x+1] != 0:
                todraw = engine.tiles.GRASS
              else:
                todraw = engine.tiles.GRASS_r
            else:
              if x==len(self.level[y+tile_y]) or self.level[y + tile_y][x + tile_x+1] != 0:
                todraw = engine.tiles.GRASS_l
              else:
                todraw = engine.tiles.GRASS_b
        else:
          continue
        self.rects.append(rect)
        self.game.zoom.blit(todraw, (x*16+offset_x, y*16+offset_y))
  
  def update(self, player):
    self.scrollx = -960 + int(player.x * 16)
    self.scrollx = max(0, self.scrollx)
    self.scrollx = min((len(self.level[0]) - 1) * 16 - 1920, self.scrollx)
  
  def event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        tile_x = self.scrollx//16
        tile_y = self.scrolly//16
        offset_x = -(self.scrollx%16)
        offset_y = -(self.scrolly%16)
        blockx, blocky = self.game.unzoompoint(*event.pos)
        clickx = int((blockx - offset_x) // 16 + tile_x)
        clicky = int((blocky - offset_y) // 16 + tile_y)
        if self.player.inventory.get_selected() in engine.items.PICKAXES:
          self.level[clicky][clickx] = 0
          return True
        if self.player.inventory.get_selected() == engine.items.DIRT:
          self.level[clicky][clickx] = 1
          return True
        

