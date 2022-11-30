import engine.tiles
import random
import math
import pygame
import engine.blocks
import engine.items
import constants
import olivas
import time
import pygame.mixer_music as music

class World:
  def __init__(self, game, seed, loadingScreen, cutscene=False):
    self.loadingScreen = loadingScreen
    self.level = []
    self.game = game
    self.scrollx = 0
    self.scrolly = 0
    self.height = 80
    self.surfacelevel = 40
    self.stonelevel = 50
    self.seed = seed
    self.rects = []
    self.items = pygame.sprite.Group()
    self.time = -1
    self.key_points = [None for i in range (2175)]
    self.cutscene = False

    if not cutscene:
      self.generate_level(seed)

  def assign_npcs(self, npcSprites, npcs, npcSpriteGroup):
    self.npcSprites, self.npcs = npcSprites, npcs
    self.npcSpriteGroup = npcSpriteGroup

  def generate_level(self, seed):
    random.seed(seed)
    self.level = [[engine.blocks.DIRT for _ in range(constants.WORLDWIDTH)] for _ in range(self.height)]

    self.surface = ((temp:=random.randint(30, 70), random.randint(0, temp-1), random.randint(1, 5)),(temp:=random.randint(40, 60), random.randint(0, temp-1), random.randint(2, 6)))
    self.stone = ((temp:=random.randint(30, 70), random.randint(0, temp-1), random.randint(1, 5)),(temp:=random.randint(40, 60), random.randint(0, temp-1), random.randint(2, 6)))

    trees = ((temp:=random.randint(30, 70), random.randint(0, temp-1), 0.5),(temp:=random.randint(40, 60), random.randint(0, temp-1), 0.5))
    landing_site_x = random.randint(20, 50)


    # Fill with stone
    for y in range(self.height):
       for x in range(constants.WORLDWIDTH):
        if self.stonelevel + self.sumsin(x, self.stone) < y:
          self.level[y][x] = engine.blocks.STONE

    # Fill top part with air
    for y in range(self.height):
       for x in range(constants.WORLDWIDTH):
        if self.surfacelevel + self.sumsin(x, self.surface) >= y:
          self.level[y][x] = engine.blocks.AIR
    
    # Add Ship
    landing_site_y = self.get_surface_level(landing_site_x, self.surface)
    self.landing_site_x = landing_site_x
    self.landing_site_y = landing_site_y
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
        self.make_tree(x)
        self.update_neighbours(x, y, drop=False)

    #Bedrock at bottom
    for x in range(constants.WORLDWIDTH):
      self.level[self.height - 1][x] = engine.blocks.BEDROCK
    
    # add the radianite for tutorial
    rad_x = random.randint(10, constants.WORLDWIDTH - 10)
    rel_pos = ((0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2))
    for x, y in rel_pos:
      self.level[self.height-15 + y][x+rad_x] = engine.blocks.RADIANITE

    self.key_points[0] = self.level

    #self.to_png()

  def get_surface_level(self, x, surface=None):
    y = 0
    while not (self.get_at(x, y) in engine.blocks.COLLIDE):
      y += 1
      if y == self.height:
        return y - 1
    return y - 1
  
  def sumsin(self, x, wave):
    height = 0
    for w in wave:
      height += round(w[2] * math.sin((x+w[1])/w[0]))
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

  def render(self):
    self.rects = []
    tile_x = int(self.scrollx//16)
    tile_y = int(self.scrolly//16)
    offset_x = -(self.scrollx%16)
    offset_y = -(self.scrolly%16)
    mouseScaledDown = self.game.unzoompoint(*pygame.mouse.get_pos())
    for x in range(131):
      x -= 10
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
        todraw = engine.blocks.TILE[tile.block]
        if todraw:
          pass
        elif tile == engine.blocks.AIR:
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
        elif tile | engine.blocks.HOUSE0000:

          if y!=0 and self.level[y-1+tile_y][x+tile_x] == tile:
            continue
          if x+tile_x!=0 and self.level[y+tile_y][x+tile_x-1] == tile:
            continue
          if x==-3:
            while self.level[y+tile_y][x+tile_x-1] == tile:
              x -= 1
          if tile.state == 0:
            todraw = engine.buildings.HOUSE0000
          elif tile.state == 1:
            todraw = engine.buildings.HOUSE0450
          elif tile.state == 2:
            todraw = engine.buildings.HOUSE0793
          elif tile.state == 3:
            todraw = engine.buildings.HOUSE1066
          elif tile.state == 4:
            todraw = engine.buildings.HOUSE1485
          elif tile.state == 5:
            todraw = engine.buildings.HOUSE1603
          elif tile.state == 6:
            todraw = engine.buildings.HOUSE1837
          elif tile.state == 7:
            todraw = engine.buildings.HOUSE1902

        elif tile in engine.blocks.USE_BUILDING_RENDERER:
          if y!=0 and self.level[y-1+tile_y][x+tile_x] == tile:
            continue
          if x+tile_x!=0 and self.level[y+tile_y][x+tile_x-1] == tile:
            continue
          if x==-3:
            while self.level[y+tile_y][x+tile_x-1] == tile:
              x -= 1
          todraw = engine.blocks.BUILDING[tile.block]
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
      engine.blocks.UPDATE[self.level[y][x-1].block](state = self.level[y][x-1], neighbours = self.get_neighbours(x-1, y), set_at = self.set_at, x = x-1, y = y, down = self.get_down(x-1, y), drop=drop)
    if x + 1 < constants.WORLDWIDTH:
      engine.blocks.UPDATE[self.level[y][x+1].block](state = self.level[y][x+1], neighbours = self.get_neighbours(x+1, y), set_at = self.set_at, x = x+1, y = y, down = self.get_down(x+1, y), drop=drop)
    if y > 0:
      engine.blocks.UPDATE[self.level[y-1][x].block](state = self.level[y-1][x], neighbours = self.get_neighbours(x, y-1), set_at = self.set_at, x = x, y = y-1, down = self.get_down(x, y-1), drop=drop)
    if y + 1 < self.height:
      engine.blocks.UPDATE[self.level[y+1][x].block](state = self.level[y+1][x], neighbours = self.get_neighbours(x, y+1), set_at = self.set_at, x = x, y = y+1, down = self.get_down(x, y+1), drop=drop)
  
  def randPosNeg(self):
    if random.getrandbits(1): return 1
    return -1

  def get_at(self, x, y):
    try:
      return self.level[y]\
        [x]
    except:
      raise ValueError()

  def set_at(self, x, y, state, drop=False):
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
            if clicky != 0 and self.level[clicky-1][clickx] in engine.blocks.CANT_MINE_BLOCK_BELOW:
              return True
            self.set_at(clickx, clicky, engine.blocks.AIR, drop=True)

            return True
        if self.player.inventory.get_selected() in engine.items.PLACABLE:
          if self.level[clicky][clickx] in engine.blocks.REPLACEABLE:
            self.set_at(clickx, clicky, engine.blocks.PLACE_MAP[self.player.inventory.get_selected()])
            self.player.inventory.removeFromSlot(self.player.inventory.selected)
            return True
        if self.level[clicky][clickx] == engine.blocks.SHIP:
          self.game.keypad.enable()

  def travel(self, dest):
    music.stop()
    music.load("assets/sound/music/startload.mp3")
    music.play(1)
    music.queue("assets/sound/music/loading.mp3", loops=-1)
    self.loadingScreen.update("Saving Time...")

    self.key_points[self.time+1] = self.level

    self.time = int(dest)
    while self.key_points[self.time + 1] == None:
      self.time -= 1
    
    for i in range(self.time+1, len(self.key_points)):
      self.key_points[i] = None

    for y in range(self.time, int(dest)):
      self.loadingScreen.update("Travelating...", timeText=str(y+1))
      self.move_forwards_year()
    
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
        self.npcSpriteGroup.add(olivas.npc.NPC(self, cstring=npc["appearance"], home=npc["home"], npc=npc))
    for i in range(100):
      time.sleep(0.1)
      self.loadingScreen.update("Traveling...")
    music.fadeout(10000)

  def deconstruct_house(self, x, y):
    if self.get_at(x, y) | engine.blocks.HOUSE0000:
      self.set_at(x, y, engine.blocks.AIR)
      self.deconstruct_house(x+1, y)
      self.deconstruct_house(x-1, y)
      self.deconstruct_house(x, y+1)
      self.deconstruct_house(x, y-1)
  
  def upgrade_house(self, x, y, to):
    if self.get_at(x, y) | engine.blocks.HOUSE0000:
      if not self.get_at(x, y) & to:
        self.set_at(x, y, to)
        self.upgrade_house(x+1, y, to)
        self.upgrade_house(x-1, y, to)
        self.upgrade_house(x, y+1, to)
        self.upgrade_house(x, y-1, to)
  
  def make_tree(self, x):
    if not self.landing_site_x <= x <= self.landing_site_x + 3:
      y = self.get_surface_level(x, self.surface)
      if self.get_at(x, y+1) not in engine.blocks.TREEABLE:
        return
      can_place = True
      for test_y in range(0, y):
        if not self.get_at(x, test_y) in engine.blocks.REPLACEABLE:
          can_place = False
          break
      if not can_place:
        return
      is_near_tree = False
      for dx in range(-4, 5):
        if 0 <= (x + dx) < (constants.WORLDWIDTH - 1):
          if self.get_at(dx + x, self.get_surface_level(x, self.surface)-1) | engine.blocks.TREE:
            return
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

  def move_forwards_year(self):
    self.time += 1
    random.seed(str(self.seed)+str(self.time))
    for i, npc in enumerate(self.npcs):
      if npc["died"] == self.time:

        home_x = npc["home"] - 3
        height = []
        for x in range(8):
          height.append(self.get_surface_level(x + home_x, self.surface))
        home_y = max(set(height), key=height.count)

        self.deconstruct_house(home_x, home_y)
      if npc["does_upgrade"]:

        home_x = npc["home"] - 3
        height = []
        for x in range(8):
          height.append(self.get_surface_level(x + home_x, self.surface))
        home_y = max(set(height), key=height.count)
        
        upgrade_year = self.time - npc["upgrade_time"]
        if upgrade_year in engine.blocks.UPGRADE_YEARS:
          self.upgrade_house(home_x, home_y, engine.blocks.UPGRADE_YEARS[upgrade_year])

      if npc["born"] == self.time:

        home_x = npc["home"] - 3
        height = []
        for x in range(8):
          height.append(self.get_surface_level(x + home_x, self.surface))
        home_y = max(set(height), key=height.count)
        
        for x in range(10):
          for y in range(12):
            if self.get_at(x + home_x - 1, y + home_y - 1) | engine.blocks.HOUSE0000:
              self.deconstruct_house(x + home_x - 1, y + home_y - 1)

        temp_time = self.time
        if temp_time > 0:
          while temp_time not in engine.blocks.UPGRADE_YEARS:
            temp_time -= 1
        house = engine.blocks.UPGRADE_YEARS[temp_time]
        for x in range(8):
          for y in range(10):
            self.set_at(x + home_x, home_y - y, house, False)
        
        for x in range(8):
          y = home_y + 1
          x = home_x + x
          while not (self.get_at(x, y) in engine.blocks.COLLIDE):
            self.set_at(x, y, engine.blocks.OBSIDIAN)
            y += 1


    # Try adding a tree
    for _ in range(3):
      x = random.randint(0, constants.WORLDWIDTH - 1)
      self.make_tree(x)
      


