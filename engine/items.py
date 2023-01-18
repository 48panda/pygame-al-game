import karas
import pygame

#Spritesheet
ITEMS_IMG = pygame.image.load("assets/items/items.png").convert_alpha()

# Item ids.
DIRT = 1
WOODEN_PICKAXE = 2
TREE = 3
OBSIDIAN = 4
RADIANITE_ORE = 5
STONE = 6
RADIANITE_INGOT = 7
PLANKS = 8
SAND = 9
SANDSTONE = 10
STONEBRICKS = 11

# Enums for index of meta
META_SHOW_TOOLTIP = 0
META_TOOLTIP_TEXT = 1
# Set metadata
ITEM_METADATA = (    #SHOW_TOOLTIP, TOOLTIP_TEXT
                    (False       , ""               ), # AIR
                    (True        , "Dirt"           ), # DIRT
                    (True        , "Pickaxe"        ), # WOODEN_PICKAXE
                    (True        , "Log"            ), # TREE
                    (True        , "Obsidian"       ), # OBSIDIAN
                    (True        , "Radianite Ore"  ), # RADIANITE_ORE
                    (True        , "Stone"          ), # STONE
                    (True        , "Radianite Ingot"), # RADIANITE_INGOT
                    (True        , "Wooden Planks"  ), # PLANKS
                    (True        , "Sand"           ), # SAND
                    (True        , "Sandstone"      ), # SANDSTONE
                    (True        , "Stone Bricks"   ), # STONEBRICKS
)
# Which ones can be placed
PLACABLE = [DIRT, OBSIDIAN, STONE, PLANKS, SAND, SANDSTONE, STONEBRICKS]
# Which ones can mines tuff
PICKAXES = [WOODEN_PICKAXE]
# scale up
SPRITESHEET = pygame.transform.scale(ITEMS_IMG, (ITEMS_IMG.get_size()[0]*2, ITEMS_IMG.get_size()[1]*2))

NUM_SPRITES = 12

class Item(karas.sprite.Sprite):
  """Item in inventory
  """
  spritesheet = True
  spritewidth = 32
  spriteheight = 32
  num_sprites = NUM_SPRITES
  def init(self, pos):
    self.pos = pos
    self.fromSpriteSheet(SPRITESHEET)
    

class InWorldItem(karas.sprite.Sprite):
  """Item in world
  """
  spritesheet = True
  spritewidth = 32
  spriteheight = 32
  num_sprites = NUM_SPRITES
  def init(self, world, pos, sprite):
    self.fromSpriteSheet(SPRITESHEET)
    self.setSprite(sprite)
    self.sprite = sprite
    self.pos = world.tileToScreenPos(*pos)
    self.world = world

  def onupdate(self, rects):
    # get rect
    newrect = pygame.Rect((0,0), (20, 20))
    scale = 0.85

    px = self.world.player.rect.centerx
    py = self.world.player.rect.centery
    mx = self.pos[0]
    my = self.pos[1]
    # move towards player (without this it can start lagging **really** bad)
    self.pos =  (scale * (mx - px) + px, scale * (my - py) + py)

  def postupdate(self):
    if self.rect.colliderect(self.world.player.rect):
      # If touching player go into inventory
      self.kill()
      self.world.player.inventory.give(self.sprite)
