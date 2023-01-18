import karas
import pygame

# Draws text that wraps
def draw_text(surface, text, color, rect, font, aa=True, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = -2
    font_height = font.size("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")[1]
    while text:
        i = 1
        if y + font_height > rect.bottom:
            break
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing
        text = text[i:]
    return text

# A dialogue bubble.
class speech(karas.sprite.Sprite):
  def init(self):
    self.font = pygame.font.SysFont("Courier", 30)
    self.smallfont = pygame.font.SysFont("Courier", 20)
    self.time = 0
    self.char = 0
    self.text = ""
    self.duration = 0
    self.surf = pygame.Surface((800, 300))
    self.all_showing = False
    self.pos = (1920//2, 1080*3//4)
    self.im = pygame.Surface((0,0))
    self.hidden = True
    self.color = (255, 255, 255)
    self.infinite = False
    self.showing_click_text = False
    
  def show(self, text, time_when_appeared, color=(255,255,255), saying=""):
    # set variables to show dialogue
    self.text = text
    self.duration = time_when_appeared if time_when_appeared else 1
    self.infinite = time_when_appeared == None
    self.im = self.surf.copy()
    self.char = 0
    self.all_showing = False
    self.hidden = False
    self.time = 0
    self.color = color
    self.showing_click_text = False
    self.saying = saying
  
  def draw_clicking_text(self):
    # Draw click to continue
    clicktxt = self.smallfont.render("Click to continue.", True, self.color)
    self.im.blit(clicktxt, clicktxt.get_rect(bottomright = self.im.get_rect().bottomright))
    self.showing_click_text = True
  
  def onupdate(self):
    if self.hidden:
      return
    if self.all_showing:
      if self.time <= 0:
        # If finished dialogue and not showing clicking text, draw it.
        if self.infinite:
          if not self.showing_click_text:
            self.draw_clicking_text()
        else:
          self.close()
    else:
      # if all characters show, it is all displayed
      if self.char >= len(self.text):
        self.time = self.duration
        self.all_showing = True
        return
      # while text needs to appear, draw it.
      while self.time <= 0:
        self.time += 0.05
        self.char += 1
        while self.char < len(self.text) and self.text[self.char] == " ":
          self.char += 1
        self.im.fill((0,0,0))
        self.im.blit(self.font.render(self.saying, True, self.color), (0,0))
        draw_text(self.im, self.text[:self.char], self.color, pygame.Rect(30, 30, 740, 240), self.font)

  def close(self):
    self.im = pygame.Surface((0,0))
    self.hidden = True

  def clock_tick(self, time):
    self.time -= time

class LinearSpeech:
  # A collection of tuples to be sent in order to a speech
  def __init__(self, speech):
    self.speech = speech
    self.text = []
  
  def add(self, textlist, color, speaker="Icarus"):
    # Add them, with defaults given by parameters
    for i in textlist:
      if type(i) == str:
        self.text.append((i, color, speaker))
      else:
        if len(i) == 2:
          self.text.append((i[1], color, i[0]))
        if len(i) == 3:
          self.text.append((i[1],i[2],i[0]))
    if self.speech.hidden and len(self.text):
      text = self.text.pop(0)
      self.speech.show(text[0], None, text[1], text[2])

  def update(self, td):
    pass

  def event(self, event):
    if self.speech.hidden:
      return False
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        if self.speech.showing_click_text:
          # If showing clicking text, go to next
          if len(self.text) == 0:
            # If no more text hide speech bubble
            self.speech.close()
            return True
          # get next text
          text = self.text.pop(0)
          #display it
          self.speech.show(text[0], None, text[1], text[2])
          return True
        else:
          # Display all characters
          self.speech.char = len(self.speech.text) - 1
          self.speech.all_showing = True
          draw_text(self.speech.im, self.speech.text, self.speech.color, pygame.Rect(30, 30, 740, 240), self.speech.font)
          self.speech.draw_clicking_text()
          return True