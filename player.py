from cmd import Cmd
import pyglet, os, sys, re
import os, argparse, random
from time import sleep

import yaml

class MusicPlayer():

    def __init__(self, action):
        super(MusicPlayer, self).__init__()
        self.player = pyglet.media.Player()
        self.current_action = action
        self.current_queue = []

    def delete_player(self):
        self.player.delete()

    def play_music(self):
        self.player.play()
        self.current_action = "playing"

    def pause_music(self):
        self.player.pause()
        self.current_action = "paused"

    def next_song(self):
        self.player.next_source()
        self.current_queue.pop(0)

    def queue_song(self, audio_file):
        print(audio_file)
        audio_src = pyglet.media.load(audio_file)
        self.player.queue(audio_src)
        self.current_queue.append(audio_file)

    def list_queue(self):
        for song in self.current_queue:
            print(os.path.basename(song))

    def restart_player(self):
        self.player.delete()
        self.player = pyglet.media.Player()
        self.current_queue = []
        self.current_action = "initialized"

    def shuffle(self):
        queue = self.current_queue
        random.shuffle(queue)
        self.restart_player()
        for song in queue:
            self.queue_song(song)
        self.play_music()

class PlayerPrompt(Cmd):

    def __init__(self, music_player, music_library):
        super(PlayerPrompt, self).__init__()
        self.music_player = music_player
        self.music_library = music_library

    def split_args(self, args):
        return [re.sub("\"","",p) for p in re.split("( |\\\".*?\\\"|'.*?')", args) if p.strip()]

    def do_play(self, args):
        """Start Playing Music. Enter a music file name or a playlist name with this command"""
        self.music_player.restart_player()
        if len(args) == 0:
            print("At least one song or playlist name is required")
            return
        mp3_files = []
        args_passed = self.split_args(args)

        for arg in args_passed:
            if os.path.isfile(arg):
                mp3_files.append(arg)
                continue
            song_from_library =  self.music_library.get_song(arg)
            if song_from_library:
                mp3_files.append(song_from_library)
                continue
            songs = self.music_library.get_playlist_songs(arg)
            if songs:
                mp3_files = mp3_files + songs
                continue
            print("Invalid argument ", arg,". Couldn't find either a playlist with that name, \
                    or a song in the music library, or in the specified path")

        print("files found ", mp3_files)
        for mp3_file in mp3_files:
            self.music_player.queue_song(mp3_file)
        # if os.path.isfile(args):
            # self.music_player.queue_song(args)
        # else:
            # songs = self.music_library.get_playlist_songs(args)
            # for song in songs:
                # self.music_player.queue_song("".join(song))
        self.music_player.play_music()

    def do_pause(self, args):
        """Pause current song"""
        self.music_player.pause_music()

    def do_exit(self, args):
        """Exit Bajao Music Player"""
        self.music_player.delete_player()
        sys.exit()

    def do_add(self, args):
        """Add songs to current player queue"""
        self.music_player.queue_song(args)

    def do_next(self, args):
        """Play next song in queue, skip current one"""
        self.music_player.next_song()

    def do_list_queue(self, args):
        """List songs in current queue"""
        self.music_player.list_queue()

    def do_delete_queue(self, args):
        """Delete current queue, so you can create a new one"""
        self.music_player.restart_player()

    def do_shuffle(self, args):
        """Shuffle all songs in the current queue"""
        self.music_player.shuffle()

    def do_queue_playlist(self, args):
        """Add a playlist you created earlier to the current queue"""
        songs = self.music_library.get_playlist_songs(args)
        for song in songs:
            self.music_player.queue_song("".join(song))
    

