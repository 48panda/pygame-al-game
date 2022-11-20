import pygame
import engine.items

SLOT_SIZE = 45
PADDED_SLOT_SIZE = 50
SLOT_POSITIONS = [(1920//2-(5-i)*PADDED_SLOT_SIZE,1080-PADDED_SLOT_SIZE) for i in range(10)]
SLOT_POSITIONS_CENTER = [(1920//2-(5-i)*PADDED_SLOT_SIZE + SLOT_SIZE/2,1080-PADDED_SLOT_SIZE + SLOT_SIZE/2) for i in range(10)]
SLOT_RECTS = [pygame.Rect(pos[0], pos[1], SLOT_SIZE, SLOT_SIZE) for pos in SLOT_POSITIONS]

INV_POSITIONS = sum([[(i[0], i[1] - PADDED_SLOT_SIZE * h) for i in SLOT_POSITIONS] for h in range(1,4)], [])
INV_POSITIONS_CENTER = sum([[(i[0], i[1] - PADDED_SLOT_SIZE * h) for i in SLOT_POSITIONS_CENTER] for h in range(1,4)], [])
INV_RECTS = [pygame.Rect(pos[0], pos[1], SLOT_SIZE, SLOT_SIZE) for pos in INV_POSITIONS]


SLOT = pygame.image.load("assets/gui/slot.png")
SELECTED = pygame.image.load("assets/gui/selectedslot.png")
SWAP = pygame.image.load("assets/gui/swapslot.png")

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
    self.selected = 0
    self.player_sprite = engine.items.Item(self.player.rect.center)
    self.player_sprite_group = pygame.sprite.GroupSingle(self.player_sprite)
    self.showall = False
    self.swap = -1
    for i in self.hotbar_sprites:
      i.setSprite(0)
      i.update()
    for i in self.inventory_sprites:
      i.setSprite(0)
      i.update()
    
  def get_slot(self, slot):
    return self.items[slot][0]

  def give(self, item):
    for i in range(len(self.items)):
      if self.items[i][0] == item:
        self.items[i][1] += 1
        return
    for i in range(len(self.items)):
      if self.items[i][0] == 0:
        self.items[i][0] = item
        self.items[i][1] = 1
        return
  
  def removeFromSlot(self, slot):
    self.items[slot][1] -= 1
    if self.items[slot][1] <= 0:
      self.items[slot][0] = 0


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