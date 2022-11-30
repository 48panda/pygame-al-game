import os
import json
import random
import engine.character
import colour
import olivas.npc
import olivas.quests
import olivas.speech
import pygame
import constants

def randomColor():
  c = colour.hsl2rgb((random.random(), random.uniform(0.5, 1), random.uniform(0.5, 0.75)))
  return (int(c[0]*255),int(c[1]*255),int(c[2]*255))

def createRandomAppearance(gender):
  if gender == "male":
    hair = random.choice(engine.character.MALE_HAIR)
  else:
    hair = random.choice(engine.character.FEMALE_HAIR)
  appearance = engine.character.CharacterCreationValues()
  top = random.randint(1, engine.character.MAX_TOP)
  appearance.top = top
  appearance.hair = hair
  appearance.eyecolor = engine.character.Color(*random.choice(engine.character.EYE_COLORS))
  appearance.haircolor = engine.character.Color(*random.choice(engine.character.HAIR_COLORS))
  appearance.skincolor = engine.character.Color(*random.choice(engine.character.SKIN_COLORS))
  appearance.topcolor = engine.character.Color(*randomColor())
  appearance.legcolor = engine.character.Color(*randomColor())
  return appearance

class NPCIndex:
  def __init__(self):
    if os.path.exists("assets\\special.json"):
      with open("assets\\special.json") as f:
        self.npcs = json.load(f)["npcs"]
    else:
      self.npcs = []
  def generateYearsForNPCs(self, seed):
    random.seed(seed)
    for n in self.npcs:
      if not "appearance" in n:
        n["appearance"] = str(createRandomAppearance(n["gender"]))
      if not "home" in n:
        n["home"] = random.randint(20, constants.WORLDWIDTH-20)
    female, male, last = [], [], []
    with open("assets\\names.csv") as f:
      for name in f.readlines():
        if name[:-1].split(",")[1] == "girl":
          female.append(name[:-1].split(",")[0])
        else:
          male.append(name[:-1].split(",")[0])
    with open("assets\\surnames.csv") as f:
      for name in f.readlines():
        last.append(name[:-1].capitalize())
    for year in range(-10, 2151):
      year = max(year, 0)
      inYear = 0
      for npc in self.npcs:
        if npc["born"] <= year <= npc["died"]:
          inYear += 1
      if inYear < 10:
        age = random.randint(50, 100)
        gender = ["female", "male"][random.getrandbits(1)]
        if gender == "male":
          name = random.choice(male) + " " + random.choice(last)
        else:
          name = random.choice(female) + " " + random.choice(last)

        appearance = createRandomAppearance(gender)
        fail = True
        fails = 0
        while fail:
          fail = False
          home = random.randint(50, constants.WORLDWIDTH-50)
          for npc in self.npcs:
            if npc["born"] <= year <= npc["died"]:
              if npc["home"] - 8 <= home <= npc["home"] + 8:
                fail = True
                break
        does_upgrade = bool(random.getrandbits(1))
        upgrade_time = random.randint(1, 10)
        self.npcs.append({"name": name, "gender": gender, "born": year, "died": min(2172, year + age), "appearance": str(appearance), "home": home, "does_upgrade": does_upgrade, "upgrade_time": upgrade_time})

  def createNPCs(self, world, loadingScreen):
    self.sprites = []
    total = len(self.npcs)
    for i, npc in enumerate(self.npcs):
      self.sprites.append(None)
    return pygame.sprite.Group()

TL_GUI = pygame.image.load("assets/gui/topleft.png").convert()
TL_GUI_FONT = pygame.font.SysFont("Calibri", 16)

class GuideBook:
  def __init__(self, game, linearSpeech):
    self.quests = []
    self.game = game
    self.linearSpeech = linearSpeech
    self.quests.append(olivas.quests.Quest(self,
     "Find 10 Radianite Ore",
     "Radianite is a rare ore found underground. It is a bright orange color.",
     lambda : game.world.player.inventory.num(engine.items.RADIANITE_ORE), toComplete=10,
     start_dialog=[("Mysterious Computer voice", "Well, That's not good... We've landed in the age of the T-rex."), ("Mysterious Computer Voice", "Oh, I'm an Intelligent Communication And Research Unit System by the way, but you can call me ICARUS."), 
                   "Not only did we crash land in time, we also crash landed in space. Let me see what was broken.", "Well, everything seems operational. except for the time travel part.",
                   "The only way to fix the ship is with Radianite. Luckily, it can only be found in the prehistoric era.", "To start with, Collect 10 Radianite Ore. It is found underground, but it should be easily visible from the surface.",
                   "To mine, simply equip your pickaxe and click on the block you want to break."],
     end_dialog=["Great work. That Radianite will be a worthy addition to the ship."]))
    self.quests.append(olivas.quests.Quest(self,
      "Craft 5 Radianite Ingots",
      "Craft Radianite ore into Radianite Ingots by using the inventory menu.",
      lambda: game.world.player.inventory.num(engine.items.RADIANITE_INGOT), toComplete=5,
      start_dialog=["Next you need to process the ore so that it can be used in the ship.", "Press E to open the inventory and click on the recipe to the right hand side of the screen."]))

    self.quest_index = -1
    self.finished = False
  
  def next_quest(self, skip_ending=False):
    if not self.finished:
      if not skip_ending:
        self.quests[self.quest_index].finish()
      self.quest_index += 1
      self.finished = self.quest_index >= len(self.quests)
      if not self.finished:
        self.quests[self.quest_index].activate()

  def update(self):
    if not self.finished:
      if self.quest_index == -1:
        self.next_quest(skip_ending = True)
      currentQuest = self.quests[self.quest_index]
      if currentQuest.is_complete():
        self.next_quest()
      
  def render(self, screen):
    screen.blit(TL_GUI, (0,0))
    time = str(self.game.world.time)
    if time == "-1":
      time = "7000000bc"
    screen.blit(TL_GUI_FONT.render(time, True, (0,255,0)), (10, 10))
    if self.finished:
      qname = "You have saved the world. Just have fun!"
      qprog = 1
    else:
      qname = self.quests[self.quest_index].name
      qprog = self.quests[self.quest_index].progress()
    screen.blit(TL_GUI_FONT.render(qname, True, (0,255,0)), (10, 40))
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(10, 96, int(320*qprog), 30))