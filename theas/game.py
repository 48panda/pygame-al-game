import pygame
import engine
import olivas
import constants
import mono
import time

def run(npcs, game, loadingScreen, clock, seed, player_appearance=None, isNew=True):
  
  seed = time.time()
  #Set the seed to the time as it is currently always a constant
  # Initialise everything
  if isNew:
    world = engine.world.World(game, seed, loadingScreen, clock)
    npcs.generateYearsForNPCs(seed, world.landing_site_x)
    loadingScreen.update("Creating NPCs...")
    npcSpriteGroup = npcs.createNPCs(world, loadingScreen)
    world.assign_npcs(npcs.sprites, npcs.npcs, npcSpriteGroup)

    game.assign_world(world)

    player = engine.player.Player(world, cstring=player_appearance)

    world.assign_player(player)
    players = pygame.sprite.Group()
    players.add(player)



    speech = olivas.speech.speech()
    speechGroup = pygame.sprite.GroupSingle(speech)
    linearSpeech = olivas.speech.LinearSpeech(speech)

    book = olivas.book.GuideBook(game, linearSpeech=linearSpeech)

    world.assign_book(book)
  else:
    world = game.world
    world.__init__(game, seed, loadingScreen, clock, hasBeenLoaded=True)
    game.keypad.world = world
    npcs.npcs = world.npcs
    loadingScreen.update("Creating NPCs...")
    npcSpriteGroup = npcs.createNPCs(world, loadingScreen)
    world.assign_npcs(npcs.sprites, npcs.npcs, npcSpriteGroup)
    player = world.player
    player.__init__(world, hasBeenLoaded=True)
    players = pygame.sprite.Group(player)
    book = world.book
    speech = olivas.speech.speech()
    speechGroup = pygame.sprite.GroupSingle(speech)
    linearSpeech = olivas.speech.LinearSpeech(speech)
    book.__init__(game, linearSpeech=linearSpeech, hasBeenLoaded=True)
    world.load_npcs()
  
    

  if constants.SHOW_FPS:
    font = pygame.font.SysFont("Courier", 30)
  mono.yes_music() #yes! music
  while True:
    # Run every frame
    world.skipRenderFrame = False
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
    # Pass events through everything
    for event in pygame.event.get():
      if linearSpeech.event(event): continue
      if player.event(event): continue
      if book.event(event): continue

      for npc in world.npcSpriteGroup:
        if npc.event(event): break
      else:

        if game.event(event): continue
        if world.event(event): continue
        if mono.music_event(event): continue
    if game.exit_to_title: return
    if constants.SHOW_FPS:
      text = font.render(str(round(clock.get_fps())), True, (255, 0, 0))
      game.nozoom.blit(text, text.get_rect(topright=(1920,0)))
    if not world.skipRenderFrame:
      game.render() # render
    