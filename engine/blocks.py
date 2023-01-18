import engine.items
import engine.buildings
class Blockstateless:
  """Blocks with only one state. E.g. Stone
  """
  def __init__(self, block):
    self.block = block
  
  def __and__(self, other):
    # equal to (state-specific)
    return self.block == other.block
  
  def __or__(self, other):
    # equal to (state-unspecific)
    return self.block == other.block
  
  def __xor__(self, other):
    # Not the same block type
    return self.block != other.block
    
  def __str__(self):
    return f"<{self.block}>"
  __repr__ = __str__

class Blockstate:
  """Blocks with multiple states e.g. trees or housing
  """
  def __init__(self, block, state):
    self.block = block
    self.state = state
  
  def __str__(self):
    return f"<{self.block}:{self.state}>"
  __repr__ = __str__
  
  def __and__(self, other):
    # equal to (state-specific)
    return (self.block == other.block) and self.state == other.state
  
  def __or__(self, other):
    # equal to (state-unspecific)
    return self.block == other.block
  
  def __xor__(self, other):
    # Not the same block type
    return self.block != other.block

NUM_BLOCKS = 16 # How many blocks there are (excluding blockstates)

class blockGroup:
  def __init__(self, *blocks):
    self.blocks = tuple([j in [i.block for i in blocks] for j in range(NUM_BLOCKS)])
  
  def __contains__(self, block):
    # for use in "if block in group"
    return self.blocks[block.block]

def blockstate(block, num_states):
  # Helper to generate blockstates
  return tuple([Blockstate(block, i) for i in range(num_states)])
allBlockStates = (
  Blockstateless(0),# Defining blocks
  Blockstateless(1),
  Blockstateless(2),
  Blockstateless(3),
  blockstate(4, 11),
  Blockstateless(5),
  Blockstateless(6),
  blockstate(7, 8),
  Blockstateless(8),
  Blockstateless(9),
  Blockstateless(10),
  Blockstateless(11),
  Blockstateless(12),
  Blockstateless(13),
  Blockstateless(14),
  Blockstateless(15),
)

# Setting enums for use throughout the program
AIR = allBlockStates[0]
DIRT = allBlockStates[1]
SHIP = allBlockStates[2]
TREE = allBlockStates[3]
LEAVES= allBlockStates[4][0]
OBSIDIAN = allBlockStates[5]
BEDROCK = allBlockStates[6]
HOUSE0000 = allBlockStates[7][0]
HOUSE0450 = allBlockStates[7][1]
HOUSE0793 = allBlockStates[7][2]
HOUSE1066 = allBlockStates[7][3]
HOUSE1485 = allBlockStates[7][4]
HOUSE1603 = allBlockStates[7][5]
HOUSE1837 = allBlockStates[7][6]
HOUSE1902 = allBlockStates[7][7]
DESK = allBlockStates[8]
BILLBOARD = allBlockStates[9]
RADIANITE = allBlockStates[10]
STONE = allBlockStates[11]
PLANKS = allBlockStates[12]
SAND = allBlockStates[13]
SANDSTONE = allBlockStates[14]
STONEBRICKS = allBlockStates[15]

# The first year each house is available
UPGRADE_YEARS = {0:HOUSE0000,450:HOUSE0450,793:HOUSE0793,1066:HOUSE1066,1485:HOUSE1485,1603:HOUSE1603,1837:HOUSE1837,1902:HOUSE1902}

import pygame
pygame.font.init()
TEST_FONT = pygame.font.SysFont("Calibri", 12)

def nothing(**_):
  pass

def leaf_update(state, neighbours, set_at, x, y, drop, **_):
  """Get distance from a log, if more than 6 then break.
  """
  highest = 0
  t = False
  # Find closest tree block to log
  for n in neighbours:
    if n | state:
      # Leaf counts as one less than it's own value
      highest = max(n.state - 1, highest)
    if n & TREE:
      t = True
      # tree counts as 6
      highest = max(6, highest)
  if highest == 0: # No log nearby
    set_at(x, y, AIR, drop=drop)
  elif highest != state.state: # Update state
    set_at(x, y, allBlockStates[4][highest], drop=drop)

def log_update(state, down, set_at, x, y, drop, **_):
  if not (down in COLLIDE or down | TREE): # If tree should fall, fall
    set_at(x, y, AIR, drop=drop)

# Called when any of it's neighbours change state
UPDATE = (nothing, nothing, nothing, log_update, leaf_update, nothing, nothing, nothing, nothing, nothing, nothing, nothing, nothing, nothing, nothing, nothing)
# block ID to item to drop
TO_ITEM = (None, engine.items.DIRT, None, engine.items.TREE, None, engine.items.OBSIDIAN, None, None, None, None, engine.items.RADIANITE_ORE, engine.items.STONE,
  engine.items.PLANKS, engine.items.SAND, engine.items.SANDSTONE, engine.items.STONEBRICKS)
# block ID to texture (tile renderer)
TILE = (None, None, None, engine.tiles.TREE, engine.tiles.LEAVES, engine.tiles.OBSIDIAN, engine.tiles.BEDROCK, None, None, None, engine.tiles.RADIANITE, engine.tiles.STONE, engine.tiles.PLANKS,
        engine.tiles.SAND, engine.tiles.SANDSTONE, engine.tiles.STONEBRICKS)
# block ID to texture (building renderer)
BUILDING = (None, None, engine.buildings.SHIP, None, None, None, None, None, engine.buildings.DESK, engine.buildings.BILLBOARD, None, None, None, None, None, None)
# Blocks that can be destroyed if you click on them with a pickaxe
MINEABLE_PICKAXE = blockGroup(DIRT, TREE, LEAVES, OBSIDIAN, RADIANITE, STONE, PLANKS, SAND, SANDSTONE, STONEBRICKS)
#Blocks that you can place blocks over
REPLACEABLE = blockGroup(AIR, LEAVES)
#Blocks characters collide with
COLLIDE = blockGroup(DIRT, OBSIDIAN, BEDROCK, RADIANITE, STONE, PLANKS, SAND, SANDSTONE, STONEBRICKS)
# Blocks that use the tile renderer (not dirt, due to the grass part)
USE_TILE_RENDERER = blockGroup(STONE, TREE, LEAVES, OBSIDIAN, BEDROCK, RADIANITE,
 PLANKS, SAND, SANDSTONE, STONEBRICKS)
# Can a tree grow here
TREEABLE = blockGroup(DIRT)
# Stops the player mining the blocks below houses
CANT_MINE_BLOCK_BELOW = blockGroup(HOUSE0000, DESK)
# Things that use the standard building renderer(large textures placed at the bottom-leftmost tile in a rectangle)
USE_BUILDING_RENDERER = blockGroup(SHIP, DESK, BILLBOARD)
# item ID to block
PLACE_MAP = (None, DIRT, None, None, OBSIDIAN, None, STONE, None, PLANKS, SAND, SANDSTONE, STONEBRICKS)