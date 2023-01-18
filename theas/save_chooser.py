import pygame
import karas
import theas.title
import mono

smallfont = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 30)

# Button
class Button(karas.sprite.Sprite):
  topLeftAligned = True
  hover = True
  def init(self, text ,foreground, background, pos, bg_hover=None, onClick=None, padding = 3, key=None, font=smallfont):
    im = font.render(text, True, foreground)
    self.im = pygame.Surface((padding * 2 + im.get_size()[0], padding * 2 + im.get_size()[1]))
    self.im.fill(background)
    self.im.blit(im, (padding,padding))
    self.hoverim = pygame.Surface((padding * 2 + im.get_size()[0], padding * 2 + im.get_size()[1]))
    self.hoverim.fill(bg_hover)
    self.hoverim.blit(im, (padding,padding))
    self.key = key
    self.onClick = onClick
    self.p = pos
    self.pos = self.p
    self.text = text
  
  def onupdate(self, time_in, y_add=0, scroll=0):
    if self.rectoffset[0] != 0:
      self.pos = (self.p[0], self.p[1] + y_add)
      self.rectoffset = (670, 70 - scroll)

  def event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        if self.rect.collidepoint((event.pos[0] - self.rectoffset[0], event.pos[1] - self.rectoffset[1])):
          if self.onClick:
            self.onClick()
          return True
    if event.type == pygame.KEYDOWN:
      if self.key and self.key == event.key:
        if self.onClick:
          self.onClick()
        return True

def do_choose_screen(screen, clock, loadingScreen):
  done = False
  action = None
  def setDone(to_do):
    nonlocal done
    nonlocal action
    done = True
    action = to_do
  backButton = Button("X", (255, 255, 255), (255, 0, 0), (670, 70), (255, 128, 128), padding=10, onClick=lambda:setDone(""))
  lvlbtns = [Button(i, (255, 255, 255), (255, 0, 0), (0,80), (255, 128, 128), padding=10, onClick=lambda:setDone(i), rectoffset=(670,70)) for i in theas.saver.get_saves()]
  screen_size =sum([i.im.get_height() + 10 for i in lvlbtns]) - 10 + 80
  screen_width = 580
  small_screen = pygame.Surface((screen_width, screen_size))
  time_in = 0
  ButtonGroup = pygame.sprite.Group(*lvlbtns)
  BackButtonGroup = pygame.sprite.GroupSingle(backButton)
  screenshot = pygame.Surface((1920, 1080))
  screenshot.blit(screen, (0,0))
  scroll = 0
  mono.yes_music()
  while not done:
    clock.tick(30)
    time_passed = clock.tick(30) / 1000
    prev_time = time_in
    time_in += time_passed
    for event in pygame.event.get():
      if backButton.event(event): continue
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 5:
          scroll += 30
          scroll = max(min(scroll, screen_size-940), 0)
          continue
        if event.button == 4:
          scroll -= 30
          scroll = max(scroll, 0)
          continue
      for b in ButtonGroup.sprites():
        if b.event(event): break
      else:
        if mono.music_event(event): continue
    screen.blit(screenshot, (0,0))
    max_w = 0
    y_pos = 0
    for sprite in ButtonGroup.sprites():
      sprite.update(time_in, y_pos, scroll)
      y_pos += sprite.rect.height + 10
      max_w = max(max_w, sprite.rect.width)
    BackButtonGroup.update(time_in, 0, 0)
    small_screen.fill((192,192,192))
    ButtonGroup.draw(small_screen)
    screen.blit(small_screen, (670, 70), area=(0,scroll,580, 940))
    pygame.draw.rect(screen, (255, 255, 255), (670,70,580, 70))
    BackButtonGroup.draw(screen)
    pygame.display.flip()
  return action