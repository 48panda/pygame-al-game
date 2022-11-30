class Quest:
  def __init__(self, guidebook, name, desc, complete_func, start_dialog=[], end_dialog=[], toComplete=1):
    self.name = name
    self.desc = desc
    self.guidebook = guidebook
    self.complete_func = complete_func
    self.start_dialog = start_dialog
    self.end_dialog = end_dialog
    self.time = 0
    self.prev_time = 0
    self.toComplete = toComplete
  
  def activate(self):
    self.guidebook.linearSpeech.add(self.start_dialog, (0, 255, 255))
    
  def is_complete(self):
    return self.complete_func() >= self.toComplete
  
  def progress(self):
    return self.complete_func() / self.toComplete
  
  def finish(self):
    self.guidebook.linearSpeech.add(self.end_dialog, (0,255,255))