if __name__ == "__main__":
  import sys
  from pathlib import Path
  import pygame
  pygame.init()
  directory = Path(__file__)
  sys.path.append(str(directory.parent.parent))
  screen = pygame.display.set_mode((1920, 1080))

import pygame
import engine
import theas.save_chooser
import karas
import random
import mono

font = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 30)
def do_settings(screen):
  pass