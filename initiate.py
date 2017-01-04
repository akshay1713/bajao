from player import MusicPlayer, PlayerPrompt
from music_library import MusicLibrary
import os, argparse, glob, sys, yaml, argcomplete
from time import sleep

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
argcomplete.autocomplete(parser)
parser.add_argument('-a', '--action', default='start', help = "start - Start Bajao Music Player \
        \nadd - Add Files in a directory to Bajao Music Library. To be used along with the 'dir' argument \
        \ncreate-playlist - Create a playlist. To be used along with the 'playlist-name' argument \
        \nadd-to-playlist - Add a song to a playlist. To be used along with 'playlist-name' argument. \
        \n\tAccepts full filenames (with extension) or directories. If a directory is passed as argument, \
        \n\tAll songs in the directory will be added to the given playlist.")

parser.add_argument('-d', '--dir', default='', help = "The directory from which all mp3 files are to be added to Bajao Music Library")
parser.add_argument('-pn', '--playlist-name', default='', help = "The name of the playlist to be created")
parser.add_argument('-s', '--songs', default='', nargs='*', help = "Songs to be added. Also accepts directories.")
args = parser.parse_args()
config = {}

with open("config.yaml", "r") as config_ptr:
    config = yaml.load(config_ptr)

music_library = MusicLibrary(config["BAJAO_DB"])
if args.action == "start":
    music_player = MusicPlayer("initialized")
    while True:
        music_library = MusicLibrary(config["BAJAO_DB"])
        player_prompt = PlayerPrompt(music_player, music_library)
        player_prompt.prompt = "bajao>"
        player_prompt.cmdloop("Starting Bajao Music Player")

elif args.action == "add":
    print("adding files")
    if not os.path.isdir(args.dir):
        print("Please specify a valid directory using the --dir option")
        sys.exit()
    mp3_files = glob.glob(args.dir+"/*.mp3")
    music_library = MusicLibrary(config["BAJAO_DB"])
    music_library.add_to_library(args.dir, mp3_files) 

elif args.action == "create-playlist":
    if not args.playlist_name:
        print("Please specify a playlist name using the --playlist-name or -pn option")
        sys.exit()
    music_library.create_playlist(args.playlist_name) 

elif args.action == "add-to-playlist":
    if not args.songs or not args.playlist_name:
        print("Please specify the playlist name using the --playlist-name or -pn option, \
                \nand at least one song name(in the current directory) or a directory using the --songs or -s option")
        sys.exit()
    mp3_files = []
    for song in args.songs:
        if os.path.isfile(song):
            mp3_files.append(song)
        elif os.path.isdir(song):
            dir_mp3_files = glob.glob(song+"/*.mp3")
            mp3_files += dir_mp3_files
    for mp3_file in mp3_files:
        music_library.add_to_playlist(mp3_file, args.playlist_name)



