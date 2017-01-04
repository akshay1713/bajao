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
        self.music_player.restart_player()
        """Start Playing Music. Enter a music file name or a playlist name with this command"""
        if len(args) > 0:
            if os.path.isfile(args):
                self.music_player.queue_song(args)
            else:
                songs = self.music_library.get_playlist_songs(args)
                for song in songs:
                    self.music_player.queue_song("".join(song))
        else:
            print("Either a song or a playlist name is required")
            return
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
        self.music_player.shuffle()

    def do_queue_playlist(self, args):
        """Add a playlist you created earlier to the current queue"""
        songs = self.music_library.get_playlist_songs(args)
        for song in songs:
            self.music_player.queue_song("".join(song))
    
    # def do_play_playlist(self, args):
        # """Start a playlist you created earlier. Skip the songs, if any, in the current queue"""
        # self.music_player.restart_player()
        # songs = self.music_library.get_playlist_songs(args)
        # for song in songs:
            # self.music_player.queue_song("".join(song))

    # def do_create_playlist(self, args):
        # """Create a new playlist"""
        # self.music_library.create_playlist(args)

    # def do_add_to_playlist(self, args):
        # """Add a song to a playlist"""
        # args_list = self.split_args(args)
        # self.music_library.add_to_playlist(args_list[0], args_list[1])

