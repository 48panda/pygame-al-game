import os
import json
import random
import engine.character
import colour
import olivas.npc
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
    for year in range(2151):
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
        self.npcs.append({"name": name, "gender": gender, "born": year, "died": min(2172, year + age), "appearance": str(appearance), "home": random.randint(20, constants.WORLDWIDTH-20)})

  def createNPCs(self, world, loadingScreen):
    self.sprites = []
    total = len(self.npcs)
    for i, npc in enumerate(self.npcs):
      self.sprites.append(None)
    return pygame.sprite.Group()