import pygame
import karas
import engine
import barras

def run(npcs):
  game = karas.game.Game()

  #buttons = karas.sprite.Group(karas.sprite.Button)
  #buttons = karas.sprite.Group(karas.sprite.TransparentButton)
  #buttons.createNew("hello!", pos=(200, 200))

  world = engine.world.World(game, 4)
  npcSpriteGroup = npcs.createNPCs(world)
  world.assign_npcs(npcs.sprites, npcs.npcs, npcSpriteGroup)


  game.assign_world(world)
  x = 0

  player = engine.player.Player(world) 

  world.assign_player(player)
  players = pygame.sprite.Group()
  players.add(player)

  clock = pygame.time.Clock()

  text = barras.timetext.timedText("2172", pygame.font.SysFont("Calibri", 50), (0, 196, 190), (100, 30), 5)
  textGroup = pygame.sprite.GroupSingle(text)

  world.assign_text(text)
  world.travel("50")

  while True:
    #buttons.update()
    world.update(player)
    npcSpriteGroup.update()
    players.update()
    textGroup.update()

    world.render()
    players.draw(game.zoom)
    for n in npcs.sprites:
      n.update2()
    npcSpriteGroup.draw(game.zoom)

    player.render()
    #textGroup.draw(game.nozoom)
    
    pressed = pygame.key.get_pressed()
    #buttons.draw(game.game)
    for event in pygame.event.get():
      if player.event(event): continue
      if game.event(event): continue
      if world.event(event): continue
    game.render()
    clock.tick(30)