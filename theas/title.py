from saras.easing import *
import karas
import pygame
import copy
import engine
import constants
import theas.loader
import theas.save_chooser
import theas.text_prompt
import theas.character_creator
import olivas
import saras
import mono

buttonFont = pygame.font.Font("assets/fonts/Montserrat-ExtraBoldItalic.ttf", 96)

class Button(karas.sprite.Sprite):
  topLeftAligned = True
  def init(self, text ,foreground, background, pos, bg_hover=None, onClick=None, padding = 3, key=None):
    self.im_nozoom = buttonFont.render(text, True, foreground)
    self.text = text
    self.foreground = foreground
    self.key = key
    self.onClick = onClick
    self.background = background
    self.bg_hover = bg_hover or background
    self.size = QuadraticEasingInteger(0.5)
    self.p = pos
    self.pos = self.p
    self.im = pygame.transform.smoothscale(self.im_nozoom, (self.im_nozoom.get_width() * self.size(), self.im_nozoom.get_height() * self.size()))
    self.bg = QuadraticEasing3dVector((background))
    self.padding = 20
  
  def onupdate(self, time_in, y_add=0):
    self.pos = (self.p[0], self.p[1] + y_add)
    self.size.update_time(time_in)
    self.bg.update_time(time_in)
    if self.rect.collidepoint(*pygame.mouse.get_pos()):
      if self.size() == 0.5 and not self.size.easing:
        self.size.ease_to(0.7, 0.1)
        self.bg.ease_to(self.bg_hover, 0.1)
        self.size.value = 0.501
        self.size.starttime = self.size.time
      elif self.size() == 0.5 or self.size() == 0.7:
        self.size.stop_easing()
        self.bg.stop_easing()
    else:
      if self.size() == 0.7 and not self.size.easing:
        self.size.ease_to(0.5, 0.1)
        self.bg.ease_to(self.background, 0.1)
        self.size.value = 0.699
        self.size.starttime = self.size.time
      elif self.size() == 0.5 or self.size() == 0.7:
        self.size.stop_easing()
        self.bg.stop_easing()
    imsize = (self.im_nozoom.get_width() * self.size(), self.im_nozoom.get_height() * self.size())
    pad = self.padding * self.size()
    self.im = pygame.Surface((pad * 2 + imsize[0], pad * 2 + imsize[1]))
    self.im.fill(self.bg())
    self.im.blit(pygame.transform.smoothscale(self.im_nozoom, imsize), (pad,pad))
  
  def event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        if self.rect.collidepoint(*event.pos):
          if self.onClick:
            self.onClick()
          return True
    if event.type == pygame.KEYDOWN:
      if self.key and self.key == event.key:
        if self.onClick:
          self.onClick()
        return True

def NewGame(loadingScreen, clock, screen):
  savename = theas.text_prompt.prompt_text(screen, "Please enter save name", clock)
  while savename in theas.saver.get_saves():
    savename = theas.text_prompt.prompt_text(screen, "Save name already in use.", clock)
  if savename:
    player_appearance = theas.character_creator.do_character_creation(screen, pygame.time.Clock())
    if player_appearance:
      if constants.SHOW_CUTSCENE:
        saras.cutscene.play_opening_cutscene(loadingScreen, player_appearance, clock)

      loadingScreen.update("Transitioning to Game Class...")
      Game = karas.game.Game(clock, savename)

      loadingScreen = theas.loader.LoadingScreen(Game.game, "Creating NPCs...")
      Game.assign_loading_screen(loadingScreen)
      npcs = olivas.NPCIndex()

      theas.game.run(npcs, Game, loadingScreen, clock, 0, player_appearance=player_appearance)
      raise karas.ReloadTitleScreen()

def LoadGame(loadingScreen, clock, screen):
  savename = theas.save_chooser.do_choose_screen(screen, clock, loadingScreen)
  if savename:
    loadingScreen.update("Transitioning to Game Class...")
    Game = theas.saver.load(savename)
    Game.__init__(clock, savename, hasBeenLoaded=True)

    loadingScreen = theas.loader.LoadingScreen(Game.game, "Creating NPCs...")
    Game.assign_loading_screen(loadingScreen)
    npcs = olivas.NPCIndex()

    theas.game.run(npcs, Game, loadingScreen, clock, 0, isNew=False)
    raise karas.ReloadTitleScreen()

def quitGame():
  raise karas.QuitTriggered()

def do_title_screen(screen, clock, loadingScreen):

  contButton = Button("Continue", (255, 255, 255), (255, 0, 0), (100,100), (255, 128, 128))
  newButton = Button("New Game", (255, 255, 255), (255, 0, 0), (100,100), (255, 128, 128), lambda: NewGame(loadingScreen,clock, screen))
  loadButton = Button("Load Game", (255, 255, 255), (255, 0, 0), (100,100), (255, 128, 128), lambda: LoadGame(loadingScreen, clock, screen))
  settingsButton = Button("Settings", (255, 255, 255), (255, 0, 0), (100,100), (255, 128, 128))
  quitButton = Button("Exit", (255, 255, 255), (255, 0, 0), (100,100), (255, 128, 128), quitGame)
  time_in = 0
  ButtonGroup = pygame.sprite.Group()
  if len(theas.saver.get_saves()) > 0:
    ButtonGroup.add(contButton)
  ButtonGroup.add(newButton)
  if len(theas.saver.get_saves()) > 0:
    ButtonGroup.add(loadButton)
  ButtonGroup.add(settingsButton,quitButton)
  mono.yes_music()
  while True:
    time_passed = clock.tick(30) / 1000
    prev_time = time_in
    time_in += time_passed
    for event in pygame.event.get():
      for b in ButtonGroup.sprites():
        if b.event(event): break
      else:
        if mono.music_event(event): continue
    screen.fill((0,0,0))
    y_pos = 0
    for sprite in ButtonGroup.sprites():
      sprite.update(time_in, y_pos)
      y_pos += sprite.rect.height + 30
    ButtonGroup.draw(screen)
    pygame.display.flip()