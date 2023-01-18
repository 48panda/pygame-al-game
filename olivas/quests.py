# Class to describe a quest
class Quest:
  def __init__(self,guidebook,  my_id, name, desc, complete_func, start_dialog=[], end_dialog=[], toComplete=1,endFunc=None):
    self.id = my_id
    self.name = name
    self.desc = desc
    self.guidebook = guidebook
    self.complete_func = complete_func
    self.start_dialog = start_dialog
    self.end_dialog = end_dialog
    self.time = 0
    self.prev_time = 0
    self.toComplete = toComplete
    self.endFunc = endFunc
  
  def activate(self):
    self.guidebook.linearSpeech.add(self.start_dialog, (0, 255, 255))
    
  def is_complete(self):
    return self.complete_func() >= self.toComplete
  
  def progress(self):
    return self.complete_func() / self.toComplete
  
  def finish(self):
    if self.endFunc:
      self.endFunc()
    self.guidebook.linearSpeech.add(self.end_dialog, (0,255,255))

def CodeCompletion():
  # A quest condition which requires the game's code to trigger next_quest.
  return 0