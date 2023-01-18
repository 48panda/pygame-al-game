import pygame
import engine.items
import engine.crafting

# A bunch of enums related to sprite positioning
SLOT_SIZE = 45
PADDED_SLOT_SIZE = 50
SLOT_POSITIONS = [(1920//2-(5-i)*PADDED_SLOT_SIZE,1080-PADDED_SLOT_SIZE) for i in range(10)]
SLOT_POSITIONS_CENTER = [(1920//2-(5-i)*PADDED_SLOT_SIZE + SLOT_SIZE/2,1080-PADDED_SLOT_SIZE + SLOT_SIZE/2) for i in range(10)]
SLOT_RECTS = [pygame.Rect(pos[0], pos[1], SLOT_SIZE, SLOT_SIZE) for pos in SLOT_POSITIONS]

INV_POSITIONS = sum([[(i[0], i[1] - PADDED_SLOT_SIZE * h) for i in SLOT_POSITIONS] for h in range(1,4)], [])
INV_POSITIONS_CENTER = sum([[(i[0], i[1] - PADDED_SLOT_SIZE * h) for i in SLOT_POSITIONS_CENTER] for h in range(1,4)], [])
INV_RECTS = [pygame.Rect(pos[0], pos[1], SLOT_SIZE, SLOT_SIZE) for pos in INV_POSITIONS]

CRAFT_POS = [(1920//2-(-6-i)*PADDED_SLOT_SIZE,1080-PADDED_SLOT_SIZE) for i in range(10)]
CRAFT_POS_C = [(1920//2-(-6-i)*PADDED_SLOT_SIZE + SLOT_SIZE/2,1080-PADDED_SLOT_SIZE + SLOT_SIZE/2) for i in range(10)]
CRAFTING_POSITIONS = sum([[(i[0], i[1] - PADDED_SLOT_SIZE * h) for i in CRAFT_POS] for h in range(4)], [])
CRAFTING_POSITIONS_CENTER = sum([[(i[0], i[1] - PADDED_SLOT_SIZE * h) for i in CRAFT_POS_C] for h in range(4)], [])
CRAFTING_RECTS = [pygame.Rect(pos[0], pos[1], SLOT_SIZE, SLOT_SIZE) for pos in CRAFTING_POSITIONS]
CRAFTING_RECTS_TALL = [pygame.Rect(pos[0], pos[1] -  PADDED_SLOT_SIZE*3, SLOT_SIZE, SLOT_SIZE + PADDED_SLOT_SIZE*3) for pos in CRAFT_POS]

# Load slot textures
SLOT = pygame.image.load("assets/gui/slot.png").convert_alpha()
SELECTED = pygame.image.load("assets/gui/selectedslot.png").convert_alpha()
SWAP = pygame.image.load("assets/gui/swapslot.png").convert_alpha()

# Initiate font
FONT = pygame.font.SysFont("Calibri", 20, bold=True)
TOOLTIP_FONT = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 24, bold=True)

class Inventory:
  def __init__(self, items, player, game ,hasBeenLoaded=False):
    if not hasBeenLoaded:
      self.items = items + [[0,0] for _ in range(40-len(items))]
      # Items is already loaded if loading from file
    # Initialise attributes
    self.player = player
    self.game = game
    self.hotbar_sprites = [engine.items.Item(SLOT_POSITIONS_CENTER[i]) for i in range(10)]
    self.hotbar_group = pygame.sprite.Group(self.hotbar_sprites)
    self.inventory_sprites = [engine.items.Item(INV_POSITIONS_CENTER[i]) for i in range(30)]
    self.inventory_group = pygame.sprite.Group(self.inventory_sprites)
    self.crafting_sprites = [engine.items.Item(CRAFTING_POSITIONS_CENTER[i]) for i in range(40)]
    self.crafting_group = pygame.sprite.Group(self.crafting_sprites)
    self.selected = 0
    self.player_sprite = engine.items.Item(self.player.rect.center)
    self.player_sprite_group = pygame.sprite.GroupSingle(self.player_sprite)
    self.showall = False
    self.swap = -1
    self.recipes = []
    # Update sprites so they have a position and the rendering of them doesn't crash.
    for i in self.hotbar_sprites:
      i.setSprite(0)
      i.update()
    for i in self.inventory_sprites:
      i.setSprite(0)
      i.update()
    for i in self.crafting_sprites:
      i.setSprite(0)
      i.update()
    self.update_craftable()
  
  def __getstate__(self):
    # For saving to file
    return (1, self.items)
  
  def __setstate__(self, state):
    # Loading from file
    if state[0] == 1:
      _, self.items = state

  def get_slot(self, slot):
    return self.items[slot][0]
  
  def has(self, item, count=1):
    # does player have count items?
    for i in self.items:
      if i[0] == item:
        return i[1] >= count
    return False

  def num(self, item):
    # Get number of items player has of type
    for i in self.items:
      if i[0] == item:
        return i[1]
    return 0
    
  def give(self, item, num=1, reloadRecipes=True):
    # Give player num items
    for i in range(len(self.items)):
      if self.items[i][0] == item:
        self.items[i][1] += num
        if reloadRecipes:
          self.update_craftable()
        return
    for i in range(len(self.items)):
      if self.items[i][0] == 0:
        self.items[i][0] = item
        self.items[i][1] = num
        if reloadRecipes:
          self.update_craftable()
        return
  def remove(self, item, num=1, reloadRecipes=True):
    # Take num items
    for i in range(len(self.items)):
      if self.items[i][0] == item:
        self.items[i][1] -= num
        if self.items[i][1] <= 0:
          self.items[i] = [0,0]
        if reloadRecipes:
          self.update_craftable()
        return
      
  
  def removeFromSlot(self, slot):
    # Take away an item from a specific slot
    self.items[slot][1] -= 1
    if self.items[slot][1] <= 0:
      self.items[slot][0] = 0
    self.update_craftable()


  def render(self):
    # Rendering. This is a mess Feel free to skip to line
    if self.showall: # If user has pressed E

      # Hotbar
      for i, pos in enumerate(SLOT_POSITIONS):
        # If slot should be green paint it green
        if i == self.swap:
          self.game.nozoom.blit(SWAP, pos)
        else:
          self.game.nozoom.blit(SLOT, pos)
      # Draw hotbar items
      self.hotbar_group.draw(self.game.nozoom)

      for i, pos in enumerate(SLOT_POSITIONS_CENTER):
        # quantities
        if self.items[i][0] != 0:
          if i == self.swap:
            c = (0, 0, 0)
          else:
            c = (255, 255, 255)
          tx, ty = pos
          text = FONT.render(str(self.items[i][1]), True, c)
          self.game.nozoom.blit(text, (tx+20-text.get_width(), ty))

      # Main Inventory
      for i, pos in enumerate(INV_POSITIONS):
        i = i + 10
        # If slot should be green paint it green
        if i == self.swap:
          self.game.nozoom.blit(SWAP, pos)
        else:
          self.game.nozoom.blit(SLOT, pos)
      # Draw items
      self.inventory_group.draw(self.game.nozoom)
      for i, pos in enumerate(INV_POSITIONS_CENTER):
        # Draw quantities
        i = i + 10
        if self.items[i][0] != 0:
          if i == self.swap:
            c = (0, 0, 0)
          else:
            c = (255, 255, 255)
          tx, ty = pos
          text = FONT.render(str(self.items[i][1]), True, c)
          self.game.nozoom.blit(text, (tx+20-text.get_width(), ty))

      # Draw crafting slots
      for i, rec in enumerate(self.recipes):
        r = CRAFTING_RECTS_TALL[i]
        for j in range(4):
          if rec[j] is not None:
            indx = i + j*10
            pos = CRAFTING_POSITIONS[indx]
            if r.collidepoint(*pygame.mouse.get_pos()):
              self.game.nozoom.blit(SELECTED, pos)
            else:
              self.game.nozoom.blit(SLOT, pos)
      # Draw crafting items
      self.crafting_group.draw(self.game.nozoom)
      # Draw crafting quantities
      for i, rec in enumerate(self.recipes):
        r = CRAFTING_RECTS_TALL[i]
        for j in range(4):
          if rec[j] is not None:
            indx = i + j*10
            pos = CRAFTING_POSITIONS_CENTER[indx]
            if r.collidepoint(*pygame.mouse.get_pos()):
              c = (0, 0, 0)
            else:
              c = (255, 255, 255)
            tx, ty = pos
            text = FONT.render(str(rec[j][1]), True, c)
            self.game.nozoom.blit(text, (tx+20-text.get_width(), ty))
      
      mouse = pygame.mouse.get_pos()
      # get slot ID of hover
      hover = -1
      for i, r in enumerate(SLOT_RECTS):
        if r.collidepoint(mouse):
          hover = i
      for i, r in enumerate(INV_RECTS):
        if r.collidepoint(mouse):
          hover = i + 10
      if hover != -1:
        # draw tooltip
        self.show_tooltip(hover, mouse)

    else: #NOT SHOWALL
      # Draw hotbar slots
      for i, pos in enumerate(SLOT_POSITIONS):
        if i == self.selected:
          self.game.nozoom.blit(SELECTED, pos)
        else:
          self.game.nozoom.blit(SLOT, pos)
      # Draw hotbar items
      self.hotbar_group.draw(self.game.nozoom)
      # Draw hotbar quantities
      for i, pos in enumerate(SLOT_POSITIONS_CENTER):
        if self.items[i][0] != 0:
          if i == self.selected:
            c = (0, 0, 0)
          else:
            c = (255, 255, 255)
          tx, ty = pos
          text = FONT.render(str(self.items[i][1]), True, c)
          self.game.nozoom.blit(text, (tx+20-text.get_width(), ty))

      mouse = pygame.mouse.get_pos()
      # Tooltip
      hover = -1
      for i, r in enumerate(SLOT_RECTS):
        if r.collidepoint(mouse):
          hover = i
      if hover != -1:
        self.show_tooltip(hover, mouse)
  
  def show_tooltip(self, indx, mouse):
    item = self.items[indx]
    meta = engine.items.ITEM_METADATA[item[0]] # If item wants to show tooltip
    if meta[engine.items.META_SHOW_TOOLTIP]:
      img = TOOLTIP_FONT.render(meta[engine.items.META_TOOLTIP_TEXT], True, (0,255,255), (0,0,255))
      self.game.nozoom.blit(img, img.get_rect(bottomleft=mouse).topleft) # Render so mouse is at bottom left


  def update(self):
    # Update the item sprites.
    for i in range(10):
      self.hotbar_sprites[i].setSprite(self.items[i][0])
    self.hotbar_group.update()
    for i in range(30):
      self.inventory_sprites[i].setSprite(self.items[i+10][0])
    self.inventory_group.update()
    self.crafting_group.update()
  
  def update_craftable(self):
    # Which recipes are craftable? store them so we only display them
    self.recipes = []
    for recipe in engine.crafting.RECIPES:
      max_num = 1000
      recipe_entry = []
      # Create the recipe entry
      for inp in recipe.inputs:
        max_num = min(max_num,self.num(inp.item) // inp.quantity)
      for inp in recipe.inputs:
        recipe_entry.append([inp.item, inp.quantity])# * max_num
      recipe_entry.extend([None] * (3 - len(recipe_entry)))
      recipe_entry.append([recipe.output.item, recipe.output.quantity])# * max_num
      if max_num > 0:
        # If can craft: add to render list
        self.recipes.append(recipe_entry[::-1])
    # set all sprites to air to hide no longer needed ones
    for s in self.crafting_sprites:
      s.setSprite(0)

    for i, rec in enumerate(self.recipes):
      for j, item in enumerate(rec):
        # set to correct sprite if needed
        indx = i + j*10
        if item is not None:
          self.crafting_sprites[indx].setSprite(item[0])

  def event(self, event):
    if event.type == pygame.KEYDOWN:
      # If number key pressed, set selected to it
      if event.key == pygame.K_1:
        self.selected = 0
        return True
      if event.key == pygame.K_2:
        self.selected = 1
        return True
      if event.key == pygame.K_3:
        self.selected = 2
        return True
      if event.key == pygame.K_4:
        self.selected = 3
        return True
      if event.key == pygame.K_5:
        self.selected = 4
        return True
      if event.key == pygame.K_6:
        self.selected = 5
        return True
      if event.key == pygame.K_7:
        self.selected = 6
        return True
      if event.key == pygame.K_8:
        self.selected = 7
        return True
      if event.key == pygame.K_9:
        self.selected = 8
        return True
      if event.key == pygame.K_0:
        self.selected = 9
        return True
      # Toggle inventory on
      if event.key == pygame.K_e and not self.showall:
        self.showall = True
        self.swap = -1
        return True
      # Toggle inventory off
      if self.showall and event.key in [pygame.K_ESCAPE, pygame.K_e]:
        self.showall = False
        return True
      # Supress movement if inventory open
      if self.showall:
        if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE]:
          return True
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        if self.showall:
          for i in range(10):
            #For each potential recipe slot
            if CRAFTING_RECTS_TALL[i].collidepoint(*event.pos):
              # If clicked, do crafting
              if len(self.recipes) > i:
                for j in range(1,4):
                  if self.recipes[i][j] is not None:
                    self.remove(self.recipes[i][j][0], self.recipes[i][j][1], False)
                self.give(self.recipes[i][0][0], self.recipes[i][0][1])
                return True
          else:
            # If no swap active
            if self.swap == -1:
              # Activate swap if clicked on slot
              for i, r in enumerate(SLOT_RECTS):
                if r.collidepoint(event.pos):
                  self.swap = i
              for i, r in enumerate(INV_RECTS):
                if r.collidepoint(event.pos):
                  self.swap = i + 10
            else:
              # Get slot id of clicked
              clicked = -1
              for i, r in enumerate(SLOT_RECTS):
                if r.collidepoint(event.pos):
                  clicked = i
              for i, r in enumerate(INV_RECTS):
                if r.collidepoint(event.pos):
                  clicked = i + 10
              if clicked !=-1:
                if clicked != self.swap:
                  # Swap if needed
                  self.items[clicked], self.items[self.swap] = self.items[self.swap], self.items[clicked]
                # end swap
                self.swap = -1
          return True
        else:
          # Select slot if clicked on while inventory closed
          for i, r in enumerate(SLOT_RECTS):
            if r.collidepoint(event.pos):
              self.selected = i
              return True
      # If scroll, change item selected
      if event.button == 5 and not self.showall:
        self.selected += 1
        self.selected %= 10
        return True
      if event.button == 4 and not self.showall:
        self.selected -= 1
        self.selected %= 10
        return True
    return False # No event happened.

  def get_selected(self):
    return self.items[self.selected][0]