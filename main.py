import pygame
screen = pygame.display.set_mode((1920,1080), pygame.SCALED | pygame.FULLSCREEN)
import theas
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
loadingScreen = theas.loader.LoadingScreen(screen)

loadingScreen.update("Loading code...")
import os

import karas
import olivas
import engine
import saras
import constants
clock = pygame.time.Clock()
while True:
  try:
    theas.title.do_title_screen(screen,clock,loadingScreen)
  except karas.QuitTriggered:
    break
  except karas.ReloadTitleScreen:
    pass
