# A class that eases between 2 numbers, and then lots of variations of it.
class EasingInteger:
    def __init__(self, default):
        self.value = default
        self.start = None
        self.end = None
        self.easing = False
        self.starttime = None
        self.time = 0
        self.duration = None

    def normalsed_function(self, normalised):
        if normalised < 0.5:
            return 4 * normalised**3
        later_half = 2 * normalised - 2
        return 0.5 * later_half**3 + 1

    def get_pos(self):
        t = (self.time - self.starttime) / self.duration
        a = self.normalsed_function(t)
        return self.end * a + self.start * (1 - a)
    
    def ease_to(self, to, duration):
      self.start = self.value
      self.end = to
      self.easing = True
      self.starttime = self.time
      self.duration = duration
    def stop_easing(self):
      if self.easing:
        self.value = self.end
        self.start = None
        self.end = None
        self.easing = False
        self.starttime = None
        self.duration = None
    def update_time(self, time):
      self.time = time
      if not self.starttime:
        return
      if self.easing and time > self.starttime + self.duration:
        self.stop_easing()
      elif self.easing:
        self.value = self.get_pos()

    def __call__(self):
        return self.value

class Easing2dVector:
    def __init__(self, default):
        self.valuex = default[0]
        self.startx = None
        self.endx = None
        self.valuey = default[1]
        self.starty = None
        self.endy = None
        self.easing = False
        self.starttime = None
        self.time = 0
        self.duration = None

    def normalsed_function(self, normalised):
        if normalised < 0.5:
            return 4 * normalised**3
        later_half = 2 * normalised - 2
        return 0.5 * later_half**3 + 1

    def get_posx(self):
        t = (self.time - self.starttime) / self.duration
        a = self.normalsed_function(t)
        return self.endx * a + self.startx * (1 - a)

    def get_posy(self):
        t = (self.time - self.starttime) / self.duration
        a = self.normalsed_function(t)
        return self.endy * a + self.starty * (1 - a)
    
    def ease_to(self, to, duration):
      self.startx = self.valuex
      self.endx = to[0]
      self.starty = self.valuey
      self.endy = to[1]
      self.easing = True
      self.starttime = self.time
      self.duration = duration

    def update_time(self, time):
      self.time = time
      if self.easing and time > self.starttime + self.duration:
        self.valuex = self.endx
        self.valuey = self.endy
        self.startx = None
        self.endx = None
        self.starty = None
        self.endy = None
        self.easing = False
        self.starttime = None
        self.duration = None
      elif self.easing:
        self.valuex = self.get_posx()
        self.valuey = self.get_posy()

    def __call__(self):
        return (self.valuex, self.valuey)

class Easing3dVector:
    def __init__(self, default):
        self.valuex = default[0]
        self.startx = None
        self.endx = None
        self.valuey = default[1]
        self.starty = None
        self.endy = None
        self.valuez = default[2]
        self.startz = None
        self.endz = None
        self.easing = False
        self.starttime = None
        self.time = 0
        self.duration = None

    def normalsed_function(self, normalised):
        if normalised < 0.5:
            return 4 * normalised**3
        later_half = 2 * normalised - 2
        return 0.5 * later_half**3 + 1

    def get_posx(self):
        t = (self.time - self.starttime) / self.duration
        a = self.normalsed_function(t)
        return self.endx * a + self.startx * (1 - a)

    def get_posy(self):
        t = (self.time - self.starttime) / self.duration
        a = self.normalsed_function(t)
        return self.endy * a + self.starty * (1 - a)

    def get_posz(self):
        t = (self.time - self.starttime) / self.duration
        a = self.normalsed_function(t)
        return self.endz * a + self.startz * (1 - a)
    
    def ease_to(self, to, duration):
      self.startx = self.valuex
      self.endx = to[0]
      self.starty = self.valuey
      self.endy = to[1]
      self.startz = self.valuez
      self.endz = to[1]
      self.easing = True
      self.starttime = self.time
      self.duration = duration

    def stop_easing(self):
      if self.easing:
        self.valuex = self.endx
        self.valuey = self.endy
        self.valuez = self.endz
        self.startx = None
        self.endx = None
        self.starty = None
        self.endy = None
        self.startz = None
        self.endz = None
        self.easing = False
        self.starttime = None
        self.duration = None
    def update_time(self, time):
      self.time = time
      if not self.starttime:
        return
      if self.easing and time > self.starttime + self.duration:
        self.stop_easing()
      elif self.easing:
        self.valuex = self.get_posx()
        self.valuey = self.get_posy()
        self.valuez = self.get_posz()

    def __call__(self):
        return (self.valuex, self.valuey, self.valuez)

class QuadraticEasingInteger(EasingInteger):
  def normalsed_function(self, normalised):
    if normalised < 0.5:
      return 2 * normalised * normalised
    return (-2 * normalised * normalised) + (4 * normalised) - 1
class QuadraticEasing2dVector(Easing2dVector):
  def normalsed_function(self, normalised):
    if normalised < 0.5:
      return 2 * normalised * normalised
    return (-2 * normalised * normalised) + (4 * normalised) - 1
class QuadraticEasing3dVector(Easing3dVector):
  def normalsed_function(self, normalised):
    if normalised < 0.5:
      return 2 * normalised * normalised
    return (-2 * normalised * normalised) + (4 * normalised) - 1