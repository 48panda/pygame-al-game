import pygame
import random

def rgbToHsl(rgb):
  c = pygame.Color(*rgb)
  return c.hsla[:3]

class ColorPicker:
  def __init__(self, pos, presets=[], default = None):
    self.hue = 0
    self.saturation = 100
    self.lightness = 50
    self.pos = pos
    self.held_slider = -1
    self.mouse_rel = 0
    self.circles = []
    self.colour = pygame.Color(0)
    if default or presets:
      self.hue, self.saturation, self.lightness = default or rgbToHsl(random.choice(presets))
    self.presets = {c:(pygame.Rect(i*30+50,15,20,20)) for i, c in enumerate(presets)}

  def draw_bar(self, surf, vary, varyamount, height=25):
    # Draws one of those bars on the color picker where every pixel is a different color.
    colour = [self.hue, self.saturation ,self.lightness, 100]
    c = pygame.Color(0,0,0,0)
    for x in range(50,350):
      val = int((varyamount * ((x-50) / 300)))
      colour[vary] = val
      c.hsla = colour
      pygame.draw.rect(surf, c, (x, height-5, 1, 10))

  def event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      for i, circle in enumerate(self.circles):
        # If clicked circle, set it to held and store where on the button it is held
        if ((event.pos[0] - self.pos[0] - circle[0]) ** 2 + (event.pos[1] - self.pos[1] - circle[1]) ** 2) ** 0.5 <= 10:
          self.held_slider = i
          self.mouse_rel = circle[0] - (event.pos[0] - self.pos[0])
          return True
      # If clicked preset, set colors to preset.
      for colour, rect in self.presets.items():
        if rect.collidepoint(event.pos[0] - self.pos[0], event.pos[1] - self.pos[1]):
          self.hue, self.saturation, self.lightness = rgbToHsl(colour)
          return True
    if event.type == pygame.MOUSEBUTTONUP:
      # No longer holding any sliders
      if self.held_slider != -1:
        self.held_slider = -1
        return True

  def draw(self):
    max_val=[360, 100, 100]
    if self.held_slider != -1:
      new_circle_x = pygame.mouse.get_pos()[0] - self.pos[0] + self.mouse_rel - 50
    if self.held_slider == 0:
      self.hue = max(0, min(360, 360*new_circle_x/300))
    if self.held_slider == 1:
      self.saturation = max(0, min(100, 100*new_circle_x/300))
    if self.held_slider == 2:
      self.lightness = max(0, min(100, 100*new_circle_x/300))
    # Draw bars
    surf = pygame.Surface((400, 125))
    self.draw_bar(surf, 0, 360, 50)
    self.draw_bar(surf, 1, 100, 75)
    self.draw_bar(surf, 2, 100,100)
    self.colour = pygame.Color(0)
    self.colour.hsla = [self.hue, self.saturation ,self.lightness, 100]
    self.circles = []
    # draw circles
    for i, v in enumerate([self.hue, self.saturation, self.lightness]):
      x = int(300 * v / max_val[i]) + 50
      y = i*25 + 50
      pygame.draw.circle(surf, self.colour, (x,y), 10)
      self.circles.append((x, y))
    # Draw presets
    for colour, rect in self.presets.items():
      pygame.draw.rect(surf, colour, rect)
    return surf
  
  def __call__(self):
    # return the rgb colours
    return self.colour.r, self.colour.g, self.colour.b

if __name__=="__main__":
  # Testing
  screen = pygame.display.set_mode((500,225))
  cPicker = ColorPicker((100,100))
  while True:
    for event in pygame.event.get():
      if cPicker.event(event): continue
    screen.fill(cPicker())
    screen.blit(cPicker.draw(), (100,100))
    pygame.display.update()