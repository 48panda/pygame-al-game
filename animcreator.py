import saras
import tkinter
import tkinter.filedialog
import pygame
import sys

screen = pygame.display.set_mode((1920, 1080))

scales = [0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4]

def prompt_file():
    top = tkinter.Tk()
    top.withdraw()
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

class SpriteState:
  def __init__(self, visible, rotate, scale, pos):
    self.visible = visible
    self.rotate = rotate
    self.scale = scale
    self.pos = pos

  @staticmethod
  def from_string(string):
    version = string[0]
    if version == "1":
      visible = string[1] == "1"
      rotate = int(string[2])
      scale = scales[int(string[3])]
      return SpriteState(visible, rotate, scale)
  
  def __str__(self):
    return f"1{'01'[self.visible]}{self.rotate}{scales.index(self.scale)}{self.pos[0]:+03d}{self.pos[1]:+03d}"
  
  __repr__ = __str__

class Sprite(pygame.sprite.Sprite):
  def __init__(self, filename, frame):
    super().__init__()
    self.image = pygame.image.load(filename)
    self.og = self.image
    self.rect = self.image.get_rect()
    self.scale = 1
    self.rotate = 0
    self.timeline = []
    self.frame = frame
    self.visible = True
  
  def update(self):
    if is_dragging:
      if id(self) == drag_sprite_id:
        self.rect.topleft = (-drag_offset[0] + pygame.mouse.get_pos()[0], -drag_offset[1] + pygame.mouse.get_pos()[1])
  
  def scaleup(self):
    if self.scale != scales[-1]:
      self.scale = scales[scales.index(self.scale) + 1]
      self.updatescale()

  def scaledown(self):
    if self.scale != scales[0]:
      self.scale = scales[scales.index(self.scale) - 1]
      self.updatescale()
  
  def rot(self):
    self.rotate = (self.rotate + 1) % 4
    self.updatescale()
  
  def updatescale(self):
    if self.visible:
      self.image = pygame.transform.scale(self.og, (int(self.og.get_width() * self.scale), int(self.og.get_height() * self.scale)))
      for i in range(self.rotate):
        self.image = pygame.transform.rotate(self.image, 270)
    else:
      self.image = pygame.Surface((0,0))
    self.rect.size = self.image.get_size()
  
  def to_state(self):
    return SpriteState(True, self.rotate, self.scale, self.rect.topleft)
  
  def from_state(self, state):
    self.rotate = state.rotate
    self.scale = state.scale
    self.visible = state.visible
    self.rect.topleft = state.pos
    self.updatescale()

  def next_frame(self, newframe):
    if len(self.timeline) > self.frame:
      self.timeline[self.frame] = self.to_state()
    elif len(self.timeline) == self.frame:
      self.timeline.append(self.to_state())
    else:
      for i in range(len_self.timeline, self.frame):
        self.timeline.append(SpriteState(False, 0, 0))
      self.timeline.append(self.to_state())
    self.frame = newframe
    if len(self.timeline) > newframe:
      self.from_state(self.timeline[newframe])

  def prev_frame(self, newframe):
    if len(self.timeline) > self.frame:
      self.timeline[self.frame] = self.to_state()
    elif len(self.timeline) == self.frame:
      self.timeline.append(self.to_state())
    else:
      for i in range(len_self.timeline, self.frame):
        self.timeline.append(SpriteState(False, 0, 0))
      self.timeline.append(self.to_state())
    self.frame = newframe
    if len(self.timeline) > newframe:
      self.from_state(self.timeline[newframe])



spriteGroup = pygame.sprite.Group()

sprites_in_order = []

images = {}

is_dragging = False
drag_sprite_id = None
drag_offset = (0, 0)
drag_start = (0,0)

is_selected = False
selected_id = None
selected_index = -1
selected_sprite = None

frame = 0

pygame.font.init()
font = pygame.font.SysFont("Calibri", 40)

while True:
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
      if event.key == pygame.K_i:
        filename = prompt_file()
        try:
          sprite = Sprite(filename, frame)
          spriteGroup.add(sprite)
          sprites_in_order.append(sprite)
          if filename in images:
            images[filename].append(sprite)
          else:
            images[filename] = [sprite]
        except FileNotFoundError:
          pass
      if event.key == pygame.K_UP:
        if selected_sprite:
          selected_sprite.scaleup()
      if event.key == pygame.K_DOWN:
        if selected_sprite:
          selected_sprite.scaledown()
      if event.key == pygame.K_r:
        if selected_sprite:
          selected_sprite.rot()
      if event.key == pygame.K_RIGHT:
        frame += 1
        for sprite in sprites_in_order:
          selected_sprite.next_frame(frame)
      if event.key == pygame.K_LEFT:
        frame -= 1
        for sprite in sprites_in_order:
          selected_sprite.prev_frame(frame)
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        for sprite in sprites_in_order[::-1]:
          if sprite.rect.collidepoint(*event.pos):
            is_dragging = True
            drag_sprite_id = id(sprite)
            drag_offset = (event.pos[0]-sprite.rect.left, event.pos[1]-sprite.rect.top)
            drag_start = event.pos
            break
    
    if event.type == pygame.MOUSEBUTTONUP:
      if event.button == 1:
        if drag_start == event.pos:
          is_selected = True
          selected_id = drag_sprite_id
          for i, sprite in enumerate(sprites_in_order):
            if id(sprite) == selected_id:
              selected_index = i
              selected_sprite = sprite
              break
          else:
            raise ValueError()
        is_dragging = False
        drag_sprite_id = None
        drag_offset = (0, 0)
  screen.fill((0,0,0))
  spriteGroup.update()
  spriteGroup.draw(screen)
  if is_selected:
    pygame.draw.rect(screen, (255, 255, 0), selected_sprite.rect, 4)

  txt = font.render(f"Frame {frame}", True, (0, 255, 0))
  screen.blit(txt, (1920 - txt.get_width(), 1080 - txt.get_height()))


  pygame.display.update()
