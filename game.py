import pygame
import karas
import engine
import barras
import olivas
import constants

def run(npcs, game, loadingScreen):
  

  #buttons = karas.sprite.Group(karas.sprite.Button)
  #buttons = karas.sprite.Group(karas.sprite.TransparentButton)
  #buttons.createNew("hello!", pos=(200, 200))

  world = engine.world.World(game, 5, loadingScreen)
  loadingScreen.update("Creating NPCs...")
  npcSpriteGroup = npcs.createNPCs(world, loadingScreen)
  world.assign_npcs(npcs.sprites, npcs.npcs, npcSpriteGroup)



  game.assign_world(world)
  x = 0

  player = engine.player.Player(world) 

  world.assign_player(player)
  players = pygame.sprite.Group()
  players.add(player)

  clock = pygame.time.Clock()

  speech = olivas.speech.speech()
  speechGroup = pygame.sprite.GroupSingle(speech)
  linearSpeech = olivas.speech.LinearSpeech(speech)

  book = olivas.book.GuideBook(game, linearSpeech=linearSpeech)
  if constants.SHOW_FPS:
    font = pygame.font.SysFont("Courier", 30)

  while True:
    #buttons.update()
    td = clock.tick(30) / 1000
    world.update(player)
    npcSpriteGroup.update()
    players.update()
    book.update()
    linearSpeech.update(td)
    speech.clock_tick(td)
    speechGroup.update()

    world.render()
    players.draw(game.zoom)
    for sprite in npcSpriteGroup.spritedict.keys():
      sprite.update2()
    npcSpriteGroup.draw(game.zoom)

    player.render()
    book.render(game.nozoom)
    speechGroup.draw(game.nozoom)
    pressed = pygame.key.get_pressed()
    #buttons.draw(game.game)
    for event in pygame.event.get():
      if linearSpeech.event(event): continue
      if player.event(event): continue
      if game.event(event): continue
      if world.event(event): continue
    
    if constants.SHOW_FPS:
      text = font.render(str(round(clock.get_fps())), True, (255, 0, 0))
      game.nozoom.blit(text, text.get_rect(topright=(1920,0)))
    game.render()
    