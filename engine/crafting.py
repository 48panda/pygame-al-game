import engine.items as items

class Item:
  def __init__(self, item, quantity):
    self.item = item
    self.quantity = quantity
    print("EE", self.quantity)

class CraftingRecipe:
  def __init__(self, output, *inputs):
    self.inputs = inputs
    self.output = output

RECIPES = (CraftingRecipe(Item(items.RADIANITE_INGOT, 1), Item(items.RADIANITE_ORE, 2)),)