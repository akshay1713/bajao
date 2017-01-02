from cmd import Cmd
import pyglet, os, sys
import os, argparse
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
        print()

    def pause_music(self):
        self.player.pause()
        self.current_action = "paused"

    def delete_player(self):
        self.player.delete()

    def next_song(self):
        self.player.next_source()

    def queue_song(self, audio_file):
        audio_src = pyglet.media.load(audio_file)
        self.player.queue(audio_src)
        print(self.player)
        self.current_queue.append(audio_file)

    def list_queue(self):
        for song in self.current_queue:
            print(song)

class PlayerPrompt(Cmd):

    def __init__(self, music_player):
        print(music_player)
        super(PlayerPrompt, self).__init__()
        self.music_player = music_player

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
