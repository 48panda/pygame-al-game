import os
import constants
import pickle

saves_path = "data/saves/"

import gzip
import pickle
import fnmatch

if not os.path.exists(saves_path):
    os.makedirs(saves_path)

def get_saves():
  file_list = os.listdir(saves_path)
  return [i[:-4] for i in fnmatch.filter(file_list, '*.ccs')]
  
def save(game):
    filepath = os.path.join(saves_path, f"{game.savename}.ccs")
    with gzip.GzipFile(filepath, "wb") as f:
      pickle.dump(game, f)

def load(savename):
  filepath = os.path.join(saves_path, f"{savename}.ccs")
  with gzip.GzipFile(filepath, "rb") as f:
    game = pickle.load(f)
  return game