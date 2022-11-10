import pygame
import karas
import engine

def run():
  game = karas.game.Game()

  #buttons = karas.sprite.Group(karas.sprite.Button)
  #buttons = karas.sprite.Group(karas.sprite.TransparentButton)
  #buttons.createNew("hello!", pos=(200, 200))
  
  world = engine.world.World(game, 0)
  x = 0

  player = engine.player.Player(world) 
  world.assign_player(player)
  players = pygame.sprite.Group()
  players.add(player)

  clock = pygame.time.Clock()

  while True:
    #buttons.update()
    game.game.fill((255,255,255))
    


    world.update(player)
    players.update()

    world.render()
    players.draw(game.zoom)
    player.render()
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
      player.vx -= 0.15
      player.flipped = False
    if pressed[pygame.K_d]:
      player.vx += 0.15
      player.flipped = True
    if pressed[pygame.K_w] and player.vy == 0:
      player.jump = 2
    #buttons.draw(game.game)
    for event in game.get_events():
      if player.event(event): continue
      if world.event(event): continue
    game.render()
    clock.tick(30)