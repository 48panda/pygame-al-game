import game
import karas
import olivas

npcs = olivas.NPCIndex()
npcs.generateYearsForNPCs(0)

try:
  game.run(npcs)
except karas.QuitTriggered:
  pass