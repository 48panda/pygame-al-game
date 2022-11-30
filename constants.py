import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="show fps", action="store_true")
parser.add_argument("-c", help="show cutscene (DEV)", action="store_true")
args = parser.parse_args()
SHOW_FPS = args.f
SHOW_CUTSCENE = args.c
WORLDWIDTH = 500