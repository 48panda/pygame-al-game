import pygame
import karas
import engine

def run():
  game = karas.game.Game()

  #buttons = karas.sprite.Group(karas.sprite.Button)
  #buttons = karas.sprite.Group(karas.sprite.TransparentButton)
  #buttons.createNew("hello!", pos=(200, 200))
  
  world = engine.world.World(game)
  x = 0

  player = engine.player.Player(world) 
  players = pygame.sprite.Group()
  players.add(player)

  clock = pygame.time.Clock()

  while True:
    #buttons.update()
    game.game.fill((255,255,255))
    


    world.update(player)
    players.update()

    world.render()
    players.draw(game.game)
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
      player.vx -= 0.1
    if pressed[pygame.K_d]:
      player.vx += 0.1
    if pressed[pygame.K_w] and player.vy == 0:
      player.vy -= 0.8
    #buttons.draw(game.game)
    game.events()
    game.render()
    clock.tick(30)