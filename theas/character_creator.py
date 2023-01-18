if __name__ == "__main__":
  # testing
  import sys
  from pathlib import Path
  import pygame
  pygame.init()
  directory = Path(__file__)
  sys.path.append(str(directory.parent.parent))
  screen = pygame.display.set_mode((1920, 1080))

import pygame
import engine
import karas
import random
import mono

font = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 30)
# main func
def do_character_creation(screen, clock):
  charCreationVals = engine.character.CharacterCreationValues()
  karas.colorpicker.ColorPicker((0,0))
  done = False
  action = None
  hair= random.randint(1, engine.character.MAX_HAIR)
  top = random.randint(1, engine.character.MAX_TOP )
  # functions to change values on button press
  def increase_hair():
    nonlocal hair
    hair += 1
    if hair == engine.character.MAX_HAIR + 1:
      hair = 1
  def decrease_hair():
    nonlocal hair
    hair -= 1
    if hair == 0:
      hair = engine.character.MAX_HAIR
  def increase_top():
    nonlocal top
    top += 1
    if top == engine.character.MAX_TOP + 1:
      top = 1
  def decrease_top():
    nonlocal top
    top -= 1
    if top == 0:
      top = engine.character.MAX_TOP
  def setDone(to_do):
    nonlocal done
    nonlocal action
    done = True
    action = to_do
  screenshot = pygame.Surface((1920, 1080))
  screenshot.blit(screen, (0,0))
  windowRect = pygame.Rect(0,0,1600,900)
  windowRect.center = 1920//2, 1080//2
  font2 = pygame.font.Font("assets/fonts/Montserrat-ExtraBoldItalic.ttf", 48)
  # Create buttons
  cancelButton = karas.sprite.Button("Cancel", (255, 0, 0), rectoffset=windowRect.topleft, pos=(630, 850), font=font2, text_color=(255,255,255), onClick=lambda:setDone(""))
  nextButton = karas.sprite.Button("Next", (0, 255, 0), rectoffset=windowRect.topleft, pos=(840, 850), font=font2, text_color=(255,255,255), onClick=lambda: setDone(str(charCreationVals)))
  prevHairButton = karas.sprite.Button("\u2039", (32, 32, 32), rectoffset=windowRect.topleft, pos=(1000, 200), font=font2, text_color=(255,255,255), onClick=decrease_hair)
  incHairButton = karas.sprite.Button("\u203A", (32, 32, 32), rectoffset=windowRect.topleft, pos=(1520, 200), font=font2, text_color=(255,255,255), onClick=increase_hair)
  prevTopButton = karas.sprite.Button("\u2039", (32, 32, 32), rectoffset=windowRect.topleft, pos=(1000, 500), font=font2, text_color=(255,255,255), onClick=decrease_top)
  incTopButton = karas.sprite.Button("\u203A", (32, 32, 32), rectoffset=windowRect.topleft, pos=(1550, 500), font=font2, text_color=(255,255,255), onClick=increase_top)

  ButtonGroup = pygame.sprite.Group(cancelButton, nextButton, prevHairButton, incHairButton, prevTopButton, incTopButton)
  # Blit all text to fixed once and display it every frame
  fixed = pygame.Surface((1600, 900))
  fixed.fill((64,64,64))
  fixed.blit(font.render("Skin Color", True, (255,255,255)), (50, 100))
  fixed.blit(font.render("Hair Color", True, (255,255,255)), (50, 300))
  fixed.blit(font.render("Eye Color", True, (255,255,255)), (50, 500))
  fixed.blit(font.render("Top Color", True, (255,255,255)), (550, 100))
  fixed.blit(font.render("Trousers Color", True, (255,255,255)), (550, 300))
  fixed.blit(pygame.font.Font("assets/fonts/Montserrat-ExtraBoldItalic.ttf", 96).render("Create your character", True, (255,255,255)), (0,0)) # This looks epic!
  variable = pygame.Surface((1600, 900), pygame.SRCALPHA)
  # Color pickers
  skin_color = karas.colorpicker.ColorPicker((windowRect.left + 0, windowRect.top + 150), engine.character.SKIN_COLORS)
  hair_color = karas.colorpicker.ColorPicker((windowRect.left + 0, windowRect.top + 350), engine.character.HAIR_COLORS)
  eye_color = karas.colorpicker.ColorPicker((windowRect.left + 0, windowRect.top + 550), engine.character.EYE_COLORS)
  top_color = karas.colorpicker.ColorPicker((windowRect.left + 500, windowRect.top + 150), default=(random.randint(0,359), 100, 50))
  legs_color = karas.colorpicker.ColorPicker((windowRect.left + 500, windowRect.top + 350), default=(random.randint(0,359), 100, 50))
  mono.yes_music()
  while not done:
    clock.tick(30)
    for event in pygame.event.get():
      # pass through color pickers
      if skin_color.event(event): continue
      if hair_color.event(event): continue
      if eye_color.event(event): continue
      if top_color.event(event): continue
      if legs_color.event(event): continue
      for b in ButtonGroup.sprites():
        if b.event(event): break
      else:
        if mono.music_event(event): continue

    screen.blit(screenshot, (0,0))
    ButtonGroup.update()
    variable.fill((0,0,0, 0))
    ButtonGroup.draw(variable)
    # draw color pickers
    variable.blit(skin_color.draw(), (0,150))
    variable.blit(hair_color.draw(), (0,350))
    variable.blit(eye_color.draw(), (0,550))
    variable.blit(top_color.draw(), (500,150))
    variable.blit(legs_color.draw(), (500,350))
    cscale = 16
    im = charCreationVals.getImage()
    # set colors
    charCreationVals.skincolour.rgb(skin_color())
    charCreationVals.haircolour.rgb(hair_color())
    charCreationVals.eyecolour.rgb(eye_color())
    charCreationVals.topcolour.rgb(top_color())
    charCreationVals.legcolour.rgb(legs_color())
    charCreationVals.hair = hair
    charCreationVals.top = top
    # Scale it up to look massive!
    im = pygame.transform.scale(im, (im.get_width() * cscale, im.get_height() * cscale))
    variable.blit(im, (1600 - 20 * cscale * 2, 900-28 * cscale * 2))
    # render
    screen.blit(screenshot, (0,0))
    screen.blit(fixed, windowRect.topleft)
    screen.blit(variable, windowRect.topleft)
    pygame.display.flip()
  return action

if __name__ == "__main__":
  print(do_character_creation(screen, pygame.time.Clock())) # useful for generating appearence strings for NPCs