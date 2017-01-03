from cmd import Cmd
import pyglet, os, sys
import os, argparse, random
from time import sleep

import yaml

class MusicPlayer():

    def __init__(self, action):
        super(MusicPlayer, self).__init__()
        self.player = pyglet.media.Player()
        self.current_action = action
        self.current_queue = []

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
        audio_src = pyglet.media.load(audio_file)
        self.player.queue(audio_src)
        self.current_queue.append(os.path.basename(audio_file))

    def list_queue(self):
        for song in self.current_queue:
            print(song)

    def restart_player(self):
        self.player.delete()
        self.player = pyglet.media.Player()
        self.current_queue = []

class PlayerPrompt(Cmd):

    def __init__(self, music_player, music_library):
        super(PlayerPrompt, self).__init__()
        self.music_player = music_player
        self.music_library = music_library

    def do_play(self, args):
        """Start Playing Music"""
        if len(args) > 0:
            self.music_player.queue_song(args)
        self.music_player.play_music()

    def do_pause(self, args):
        """Pause current song"""
        self.music_player.pause_music()

    def do_exit(self, args):
        """Exit Bajao Music Player"""
        self.music_player.delete_player()
        sys.exit()

    def do_add_songs(self, args):
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
        """Shuffle all songs in the Music Library"""
        songs = self.music_library.get_all_songs()
        random.shuffle(songs)
        for song in songs:
            self.music_player.queue_song(song[0])
