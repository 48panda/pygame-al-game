import pygame
import random

pygame.mixer.init()

# Set enums/constants/variable
MUSIC_END_EVENT = pygame.USEREVENT + 0

FIRST = True

DO_MUSIC = False

MUSIC_CHANNEL = pygame.mixer_music

MUSIC_CHANNEL.set_endevent(MUSIC_END_EVENT)

TRACKS = ["assets/sound/music/syncopation.mp3", "assets/sound/music/offbeat.mp3", "assets/sound/music/chill beats.mp3"]

# event handler to play new track
def music_event(event):
  if event.type == MUSIC_END_EVENT and DO_MUSIC:
    MUSIC_CHANNEL.load(random.choice(TRACKS))
    MUSIC_CHANNEL.play()
    return True
# stop music
def no_music():
  global DO_MUSIC
  MUSIC_CHANNEL.stop()
  DO_MUSIC = False
#re-enable music
def yes_music():
  global FIRST
  global DO_MUSIC
  DO_MUSIC = True
  if not MUSIC_CHANNEL.get_busy():
    if FIRST:
      FIRST = False
      MUSIC_CHANNEL.load(TRACKS[1])
    else:
      MUSIC_CHANNEL.load(random.choice(TRACKS))
    MUSIC_CHANNEL.play()