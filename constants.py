import argparse
import json
import os
import gzip

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="show fps", action="store_true")
parser.add_argument("-C", help="hide cutscene (DEV)", action="store_true")
parser.add_argument("-T", help="skip tutorial (DEV)", action="store_true")
args = parser.parse_args()
SHOW_FPS = args.f
SHOW_CUTSCENE = not args.C
SKIP_TUTORIAL = args.T
WORLDWIDTH = 500
HAS_SAVES = False
CURRENT_FILE_VERSION = 1

SETTINGS = {
  
}

if os.path.exists("data/settings.json"):
  with open("data/settings.json", "r") as f:
    SETTINGS = json.load(f)

if os.path.exists("assets\\chat.json"):
  with open("assets\\chat.json") as f:
    CHAT_DATA = json.load(f)
else:
  with gzip.open("assets\\chat.gzon", "rb") as f:
    CHAT_DATA = json.load(f)