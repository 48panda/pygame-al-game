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
import gzip

# get a random color
def randomColor():
  c = colour.hsl2rgb((random.random(), random.uniform(0.5, 1), random.uniform(0.5, 0.75)))
  return (int(c[0]*255),int(c[1]*255),int(c[2]*255))

# create a random appearence for a gender (gender is random, only determines this and name)
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
  appearance.haircolour = engine.character.Color(*random.choice(engine.character.HAIR_COLORS))
  appearance.skincolour = engine.character.Color(*random.choice(engine.character.SKIN_COLORS))
  appearance.topcolor = engine.character.Color(*randomColor())
  appearance.legcolor = engine.character.Color(*randomColor())
  return appearance

# Load images for phone
PHONE = pygame.image.load("assets/gui/phone.png").convert_alpha()
TAB = pygame.image.load("assets/gui/tab.png").convert()
TAB_SELECTED = pygame.image.load("assets/gui/tab_selected.png").convert()
TAB_LABELS = pygame.image.load("assets/gui/tab_icons.png").convert_alpha()

# List of all NPCs
class NPCIndex:
  def __init__(self):
    # Load NPCs from json or gzon (to stop people accidentally seeing spoilers)
    if os.path.exists("assets\\special.json"):
      with open("assets\\special.json") as f:
        self.npcs = json.load(f)["npcs"]
    else:
      if os.path.exists("assets\\special.gzon"):
        with gzip.open("assets\\special.gzon", "rb") as f:
          self.npcs = json.load(f)["npcs"]
      else:
        self.npcs = []
  def generateYearsForNPCs(self, seed, homex):
    # Generate all NPC properties
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
          home = random.randint(50, constants.WORLDWIDTH-50)
          if homex - 8 <= home <= homex + 8:
            continue
          fail = False
          for npc in self.npcs:
            if npc["born"] <= year <= npc["died"]:
              if npc["home"] - 8 <= home <= npc["home"] + 8:
                fail = True
                break
        does_upgrade = bool(random.getrandbits(1))
        upgrade_time = random.randint(1, 10)
        self.npcs.append({"name": name, "gender": gender, "born": year, "died": min(2172, year + age), "appearance": str(appearance), "home": home, "does_upgrade": does_upgrade, "upgrade_time": upgrade_time})
  # 
  def createNPCs(self, world, loadingScreen): # Not sure how useful this is but something probably needs it
    self.sprites = []
    total = len(self.npcs)
    for i, npc in enumerate(self.npcs):
      self.sprites.append(None)
    return pygame.sprite.Group()
# load images and fonts more
TL_GUI = pygame.image.load("assets/gui/topleft.png").convert()
TL_GUI_FONT = pygame.font.SysFont("Calibri", 16)

