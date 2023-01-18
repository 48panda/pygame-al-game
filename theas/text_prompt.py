import theas.title
import karas
import pygame
import mono

# Asks user for a save name

def prompt_text(screen, text, clock):
  done = False
  action = None
  def setDone(to_do):
    nonlocal done
    nonlocal action
    done = True
    action = to_do
  screenshot = pygame.Surface((1920, 1080))
  screenshot.blit(screen, (0,0))
  cancelButton = karas.sprite.Button("Cancel", (255, 0, 0), pos=(750, 700), font=pygame.font.Font("assets/fonts/Montserrat-ExtraBoldItalic.ttf", 48), text_color=(255,255,255), onClick=lambda:setDone(""))
  submitButton = karas.sprite.Button("Submit", (0, 255, 0), pos=(960, 700), font=pygame.font.Font("assets/fonts/Montserrat-ExtraBoldItalic.ttf", 48), text_color=(255,255,255))
  submitButton.update()
  textInput = karas.textbox.TextInput(pygame.font.Font("assets/fonts/Montserrat-ExtraBoldItalic.ttf", 30), (750, 500), (255,255,0), 210 + submitButton.rect.width, (100, 100, 100))
  submitButton.onclick=lambda:setDone(textInput.text)
  textInputGroup = pygame.sprite.GroupSingle(textInput)
  topText = pygame.font.Font("assets/fonts/Montserrat-ExtraBoldItalic.ttf", 30).render(text, True, (255,255,255))
  ButtonGroup = pygame.sprite.Group(cancelButton, submitButton)
  mono.yes_music()
  while not done:
    clock.tick(30)
    for event in pygame.event.get():
      if textInput.event(event): continue
      for b in ButtonGroup.sprites():
        if b.event(event): break
      else:
        if mono.music_event(event): continue

    screen.blit(screenshot, (0,0))
    ButtonGroup.update()
    textInputGroup.update()
    pygame.draw.rect(screen, (192,192,192), (700, 400, 310 + submitButton.rect.width, 350))
    screen.blit(topText, (750, 450))
    ButtonGroup.draw(screen)
    textInputGroup.draw(screen)
    pygame.display.flip()
  return action