import engine.tiles
import random
import math
import pygame
import engine.blocks
import engine.items
import constants
import olivas

class World:
  def __init__(self, game, seed, loadingScreen):
    self.loadingScreen = loadingScreen
    self.level = []
    self.game = game
    self.scrollx = 0
    self.scrolly = 0
    self.height = 80
    self.surfacelevel = 40
    self.seed = seed
    self.rects = []
    self.items = pygame.sprite.Group()
    self.time = -70000000

    self.generate_level(seed)

  def assign_npcs(self, npcSprites, npcs, npcSpriteGroup):
    self.npcSprites, self.npcs = npcSprites, npcs
    self.npcSpriteGroup = npcSpriteGroup

  def generate_level(self, seed):
    random.seed(seed)
    self.level = [[engine.blocks.DIRT for _ in range(constants.WORLDWIDTH)] for _ in range(self.height)]

    self.surface = ((random.randint(30, 70), random.randint(1, 5)),(random.randint(40, 60), random.randint(2, 6)))

    trees = ((random.randint(30, 70), 0.5),(random.randint(40, 60), 0.5))
    landing_site_x = random.randint(50, constants.WORLDWIDTH - 50)

    # Fill top part with air
    for y in range(self.height):
       for x in range(constants.WORLDWIDTH):
        if self.get_surface_level(x, self.surface) >= y:
          self.level[y][x] = engine.blocks.AIR
    
    # Add Ship
    landing_site_y = self.get_surface_level(landing_site_x, self.surface)
    for y in range(3):
      for x in range(4):
        self.level[landing_site_y-y][landing_site_x+x] = engine.blocks.SHIP
    for x in range(4):
      self.level[landing_site_y+1][landing_site_x + x] = engine.blocks.BEDROCK
    
    # Add trees
    most_recent_tree = 0
    for x in range(constants.WORLDWIDTH):
      if most_recent_tree > 0:
        most_recent_tree -= 1
        continue
      if landing_site_x <= x <= landing_site_x + 3: continue
      if (self.sumsin(x, trees) + 1 ) / 2 > random.random() * 4:
        most_recent_tree = 3
        y = self.get_surface_level(x, self.surface)
        theight = random.randint(5, min(max(y // 2, 10), y))
        for i in range(theight):
          self.level[y][x] = engine.blocks.TREE
          y -= 1
        y += 1
        for dy in range(11):
          for dx in range(11):
            if 0 <= x + dx - 5 < constants.WORLDWIDTH:
              if y + dy - 5 >= 0:
                if (dx - 5)**2 + (dy - 5)**2 < 25:
                  if self.level[y + dy - 5][x + dx - 5] in engine.blocks.REPLACEABLE:
                    self.level[y + dy - 5][x + dx - 5] = engine.blocks.LEAVES
        self.update_neighbours(x, y, drop=False)
        

    #Bedrock at bottom
    for x in range(constants.WORLDWIDTH):
      self.level[self.height - 1][x] = engine.blocks.BEDROCK
    
    self.landing_site_x = landing_site_x
    self.landing_site_y = landing_site_y
    #self.to_png()

  def get_surface_level(self, x, surface):
    return self.surfacelevel + self.sumsin(x, surface)
  
  def sumsin(self, x, wave):
    height = 0
    for w in wave:
      height += round(w[1] * math.sin(x/w[0]))
    return height

  def to_png(self):
    from PIL import Image
    from matplotlib import cm
    im = Image.fromarray(np.uint8(cm.gist_earth(self.level)*255))
    pygame.quit()
    im.show()
  
  def assign_player(self, player):
    self.player = player
    self.player.x = self.landing_site_x + 1
    self.player.y = self.landing_site_y + 2

  def assign_text(self, text):
    self.text = text

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
      if x + tile_x + 1 >= constants.WORLDWIDTH:
        continue
      for y in range(69):
        if y + tile_y < 0:
          continue
        if y + tile_y >= self.height:
          continue

        tile = self.level[y + tile_y][x + tile_x]
        rect = pygame.Rect(x*16+offset_x, y*16+offset_y, 16, 16)
        if tile == engine.blocks.AIR:
          continue
        elif tile == engine.blocks.DIRT:
          if y==0 or self.level[y-1 + tile_y][x + tile_x] != engine.blocks.AIR:
            todraw = engine.tiles.DIRT
          else:
            if x==0 or self.level[y + tile_y][x + tile_x-1] != engine.blocks.AIR:
              if x==len(self.level[y+tile_y]) or self.level[y + tile_y][x + tile_x+1] != engine.blocks.AIR:
                todraw = engine.tiles.GRASS
              else:
                todraw = engine.tiles.GRASS_r
            else:
              if x==len(self.level[y+tile_y]) or self.level[y + tile_y][x + tile_x+1] != engine.blocks.AIR:
                todraw = engine.tiles.GRASS_l
              else:
                todraw = engine.tiles.GRASS_b
        elif tile == engine.blocks.SHIP:
          if y!=0 and self.level[y-1+tile_y][x+tile_x] == engine.blocks.SHIP:
            continue
          if x+tile_x!=0 and self.level[y+tile_y][x+tile_x-1] == engine.blocks.SHIP:
            continue
          if x==0:
            while self.level[y+tile_y][x+tile_x-1] == engine.blocks.SHIP:
              x -= 1
          todraw = engine.tiles.SHIP
        elif tile in engine.blocks.USE_TILE_RENDERER:
          todraw = engine.blocks.TILE[tile.block]
        else:
          continue
        if tile in engine.blocks.COLLIDE:
          self.rects.append(rect)
        self.game.zoom.blit(todraw, (x*16+offset_x, y*16+offset_y))
    self.items.draw(self.game.zoom)
  
  def update(self, player=None):
    if not player:
      player = self.player
    self.scrollx = -960 + int(player.x * 16)
    self.scrollx = max(0, self.scrollx)
    self.scrollx = min((constants.WORLDWIDTH - 1) * 16 - 1920, self.scrollx)
    self.scrolly = -540 + int(player.y * 16)
    self.scrolly = max(0, self.scrolly)
    self.scrolly = min((self.height) * 16 - 1080, self.scrolly)
    self.items.update(self.rects)
  
  def get_neighbours(self, x, y):
    n = []
    if x > 0:
      n.append(self.level[y][x-1])
    if x + 1 < constants.WORLDWIDTH:
      n.append(self.level[y][x+1])
    if y > 0:
      n.append(self.level[y-1][x])
    if y + 1 < self.height:
      n.append(self.level[y+1][x])
    return n
  
  def get_down(self, x, y):
    if y + 1 < self.height:
      return self.level[y+1][x]
    return engine.blocks.AIR

  def update_neighbours(self, x, y, drop=False):
    if x > 0:
      engine.blocks.UPDATE[self.level[y][x-1].block](state = self.level[y][x-1], neighbours = self.get_neighbours(x-1, y), changeState = self.changeState, x = x-1, y = y, down = self.get_down(x-1, y), drop=drop)
    if x + 1 < constants.WORLDWIDTH:
      engine.blocks.UPDATE[self.level[y][x+1].block](state = self.level[y][x+1], neighbours = self.get_neighbours(x+1, y), changeState = self.changeState, x = x+1, y = y, down = self.get_down(x+1, y), drop=drop)
    if y > 0:
      engine.blocks.UPDATE[self.level[y-1][x].block](state = self.level[y-1][x], neighbours = self.get_neighbours(x, y-1), changeState = self.changeState, x = x, y = y-1, down = self.get_down(x, y-1), drop=drop)
    if y + 1 < self.height:
      engine.blocks.UPDATE[self.level[y+1][x].block](state = self.level[y+1][x], neighbours = self.get_neighbours(x, y+1), changeState = self.changeState, x = x, y = y+1, down = self.get_down(x, y+1), drop=drop)
  
  def randPosNeg(self):
    if random.getrandbits(1): return 1
    return -1

  def changeState(self, x, y, state, drop=False):
    if drop and (self.level[y][x].block != state.block):
      if engine.blocks.TO_ITEM[self.level[y][x].block] is not None:
        self.items.add(engine.items.InWorldItem(self, (x, y), engine.blocks.TO_ITEM[self.level[y][x].block]))
    self.level[y][x] = state
    self.update_neighbours(x, y, drop=drop)
  
  def tileToScreenPos(self, x, y):
    return [16 * x - self.scrollx, 16 * y - self.scrolly]
  
  def screenToTilePos(self, x, y):
    return [(x + self.scrollx) / 16, (y + self.scrolly) / 16]

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
        distance = ((self.player.x - clickx)**2 + (self.player.y - clicky)**2)**0.5
        if distance > 10:
          return False
        if self.player.inventory.get_selected() in engine.items.PICKAXES:
          if self.level[clicky][clickx] in engine.blocks.MINEABLE_PICKAXE:
            self.changeState(clickx, clicky, engine.blocks.AIR, drop=True)

            return True
        if self.player.inventory.get_selected() in engine.items.PLACABLE:
          if self.level[clicky][clickx] in engine.blocks.REPLACEABLE:
            self.changeState(clickx, clicky, engine.blocks.PLACE_MAP[self.player.inventory.get_selected()])
            self.player.inventory.removeFromSlot(self.player.inventory.selected)
            return True
        if self.level[clicky][clickx] == engine.blocks.SHIP:
          self.game.keypad.enable()

  def travel(self, dest):
    self.time = int(dest)
    self.npcSpriteGroup.empty()
    total = 0
    for i, npc in enumerate(self.npcs):
      if npc["born"] <= self.time < npc["died"]:
        total += 1
    current = 0
    for i, npc in enumerate(self.npcs):
      if npc["born"] <= self.time < npc["died"]:
        current += 1
        self.loadingScreen.update(f"Generating NPCs... {current}/{total}")
        self.npcSpriteGroup.add(olivas.npc.NPC(self, cstring=npc["appearance"], home=npc["home"]))
    self.text.reset(dest)
