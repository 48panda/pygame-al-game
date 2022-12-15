import engine.items as items

class Item:
  def __init__(self, item, quantity):
    self.item = item
    self.quantity = quantity

class CraftingRecipe:
  def __init__(self, output, *inputs):
    self.inputs = inputs
    self.output = output

RECIPES = (CraftingRecipe(Item(items.RADIANITE_INGOT, 1), Item(items.RADIANITE_ORE, 2)),
          CraftingRecipe(Item(items.PLANKS, 2)     , Item(items.TREE, 4) ),
          CraftingRecipe(Item(items.SANDSTONE, 1)  , Item(items.SAND, 3) ),
          CraftingRecipe(Item(items.STONEBRICKS, 2), Item(items.STONE, 1))
)