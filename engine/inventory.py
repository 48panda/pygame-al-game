import pygame
import engine.items

SLOT_SIZE = 45
PADDED_SLOT_SIZE = 50
SLOT_POSITIONS = [(1920//2-(5-i)*PADDED_SLOT_SIZE,1080-PADDED_SLOT_SIZE) for i in range(10)]
SLOT_POSITIONS_CENTER = [(1920//2-(5-i)*PADDED_SLOT_SIZE + SLOT_SIZE/2,1080-PADDED_SLOT_SIZE + SLOT_SIZE/2) for i in range(10)]
SLOT_RECTS = [pygame.Rect(pos[0], pos[1], SLOT_SIZE, SLOT_SIZE) for pos in SLOT_POSITIONS]

SLOT = pygame.image.load("assets/gui/slot.png")
SELECTED = pygame.image.load("assets/gui/selectedslot.png")

class Inventory:
  def __init__(self, items, player, game):
    self.items = items + [0 for _ in range(10-len(items))]
    self.player = player
    self.game = game
    self.hotbar_sprites = [engine.items.Item(SLOT_POSITIONS_CENTER[i]) for i in range(10)]
    self.hotbar_group = pygame.sprite.Group(self.hotbar_sprites)
    self.selected = 0
    self.player_sprite = engine.items.Item(self.player.rect.center)
    self.player_sprite_group = pygame.sprite.GroupSingle(self.player_sprite)
    for i in self.hotbar_sprites:
      i.setSprite(0)
      i.update()
  def get_slot(self, slot):
    return self.items[slot]
  def render(self):
    for i, pos in enumerate(SLOT_POSITIONS):
      if i == self.selected:
        self.game.nozoom.blit(SELECTED, pos)
      else:
        self.game.nozoom.blit(SLOT, pos)
    self.hotbar_group.draw(self.game.nozoom)
  def update(self):
    for i in range(10):
      self.hotbar_sprites[i].setSprite(self.items[i])
    self.hotbar_group.update()
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
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        for i, r in enumerate(SLOT_RECTS):
          if r.collidepoint(event.pos):
            self.selected = i
            return True
    return False
  def get_selected(self):
    return self.items[self.selected]