class GuideBook: # Aka the temporal phone and the quest thing in the top right
  def __init__(self, game, linearSpeech, hasBeenLoaded=False):
    self.quests = []
    self.game = game
    self.linearSpeech = linearSpeech
    # quests
    self.quests.append(olivas.quests.Quest(self, "tutorial-1",
     "Find 10 Radianite Ore",
     "Radianite is a rare ore found underground. It is a bright orange color.",
     lambda : game.world.player.inventory.num(engine.items.RADIANITE_ORE), toComplete=10,
     start_dialog=[("Mysterious Computer voice", "Well, That's not good... We've landed in the age of the T-rex."), ("Mysterious Computer Voice", "Oh, I'm an Intelligent Communication And Research Unit System by the way, but you can call me ICARUS."), 
                   "Not only did we crash land in time, we also crash landed in space. Let me see what was broken.", "Well, everything seems operational. except for the time travel part.",
                   "The only way to fix the ship is with Radianite. Luckily, it can only be found in the prehistoric era.", "To start with, Collect 10 Radianite Ore. It is found underground, but it should be easily visible from the surface.",
                   "To mine, simply equip your pickaxe and click on the block you want to break."],
     end_dialog=["Great work. That Radianite will be a worthy addition to the ship."]))
    self.quests.append(olivas.quests.Quest(self, "tutorial-2",
      "Craft 5 Radianite Ingots",
      "Craft Radianite ore into Radianite Ingots by using the inventory menu.",
      lambda: game.world.player.inventory.num(engine.items.RADIANITE_INGOT), toComplete=5,
      start_dialog=["Next you need to process the ore so that it can be used in the ship.", "Press E to open the inventory and click on the recipe to the right hand side of the screen."],
      end_dialog=["Good job. I've repaired all damages to the ship."],
      endFunc= lambda: game.world.player.inventory.remove(engine.items.RADIANITE_INGOT, 5)))
    self.quests.append(olivas.quests.Quest(self, "tutorial-3",
      "Click on the ship to time travel.",
      "Click on the ship to travel in time for your first time!",
      olivas.quests.CodeCompletion, toComplete=1,
      start_dialog=["There is a problem, though. You've left a hole in the ground!", "Traveling back in time removes all changes you've made in years since then.", "I'll control the destination, just click on the ship and we'll go back a year."],
      end_dialog=["Great. Problem fixed. Because of this, if you want to build a permanent base, I strongly recommend building it in 1ad, as that's the furthest back the ship will go after this trip."]))
    self.quests.append(olivas.quests.Quest(self, "2022-1",
          "Travel to the year 2022 and talk to locals.",
          "Use the keypad to go to the year 2022.",
          olivas.quests.CodeCompletion, toComplete=1,
          start_dialog=["We need to work out what happened back in 2172. Let's go to 2022. It's somewhat close, but far away enought that we'll be safe."]))
    self.quests.append(olivas.quests.Quest(self, "1125-1",
          "Travel to the year 1125 and talk to Roy.",
          "Use the keypad to go to the year 1125.",
          olivas.quests.CodeCompletion, toComplete=1,
          start_dialog=["Well then, off we go to 1125!"],
          end_dialog=["Great! Why don't you try and work out the puzzle.", ("TIP", "You can press the Windows button or ALT+TAB to access your browser if you don't happen to know these very specific facts", (255,255,0)),
          ("NOTICE", "As of v1a, The storyline ends here.", (255,0,0))]))
    # initialise constants
    self.finished = False
    self.phone_open = False
    if not hasBeenLoaded:
      self.quest_index = -1
      self.phone_tab = 0
      self.notes_image_path = "assets/gui/blueprint.png"
    self.notes_image = pygame.image.load(self.notes_image_path).convert()
    if self.quest_index >= len(self.quests):
      self.quest_id = "finished"
      self.finished = True
    else:
      self.quest_id = self.quests[self.quest_index].id
  
  def __getstate__(self):
    return (1, self.quest_index, self.phone_tab, self.notes_image_path)
  
  def __setstate__(self, state):
    if state[0] == 1:
      version, self.quest_index, self.phone_tab, self.notes_image_path = state
      self.notes_image = pygame.image.load(self.notes_image_path).convert()    
  
  def next_quest(self, skip_ending=False):
    # go to next quest or finished state if finished
    if not self.finished:
      if not skip_ending:
        self.quests[self.quest_index].finish()
      self.quest_index += 1
      self.finished = self.quest_index >= len(self.quests)
      if not self.finished:
        self.quest_id = self.quests[self.quest_index].id
        self.quests[self.quest_index].activate()
      else:
        self.quest_id = "finished"

  def update(self):
    #go to next quest if needed
    if not self.finished:
      if self.quest_index == -1 or (constants.SKIP_TUTORIAL and self.quest_index < 3):
        self.next_quest(skip_ending = True)
      currentQuest = self.quests[self.quest_index]
      if currentQuest.is_complete():
        self.next_quest()

  def event(self, event):
    # open phone (press G, not used in game yet but still exists)
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_g:
        self.phone_open = not self.phone_open
        return True
      
  def render(self, screen):
    # draw the thing in the top left
    screen.blit(TL_GUI, (0,0))
    time = str(self.game.world.time)
    if time == "-1":
      time = "70632022bc"
    if time == "-2":
      time = "70632023bc"
    screen.blit(TL_GUI_FONT.render(time, True, (0,255,0)), (10, 10))
    if self.finished:
      qname = "The game is still in alpha, the story is over (for now!)"
      qprog = 1
    else:
      qname = self.quests[self.quest_index].name
      qprog = self.quests[self.quest_index].progress()
    screen.blit(TL_GUI_FONT.render(qname, True, (0,255,0)), (10, 40))
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(10, 96, int(320*qprog), 30))
    
    if self.phone_open:
      tl = PHONE.get_rect(center=(960, 540)).topleft
      screen.blit(PHONE, tl)
      for i in range(3):
        if self.phone_tab == i:
          screen.blit(TAB_SELECTED, (tl[0] + 50 + 150*i, tl[1] + 50))
        else:
          screen.blit(TAB, (tl[0] + 50 + 150*i, tl[1] + 50))
      screen.blit(TAB_LABELS, (tl[0] + 50, tl[1] + 50))
      if self.phone_tab == 0:
        screen.blit(self.notes_image, (tl[0] + 50, tl[1] + 100))
      