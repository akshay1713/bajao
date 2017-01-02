from player import MusicPlayer, PlayerPrompt
from music_library import MusicLibrary
import os, argparse, glob, sys, yaml
from time import sleep

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

    with open("config.yaml", "r") as config_ptr:
        config = yaml.load(config_ptr)
        mp3_files = glob.glob(args.dir+"/*.mp3")
        music_library = MusicLibrary(config["BAJAO_DB"])
        music_library.add_to_library(mp3_files) 
