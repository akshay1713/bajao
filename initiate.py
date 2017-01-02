from player import MusicPlayer, PlayerPrompt
from music_library import MusicLibrary
import os, argparse
from time import sleep
import glob, sys

import yaml

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-a', '--action', default='start', help = "start - Start Bajao Music Player \nadd - Add Files in a directory to Bajao Music Library. To be used along with the 'dir' argument")
parser.add_argument('-d', '--dir', default='', help = "The directory from which all mp3 files are to be added to Bajao Music Library")
args = parser.parse_args()

if args.action == "start":
    pm = MusicPlayer("initialized")
    while True:
        player_prompt = PlayerPrompt(pm)
        player_prompt.prompt = "bajao>"
        player_prompt.cmdloop("Starting Bajao Music Player")

elif args.action == "add":
    print("adding files")
    
    if not os.path.isdir(args.dir):
        print("Please specify a valid directory using the -dir option")
        sys.exit()

    mp3_files = glob.glob(args.dir+"/*.mp3")
    music_library = MusicLibrary("bajao.db")
    music_library.add_to_library(mp3_files) 
