import engine.items
class Blockstateless:
  def __init__(self, block):
    self.block = block
  
  def __and__(self, other):
    return self.block == other.block
  
  def __or__(self, other):
    return self.block == other.block

class Blockstate:
  def __init__(self, block, state):
    self.block = block
    self.state = state
  
  def __str__(self):
    return f"<{self.block}:{self.state}>"
  __repr__ = __str__
  
  def __and__(self, other):
    return (self.block == other.block) and self.state == other.state
  
  def __or__(self, other):
    return self.block == other.block

class blockGroup:
  def __init__(self, *blocks):
    self.blocks = blocks
  
  def __contains__(self, block):
    for b in self.blocks:
      if b | block:
        return True
    return False

def blockstate(block, num_states):
  return tuple([Blockstate(block, i) for i in range(num_states)])
allBlockStates = (Blockstateless(0), Blockstateless(1), Blockstateless(2), Blockstateless(3), blockstate(4, 11))

AIR = allBlockStates[0]
DIRT = allBlockStates[1]
SHIP = allBlockStates[2]
TREE = allBlockStates[3]
LEAVES= allBlockStates[4][0]

import pygame
pygame.font.init()
TEST_FONT = pygame.font.SysFont("Calibri", 12)

def nothing(**_):
  pass

def leaf_update(state, neighbours, changeState, x, y, drop, **_):
  highest = 0
  t = False
  for n in neighbours:
    if n | state:
      highest = max(n.state - 1, highest)
    if n & TREE:
      t = True
      highest = max(10, highest)
  if highest == 0:
    changeState(x, y, AIR, drop=drop)
  elif highest != state.state:
    changeState(x, y, allBlockStates[4][highest], drop=drop)

def log_update(state, down, changeState, x, y, drop, **_):
  if not (down in COLLIDE or down | TREE):
    changeState(x, y, AIR, drop=drop)

UPDATE = (nothing, nothing, nothing, log_update, leaf_update)
TO_ITEM = (None, engine.items.DIRT, None, engine.items.TREE, None)

MINEABLE_PICKAXE = blockGroup(DIRT, TREE, LEAVES)
REPLACEABLE = blockGroup(AIR, LEAVES)
WALKABLE = blockGroup(AIR, SHIP, TREE, LEAVES)
COLLIDE = blockGroup(DIRT)