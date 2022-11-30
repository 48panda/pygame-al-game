import pygame
import engine.items
import engine.crafting

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

SLOT = pygame.image.load("assets/gui/slot.png").convert_alpha()
SELECTED = pygame.image.load("assets/gui/selectedslot.png").convert_alpha()
SWAP = pygame.image.load("assets/gui/swapslot.png").convert_alpha()

FONT = pygame.font.SysFont("Calibri", 20, bold=True)

class Inventory:
  def __init__(self, items, player, game):
    self.items = items + [[0,0] for _ in range(40-len(items))]
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
    
  def get_slot(self, slot):
    return self.items[slot][0]
  
  def has(self, item, count=1):
    for i in self.items:
      if i[0] == item:
        return i[1] >= count
    return False

  def num(self, item):
    for i in self.items:
      if i[0] == item:
        return i[1]
    return 0
    
  def give(self, item, num=1, reloadRecipes=True):
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
    for i in range(len(self.items)):
      if self.items[i][0] == item:
        self.items[i][1] -= num
        if self.items[i][1] <= 0:
          self.items[i] = [0,0]
        if reloadRecipes:
          self.update_craftable()
        return
      
  
  def removeFromSlot(self, slot):
    self.items[slot][1] -= 1
    if self.items[slot][1] <= 0:
      self.items[slot][0] = 0
    self.update_craftable()


  def render(self):
    if self.showall:
      for i, pos in enumerate(SLOT_POSITIONS):
        if i == self.swap:
          self.game.nozoom.blit(SWAP, pos)
        else:
          self.game.nozoom.blit(SLOT, pos)
      self.hotbar_group.draw(self.game.nozoom)
      for i, pos in enumerate(SLOT_POSITIONS_CENTER):
        if self.items[i][0] != 0:
          if i == self.swap:
            c = (0, 0, 0)
          else:
            c = (255, 255, 255)
          tx, ty = pos
          text = FONT.render(str(self.items[i][1]), True, c)
          self.game.nozoom.blit(text, (tx+20-text.get_width(), ty))

      for i, pos in enumerate(INV_POSITIONS):
        i = i + 10
        if i == self.swap:
          self.game.nozoom.blit(SWAP, pos)
        else:
          self.game.nozoom.blit(SLOT, pos)
      self.inventory_group.draw(self.game.nozoom)
      for i, pos in enumerate(INV_POSITIONS_CENTER):
        i = i + 10
        if self.items[i][0] != 0:
          if i == self.swap:
            c = (0, 0, 0)
          else:
            c = (255, 255, 255)
          tx, ty = pos
          text = FONT.render(str(self.items[i][1]), True, c)
          self.game.nozoom.blit(text, (tx+20-text.get_width(), ty))

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
      self.crafting_group.draw(self.game.nozoom)
      for i, rec in enumerate(self.recipes):
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
    else:
      for i, pos in enumerate(SLOT_POSITIONS):
        if i == self.selected:
          self.game.nozoom.blit(SELECTED, pos)
        else:
          self.game.nozoom.blit(SLOT, pos)
      self.hotbar_group.draw(self.game.nozoom)
      for i, pos in enumerate(SLOT_POSITIONS_CENTER):
        if self.items[i][0] != 0:
          if i == self.selected:
            c = (0, 0, 0)
          else:
            c = (255, 255, 255)
          tx, ty = pos
          text = FONT.render(str(self.items[i][1]), True, c)
          self.game.nozoom.blit(text, (tx+20-text.get_width(), ty))
  
  def update(self):
    for i in range(10):
      self.hotbar_sprites[i].setSprite(self.items[i][0])
    self.hotbar_group.update()
    for i in range(30):
      self.inventory_sprites[i].setSprite(self.items[i+10][0])
    self.inventory_group.update()
    self.crafting_group.update()
  
  def update_craftable(self):
    self.recipes = []
    for recipe in engine.crafting.RECIPES:
      max_num = 1000
      recipe_entry = []
      for inp in recipe.inputs:
        max_num = min(max_num,self.num(inp.item) // inp.quantity)
      for inp in recipe.inputs:
        recipe_entry.append([inp.item, inp.quantity])# * max_num
      recipe_entry.extend([None] * (3 - len(recipe_entry)))
      recipe_entry.append([recipe.output.item, recipe.output.quantity])# * max_num
      if max_num > 0:
        self.recipes.append(recipe_entry[::-1])
    for s in self.crafting_sprites:
      s.setSprite(0)
    for i, rec in enumerate(self.recipes):
      for j, item in enumerate(rec):
        indx = i + j*10
        if item is not None:
          self.crafting_sprites[indx].setSprite(item[0])

  def event(self, event):
    if event.type == pygame.KEYDOWN:
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
      if event.key == pygame.K_e and not self.showall:
        self.showall = True
        self.swap = -1
        return True
      if self.showall and event.key in [pygame.K_ESCAPE, pygame.K_e]:
        self.showall = False
        return True
      if self.showall:
        if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE]:
          return True
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        if self.showall:
          for i in range(10):
            if CRAFTING_RECTS_TALL[i].collidepoint(*event.pos):
              for j in range(1,4):
                if self.recipes[i][j] is not None:
                  self.remove(self.recipes[i][j][0], self.recipes[i][j][1], False)
              self.give(self.recipes[i][0][0], self.recipes[i][0][1])
              return True
          else:
            if self.swap == -1:
              for i, r in enumerate(SLOT_RECTS):
                if r.collidepoint(event.pos):
                  self.swap = i
              for i, r in enumerate(INV_RECTS):
                if r.collidepoint(event.pos):
                  self.swap = i + 10
            else:
              clicked = -1
              for i, r in enumerate(SLOT_RECTS):
                if r.collidepoint(event.pos):
                  clicked = i
              for i, r in enumerate(INV_RECTS):
                if r.collidepoint(event.pos):
                  clicked = i + 10
              if clicked !=-1:
                if clicked != self.swap:
                  self.items[clicked], self.items[self.swap] = self.items[self.swap], self.items[clicked]
                self.swap = -1
          return True
        else:
          for i, r in enumerate(SLOT_RECTS):
            if r.collidepoint(event.pos):
              self.selected = i
              return True
      if event.button == 5 and not self.showall:
        self.selected += 1
        self.selected %= 10
      if event.button == 4 and not self.showall:
        self.selected -= 1
        self.selected %= 10
    return False
  def get_selected(self):
    return self.items[self.selected][0]