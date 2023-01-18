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
import copy
import mono

class World:
  # Class that does everything related to the world.
  def __init__(self, game, seed, loadingScreen, clock, cutscene=False, hasBeenLoaded=False):
    self.loadingScreen = loadingScreen
    self.game = game
    self.clock = clock
    self.height = 80
    self.surfacelevel = 40
    self.stonelevel = 50
    self.seed = seed
    self.rects = []
    self.items = pygame.sprite.Group()
    self.cutscene = cutscene
    self.skipRenderFrame = False
    if not hasBeenLoaded:
      # Stuff that is saved if needed
      self.level = []
      self.time = -1
      self.scrollx = 0
      # The state of the world in each visited year (not every year, too much memory)
      self.key_points = [None for i in range (2175)]
      self.scrolly = 0
      self.book = None

    if not cutscene and not hasBeenLoaded:
      # Do generation of world
      self.generate_level(seed)
  
  def __getstate__(self):
    # save from file
    return (1, self.time, self.key_points, self.level, self.scrollx, self.scrolly, self.book, self.player, self.npcs, self.landing_site_x, self.landing_site_y)
  
  def __setstate__(self, state):
    # load from file
    if state[0] == 1:
      _, self.time, self.key_points, self.level, self.scrollx, self.scrolly, self.book, self.player, self.npcs, self.landing_site_x, self.landing_site_y = state
  
  # Set attributes based off of things which require world to be initialised
  def assign_book(self, book):
    self.book = book

  def assign_npcs(self, npcSprites, npcs, npcSpriteGroup):
    self.npcSprites, self.npcs = npcSprites, npcs
    self.npcSpriteGroup = npcSpriteGroup

  def generate_level(self, seed):
    random.seed(seed) # seed

    # create random sin waves
    self.level = [[engine.blocks.DIRT for _ in range(constants.WORLDWIDTH)] for _ in range(self.height)]

    self.surface = ((temp:=random.randint(30, 70), random.randint(0, temp-1), random.randint(1, 5)),(temp:=random.randint(40, 60), random.randint(0, temp-1), random.randint(2, 6)))
    self.stone = ((temp:=random.randint(30, 70), random.randint(0, temp-1), random.randint(1, 5)),(temp:=random.randint(40, 60), random.randint(0, temp-1), random.randint(2, 6)))
    sand = ((temp:=random.randint(30, 50), random.randint(0, temp-1), sandlevel:=random.randint(80, 100)),(temp:=random.uniform(1, 5), random.randint(0, int(temp-1)), random.randint(3, 5)))

    trees = ((temp:=random.randint(30, 70), random.randint(0, temp-1), 0.5),(temp:=random.randint(40, 60), random.randint(0, temp-1), 0.5))
    landing_site_x = random.randint(20, 50)


    # Fill with stone
    for y in range(self.height):
       for x in range(constants.WORLDWIDTH):
        if self.stonelevel + self.sumsin(x, self.stone) < y:
          self.level[y][x] = engine.blocks.STONE

    # Fill with sand
    for y in range(self.height):
       for x in range(constants.WORLDWIDTH):
        if 50-sandlevel + self.sumsin(x, sand) >= y:
          self.level[y][x] = engine.blocks.SAND
  
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

    self.key_points[0] = copy.deepcopy(self.level)

  def get_surface_level(self, x, surface=None):
    # note: surface= still here as some places still use it. It used to be what is now sumsin.
    y = 0
    while not (self.get_at(x, y) in engine.blocks.COLLIDE):
      y += 1
      # Find highest collidable block
      if y == self.height:
        return y - 1
    return y - 1
  
  def sumsin(self, x, wave):
    height = 0
    for w in wave:
      height += round(w[2] * math.sin((x+w[1])/w[0]))
    return height
  
  def assign_player(self, player):
    self.player = player
    # set player start pos
    self.player.x = self.landing_site_x + 1
    self.player.y = self.landing_site_y + 2

  def render(self):
    self.rects = []
    # Get divmod of scroll
    tile_x = int(self.scrollx//16)
    tile_y = int(self.scrolly//16)
    offset_x = -(self.scrollx%16)
    offset_y = -(self.scrolly%16)

    for x in range(131): # Do a few more x than we need just in case.
      x -= 10
      # skip out of bounds
      if x + tile_x < 0:
        continue
      if x + tile_x + 1 >= constants.WORLDWIDTH:
        continue
      for y in range(69):
        # skip out of bounds
        if y + tile_y < 0:
          continue
        if y + tile_y >= self.height:
          continue
        
        # get block
        tile = self.level[y + tile_y][x + tile_x]
        rect = pygame.Rect(x*16+offset_x, y*16+offset_y, 16, 16)
        todraw = engine.blocks.TILE[tile.block]
        area = None
        if todraw: # should draw?
          if tile | engine.blocks.PLANKS:
            # planks use this formula to provide texture variety
            area = (0,16*((y + tile_y + math.floor(4*math.sin(100*math.floor(x+tile_x)))) % 4),16,16)
        elif tile | engine.blocks.AIR:
          # don't render air
          continue
        elif tile | engine.blocks.DIRT:
          # Work out which dirt sprite
          if y==0 or self.level[y-1 + tile_y][x + tile_x] ^ engine.blocks.AIR:
            todraw = engine.tiles.DIRT
          else:
            if x==0 or self.level[y + tile_y][x + tile_x-1] ^ engine.blocks.AIR:
              if x==len(self.level[y+tile_y]) or self.level[y + tile_y][x + tile_x+1] ^ engine.blocks.AIR:
                todraw = engine.tiles.GRASS
              else:   
                todraw = engine.tiles.GRASS_r
            else:
              if x==len(self.level[y+tile_y]) or self.level[y + tile_y][x + tile_x+1] ^ engine.blocks.AIR:
                todraw = engine.tiles.GRASS_l
              else:
                todraw = engine.tiles.GRASS_b

        elif tile | engine.blocks.HOUSE0000:
          # Render houses (see block renderer for explanation -- just can't use it as blockstate changes texture)
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
        # Building renderer
        elif tile in engine.blocks.USE_BUILDING_RENDERER:
          # if not bottom left, don't render
          if y!=0 and self.level[y-1+tile_y][x+tile_x] == tile:
            continue
          if x+tile_x!=0 and self.level[y+tile_y][x+tile_x-1] == tile:
            continue
          if x==-3: # if x is at boundry on left, find where it should be rendered
            while self.level[y+tile_y][x+tile_x-1] == tile:
              x -= 1
          todraw = engine.blocks.BUILDING[tile.block]
        else:
          continue
        if tile in engine.blocks.COLLIDE: # Create hitboxes
          self.rects.append(rect)
        self.game.zoom.blit(todraw, (x*16+offset_x, y*16+offset_y), area=area)
    self.items.draw(self.game.zoom)
  
  def update(self, player=None):
    if not player:
      player = self.player
    # set scroll to center on player if player is not near border else go as close as can
    self.scrollx = -960 + int(player.x * 16)
    self.scrollx = max(0, self.scrollx)
    self.scrollx = min((constants.WORLDWIDTH - 1) * 16 - 1920, self.scrollx)
    self.scrolly = -540 + int(player.y * 16)
    self.scrolly = max(0, self.scrolly)
    self.scrolly = min((self.height) * 16 - 1080, self.scrolly)
    self.items.update(self.rects)
  
  def get_neighbours(self, x, y):
    # get neighbours of block
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
    # get block below
    if y + 1 < self.height:
      return self.level[y+1][x]
    return engine.blocks.AIR

  def update_neighbours(self, x, y, drop=False):
    # update all neighbous of block if they are in bounds
    if x > 0:
      engine.blocks.UPDATE[self.level[y][x-1].block](state = self.level[y][x-1], neighbours = self.get_neighbours(x-1, y), set_at = self.set_at, x = x-1, y = y, down = self.get_down(x-1, y), drop=drop)
    if x + 1 < constants.WORLDWIDTH:
      engine.blocks.UPDATE[self.level[y][x+1].block](state = self.level[y][x+1], neighbours = self.get_neighbours(x+1, y), set_at = self.set_at, x = x+1, y = y, down = self.get_down(x+1, y), drop=drop)
    if y > 0:
      engine.blocks.UPDATE[self.level[y-1][x].block](state = self.level[y-1][x], neighbours = self.get_neighbours(x, y-1), set_at = self.set_at, x = x, y = y-1, down = self.get_down(x, y-1), drop=drop)
    if y + 1 < self.height:
      engine.blocks.UPDATE[self.level[y+1][x].block](state = self.level[y+1][x], neighbours = self.get_neighbours(x, y+1), set_at = self.set_at, x = x, y = y+1, down = self.get_down(x, y+1), drop=drop)
  
  def randPosNeg(self):
    # randomly return 1 or -1
    if random.getrandbits(1): return 1
    return -1

  def get_at(self, x, y):
    try:
      return self.level[y][x]
    except:
      raise ValueError()

  def set_at(self, x, y, state, drop=False):
    # set block at location
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
        # get clicked block
        tile_x = self.scrollx//16
        tile_y = self.scrolly//16
        offset_x = -(self.scrollx%16)
        offset_y = -(self.scrolly%16)
        blockx, blocky = self.game.unzoompoint(*event.pos)
        clickx = int((blockx - offset_x) // 16 + tile_x)
        clicky = int((blocky - offset_y) // 16 + tile_y)
        #get distance
        distance = ((self.player.x - clickx)**2 + (self.player.y - clicky)**2)**0.5
        if distance > 10: # if not in range
          return False
        # if pickaxe and clicked on mineable block, mine.
        if self.player.inventory.get_selected() in engine.items.PICKAXES:
          if self.level[clicky][clickx] in engine.blocks.MINEABLE_PICKAXE:
            if clicky != 0 and self.level[clicky-1][clickx] in engine.blocks.CANT_MINE_BLOCK_BELOW:
              return True
            self.set_at(clickx, clicky, engine.blocks.AIR, drop=True)

            return True
        # if placeable and clicked on overwritable block, place.
        if self.player.inventory.get_selected() in engine.items.PLACABLE:
          if self.level[clicky][clickx] in engine.blocks.REPLACEABLE:
            self.set_at(clickx, clicky, engine.blocks.PLACE_MAP[self.player.inventory.get_selected()])
            self.player.inventory.removeFromSlot(self.player.inventory.selected)
            return True
        # If ship clicked, open time travel menu.
        if self.level[clicky][clickx] | engine.blocks.SHIP:
          if self.book.quest_id.startswith("tutorial"):
            if self.book.quest_id == "tutorial-3":
              # automatic for first use
              self.travel("-2")
              self.book.next_quest()
          else:
            self.game.keypad.enable()

  def get_copy(self):
    # copy the level to store it
    return [[cell for cell in r] for r in self.level]
  
  def load_npcs(self):
    self.npcSpriteGroup.empty()
    # Get number of NPCs that will be spawned
    # Just for text on load? seems inefficient.
    total = 0
    for i, npc in enumerate(self.npcs):
      if npc["born"] <= self.time < npc["died"]:
        total += 1
      elif "special_appearences" in npc:
        for i in npc["special_appearences"]:
          if i["year"] == self.time and i["quest_id"] == self.book.quest_id:
            total += 1
            break
    current = 0
    # Load NPC sprites and generate character textures
    for i, npc in enumerate(self.npcs):
      if npc["born"] <= self.time < npc["died"]:
        current += 1
        self.loadingScreen.update(f"Generating NPCs... {current}/{total}")
        self.npcSpriteGroup.add(olivas.npc.NPC(self, cstring=npc["appearance"], home=npc["home"], npc=npc))
      elif "special_appearences" in npc:
        for i in npc["special_appearences"]:
          if i["year"] == self.time and i["quest_id"] == self.book.quest_id:
            current += 1
            self.loadingScreen.update(f"Generating NPCs... {current}/{total}")
            self.npcSpriteGroup.add(olivas.npc.NPC(self, cstring=npc["appearance"], home=npc["home"], npc=npc))
            break

  def travel(self, dest):
    # music
    mono.no_music()
    music.load("assets/sound/music/startload.mp3")
    music.play(1)
    music.queue("assets/sound/music/loading.mp3", loops=-1)
    self.loadingScreen.update("Saving Time...")
    # save copy of this time
    self.key_points[self.time+2] = self.get_copy()

    self.time = int(dest)
    # find nearest key point to destination
    while self.key_points[self.time + 2] == None:
      self.time -= 1
    # load that time
    self.level = copy.deepcopy(self.key_points[self.time + 2])
    # work to time wanted
    for i in range(self.time+3, len(self.key_points)):
      self.key_points[i] = None
    for y in range(self.time, int(dest)):
      if y % 3 == 0: # mod 3 because it is coprime with 10 so all last digits are displayed to get the effect of it being really fast
        self.loadingScreen.update("Travelating...", timeText=str(y))
      # simulate year
      self.move_forwards_year()
      # Store a key point every 100 years.
      # why? example:
      # player goes to 2021 in a new save.
      # player then goes to 2020.
      # Intead of calculating all 2000 years again it only has to do 20.
      if self.time % 100 == 0:
        self.key_points[self.time+2] = self.get_copy()
    if int(dest) > 0:
      self.loadingScreen.update("Travelating...", timeText=dest)
    
    
    self.load_npcs()
    # This happens at a time when if the next frame was rendered it would be the old world still.
    self.skipRenderFrame = True

    for i in range(20): # delay for short travels
      time.sleep(0.1)
      self.loadingScreen.update("Traveling...")
    music.fadeout(10000)
    self.clock.tick(30)
    mono.yes_music()

  # destroy a whole house from a single tile coordinate
  def deconstruct_house(self, x, y):
    if self.get_at(x, y) | engine.blocks.HOUSE0000:
      self.set_at(x, y, engine.blocks.AIR)
      self.deconstruct_house(x+1, y)
      self.deconstruct_house(x-1, y)
      self.deconstruct_house(x, y+1)
      self.deconstruct_house(x, y-1)
  # upgrade a whole house from a single tile coordinate
  def upgrade_house(self, x, y, to):
    if self.get_at(x, y) | engine.blocks.HOUSE0000:
      if not self.get_at(x, y) & to:
        self.set_at(x, y, to)
        self.upgrade_house(x+1, y, to)
        self.upgrade_house(x-1, y, to)
        self.upgrade_house(x, y+1, to)
        self.upgrade_house(x, y-1, to)
  # plant a tree. #teamtrees
  def make_tree(self, x):
    # don't plant over ship. (probably not needed with TREEABLE but just to be safe)
    if not self.landing_site_x <= x <= self.landing_site_x + 3:
      y = self.get_surface_level(x) # get tree y height
      if self.get_at(x, y+1) not in engine.blocks.TREEABLE:
        return
      can_place = True
      # check all the blocks are valid
      for test_y in range(0, y):
        if not self.get_at(x, test_y) in engine.blocks.REPLACEABLE:
          can_place = False
          break
      if not can_place:
        return
      # don't plant too close to another tree
      for dx in range(-4, 5):
        if 0 <= (x + dx) < (constants.WORLDWIDTH - 1):
          if self.get_at(dx + x, self.get_surface_level(x)-1) | engine.blocks.TREE:
            return
      # randomly set height. maybe make them smaller on average?
      theight = random.randint(5, min(max(y // 2, 10), y))
      # make the tree
      for i in range(theight):
        self.level[y][x] = engine.blocks.TREE
        y -= 1
      y += 1
      # make leaves
      for dy in range(11):
        for dx in range(11):
          if 0 <= x + dx - 5 < constants.WORLDWIDTH:
            if y + dy - 5 >= 0:
              if (dx - 5)**2 + (dy - 5)**2 < 25:
                if self.level[y + dy - 5][x + dx - 5] in engine.blocks.REPLACEABLE:
                  self.level[y + dy - 5][x + dx - 5] = engine.blocks.LEAVES
      self.update_neighbours(x, y, drop=False) # set leave distance values correctly

  def move_forwards_year(self):
    self.time += 1 # add one to time
    random.seed(str(self.seed)+str(self.time)) # make it deterministic
    for i, npc in enumerate(self.npcs):
      if npc["died"] == self.time: # npc has died. ):

        home_x = npc["home"] - 3
        height = []
        for x in range(8):
          height.append(self.get_surface_level(x + home_x))
        home_y = max(set(height), key=height.count)

        # The second they die we blow up their house
        self.deconstruct_house(home_x, home_y)
      if npc["does_upgrade"]:
        # If the npc is the upgrading type
        home_x = npc["home"] - 3
        height = []
        for x in range(8):
          height.append(self.get_surface_level(x + home_x))
        home_y = max(set(height), key=height.count)
        
        upgrade_year = self.time - npc["upgrade_time"]
        if upgrade_year in engine.blocks.UPGRADE_YEARS:
          self.upgrade_house(home_x, home_y, engine.blocks.UPGRADE_YEARS[upgrade_year])

      if npc["born"] == self.time: # An NPC is born (: They are an adult already somehow though

        home_x = npc["home"] - 3
        height = []
        # decide height for house
        for x in range(8):
          height.append(self.get_surface_level(x + home_x))
        home_y = max(set(height), key=height.count)

        # Find most recent house type and build it for them
        temp_time = self.time
        if temp_time > 0:
          while temp_time not in engine.blocks.UPGRADE_YEARS:
            temp_time -= 1
        house = engine.blocks.UPGRADE_YEARS[temp_time]
        for x in range(8):
          for y in range(10):
            self.set_at(x + home_x, home_y - y, house, False)
        # Build obsisian to support house where needed
        for x in range(8):
          y = home_y + 1
          x = home_x + x
          while not (self.get_at(x, y) in engine.blocks.COLLIDE):
            self.set_at(x, y, engine.blocks.OBSIDIAN)
            y += 1


    # Try adding a tree. Well, 3 trees.
    for _ in range(3):
      x = random.randint(0, constants.WORLDWIDTH - 1)
      self.make_tree(x)
      


