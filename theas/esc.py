import theas.title
import pygame
import mono

def do_esc_screen(screen, clock, loadingScreen):
  done = False
  action = None
  def setDone(to_do):
    nonlocal done
    nonlocal action
    done = True
    action = to_do
  screenshot = pygame.Surface((1920, 1080))
  screenshot.blit(screen, (0,0))
  contButton = theas.title.Button("Continue", (255, 255, 255), (255, 0, 0), (100,100), (255, 128, 128), lambda: setDone("cont"), key=pygame.K_ESCAPE)
  #settingsButton = theas.title.Button("Settings", (255, 255, 255), (255, 0, 0), (100,100), (255, 128, 128))
  # No settings yet!
  quitButton = theas.title.Button("Exit world", (255, 255, 255), (255, 0, 0), (100,100), (255, 128, 128), lambda: setDone("save"))
  time_in = 0
  ButtonGroup = pygame.sprite.Group(contButton,quitButton)
  mono.yes_music()
  while not done:
    # timings
    time_passed = clock.tick(30) / 1000
    prev_time = time_in
    time_in += time_passed

    for event in pygame.event.get():
      for b in ButtonGroup.sprites():
        if b.event(event): break
      else:
        if mono.music_event(event): continue

    screen.blit(screenshot, (0,0))
    y_pos = 0
    max_w = 0
    # move down if one expands
    for sprite in ButtonGroup.sprites():
      sprite.update(time_in, y_pos)
      y_pos += sprite.rect.height + 30
      max_w = max(max_w, sprite.rect.width)
    pygame.draw.rect(screen, (0,0,0), (70, 70, max_w + 60, y_pos + 30))
    ButtonGroup.draw(screen)
    pygame.display.flip()
  return action