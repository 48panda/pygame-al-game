import loader
import pygame

screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)

loadingScreen = loader.LoadingScreen(screen)

loadingScreen.update("Loading code...")
import game
import karas
import olivas

loadingScreen.update("Transitioning to Game Class...")
Game = karas.game.Game()

loadingScreen = loader.LoadingScreen(Game.game, "Creating NPCs...")
npcs = olivas.NPCIndex()
npcs.generateYearsForNPCs(0)


try:
  game.run(npcs, Game, loadingScreen)
except karas.QuitTriggered:
  pass