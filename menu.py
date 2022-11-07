import pygame
import karas

def run():
  game = karas.game.Game()

  #buttons = karas.sprite.Group(karas.sprite.Button)
  buttons = karas.sprite.Group(karas.sprite.TransparentButton)
  buttons.createNew("hello!", pos=(200, 200))

  while True:
    buttons.update()
    game.game.fill((255,255,255))
    buttons.draw(game.game)
    game.events()
    game.render()