import pygame
import karas
import engine
import olivas
import time
import saras.easing
import random
import constants
import mono

# Defines an asteroid sprite. Moves in a diagonal at a fixed speed. speeds up later to simulate rocket moving up
ASTEROID = pygame.image.load("assets/cutscene/asteroid.png").convert_alpha()

class AsteroidSprite(pygame.sprite.Sprite):
  def __init__(self, world):
    super().__init__()
    self.size = random.randint(30, 120)
    self.image = pygame.transform.scale(ASTEROID, (self.size, self.size))
    self.world = world
    self.x = random.uniform(0,200)
    self.y = 0
    self.speed = random.uniform(5, 20) * 30 / self.size
  def update(self, time, fall_fast):
    self.rect = self.image.get_rect(bottomleft = (self.x * 16 - self.world.scrollx, self.y * 16 - self.world.scrolly))
    self.x -= self.speed * time
    self.y += self.speed * time * fall_fast
    if self.y - self.size > 1080:
      self.kill()

def play_opening_cutscene(loadingScreen, player_appearance, clock):
  game = karas.game.Game(clock, None)
  mono.no_music() # Want custom music
  pygame.mixer_music.load("assets/sound/music/cutscene.mp3")
  world = engine.world.World(game, 0, loadingScreen, clock, cutscene=True)
  with open("assets/cutscene/level.txt", "r") as f:
    for line in f.readlines():
      row = []
      for c in line[:208]:
        # Read text file code
        if c == " ":
          block = engine.blocks.AIR
        if c == "c":
          block = engine.blocks.DIRT
        if c == "D":
          block = engine.blocks.DESK
        if c == "B":
          block = engine.blocks.BILLBOARD
        if c == "t":
          block = engine.blocks.TREE
        if c == "l":
          block = engine.blocks.LEAVES
        if c == "b":
          block = engine.blocks.STONEBRICKS
        if c == "s":
          block = engine.blocks.SANDSTONE
        row.append(block)
      world.level.append(row)
  clock = pygame.time.Clock()
  time_in = 0
  # Make easing for all things we want to ease
  # Starts out specific to show the screen. Maybe a way to make it more detailed in the future?
  zoom = saras.easing.EasingInteger(120)
  cameraPos = saras.easing.Easing2dVector((3,0.1875))
  scroll_x = saras.easing.EasingInteger(0)
  pygame.mixer.music.play()
  # NPC the player talks to
  em = olivas.cutscenenpc.NPC(world, pos=(30,60), cstring="1113d671dff7b00391d00ffdbac404040")
  player = olivas.cutscenenpc.NPC(world, pos=(27,60), cstring=player_appearance)
  speech = olivas.speech.speech()
  speechGroup = pygame.sprite.GroupSingle(speech)
  npcs = pygame.sprite.Group(em, player)
  # all thruster variations of the rocket with the player's head stuck inside it.
  rocket = engine.buildings.scale2x(pygame.image.load("assets/cutscene/rocket.png").convert_alpha())
  rocket.blit(player.sprites[0], (56, 30), area=pygame.Rect(12, 6, 16, 22))
  rocket2 = engine.buildings.scale2x(pygame.image.load("assets/cutscene/rocket2.png").convert_alpha())
  rocket2.blit(player.sprites[0], (56, 30), area=pygame.Rect(12, 6, 16, 22))
  rocket3 = engine.buildings.scale2x(pygame.image.load("assets/cutscene/rocket3.png").convert_alpha())
  rocket3.blit(player.sprites[0], (56, 30), area=pygame.Rect(12, 6, 16, 22))
  rocket4 = engine.buildings.scale2x(pygame.image.load("assets/cutscene/rocket4.png").convert_alpha())
  rocket4.blit(player.sprites[0], (56, 30), area=pygame.Rect(12, 6, 16, 22))
  rocketpos = saras.easing.Easing2dVector((0,0))
  # initialise more stuff
  font = pygame.font.SysFont("Calibri", 30)
  asteroids = pygame.sprite.Group()
  opacity = saras.easing.EasingInteger(0)
  frame = 0
  if constants.SHOW_FPS:
    font = pygame.font.SysFont("Courier", 30)
  while True:
    frame += 1
    # time pass counter
    pygame.event.pump()
    time_passed = clock.tick(30) / 1000
    prev_time = time_in
    time_in += time_passed
    # time of rocket launch (in s)
    t = 92

    # Events here
    if prev_time < 4 <= time_in:
      zoom.ease_to(2, 2)
    if prev_time < 7 <= time_in:
      cameraPos.ease_to((0, 0), 2)
      em.go_right(4, 3)
    elif prev_time < 12 <= time_in:
      player.go_right(3.5, 3)
    elif prev_time < 14 <= time_in:
      em.go_left(1.2, 2)
    elif prev_time < 15 <= time_in:
      speech.show("My readings say we've got a minute, at most.", 5)
    elif prev_time < 24 <= time_in:
      speech.show("You're going to go to space in a rocket. But, it's not any rocket.", 5)
    elif prev_time < 34 <= time_in:
      speech.show("You'll go back in time 5 years to 2167.", 5)
    elif prev_time < 43 <= time_in:
      speech.show("There, you have to find out what happened. Why the world is ending.", 5)
    elif prev_time < 53 <= time_in:
      speech.show("And, you know, stop it too.", 5)
    elif prev_time < 61 <= time_in:
      speech.show("Come on. We're all counting on you.", 5)
    elif prev_time < t-25 <= time_in:
      em.go_right(5, 4)
      player.go_right(5, 5)
    elif prev_time < t-20 <= time_in:
      scroll_x.ease_to(70, 6)
      zoom.ease_to(1, 1)
      player.x = -100
    elif prev_time < t - 1 <= time_in: # Wait the rocket launches when the countdown says 1??
                                       # Yes, but the easing function is very slow for the first second.
      rocketpos.ease_to((0, -20), 10)
      cameraPos.ease_to((10, 30), 10)
      zoom.ease_to(3, 10)
    elif prev_time < 118 <= time_in:
      opacity.ease_to(255, 4) # Start fade
    elif prev_time < 126 <= time_in:
      return # Exit
    if frame % (5 - int(max(1,min(4,(time_in - t)/4)))) == 0:
      asteroids.add(AsteroidSprite(world))
      # Eery 5 frames add an asteroid
    # Update everything
    em.clock_tick(time_passed)
    player.clock_tick(time_passed)
    speech.clock_tick(time_passed)
    asteroids.update(time_passed,  max(1,min(4,(time_in - t)/4)))
    npcs.update()
    speech.update()
    # update time stuffs
    zoom.update_time(time_in)
    cameraPos.update_time(time_in)
    scroll_x.update_time(time_in)
    rocketpos.update_time(time_in)
    opacity.update_time(time_in)
    # set values from easers
    game.zoomamount = zoom()
    cpos = cameraPos()
    game.zoompos = (1920//2 + cpos[0] * 16, 1080//2 - cpos[1] * 16)
    world.scrollx = scroll_x() * 16
    asteroids.draw(game.zoom)
    world.render()
    npcs.draw(game.zoom)
    pos = rocketpos()
    pos = (pos[0] + 135, pos[1] + 22)
    # Render
    # Rocket stuff
    if t -1 <= time_in:
      if time_in % 0.3 > 0.2:
        game.zoom.blit(rocket2, (pos[0] * 16 - world.scrollx, pos[1] * 16 - world.scrolly))
      if time_in % 0.3 < 0.1:
        game.zoom.blit(rocket3, (pos[0] * 16 - world.scrollx, pos[1] * 16 - world.scrolly))
      else:
        game.zoom.blit(rocket4, (pos[0] * 16 - world.scrollx, pos[1] * 16 - world.scrolly))
    else:
      game.zoom.blit(rocket, (pos[0] * 16 - world.scrollx, pos[1] * 16 - world.scrolly))
    to_write = max(int(t - time_in), 0)
    txt = font.render(str(to_write), True, (255, 0, 0))
    r = txt.get_rect()
    r.center = 121 * 16 - world.scrollx + 32, 24 * 16 - world.scrolly + 26
    game.zoom.blit(txt, r.topleft)
    game.nozoom.fill((0,0,0,opacity()))
    speechGroup.draw(game.nozoom)
    if constants.SHOW_FPS:
      text = font.render(str(round(clock.get_fps())), True, (255, 0, 0))
      game.nozoom.blit(text, text.get_rect(topright=(1920,0)))
    game.render()
    