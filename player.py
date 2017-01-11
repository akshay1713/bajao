from cmd import Cmd
import pyglet
import os
import sys
import re
import math
import random
import threading
from time import sleep


class PlayerQueueManager(object):

    def __init__(self, player, interval=1):
        self.interval = interval
        self.player = player

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        jump_actions = ["next", "prev"]
        while True:
            current_action = self.player.get_action()
            if current_action == "paused":
                continue
            if current_action == "playing":
                self.check_is_playing()
            elif current_action in jump_actions:
                self.player.update_queue(current_action)
                self.player.play_music()

    def check_is_playing(self):
        current_time = self.player.get_time()
        is_playing = True
        sleep(1)
        current_action = "playing"
        while is_playing and current_action == "playing":
            is_playing = not math.isclose(
                current_time, self.player.get_time(), abs_tol=0.00003)
            current_time = self.player.get_time()
            current_action = self.player.get_action()
            sleep(1)
        if current_action == "playing":
            self.player.set_action("next")
        return


class MusicPlayer():

    def __init__(self, action):
        super(MusicPlayer, self).__init__()
        self.player = pyglet.media.Player()
        self.current_action = action
        self.current_queue = []
        self.played_queue = []
        self.manager = PlayerQueueManager(self)
        self.repeat_status = 0

    def get_time(self):
        return self.player.time

    def set_action(self, action):
        self.current_action = action

    def get_action(self):
        return self.current_action

    def delete_player(self):
        self.player.delete()

    def play_music(self):
        if len(self.current_queue) == 0:
            print("No more songs in queue")
            self.player.current_action = "finished"
            return
        audio_file = self.current_queue[0]
        audio_src = pyglet.media.load(audio_file)
        self.current_duration = audio_src.duration
        self.player.queue(audio_src)
        self.current_action = "playing"
        self.player.play()
        return

    def update_queue(self, update_type="next"):
        if update_type == "next":
            finished_song = self.current_queue.pop(0)
            self.played_queue.append(finished_song)
            self.player.delete()
            self.player = pyglet.media.Player()
            if(len(self.current_queue) == 0):
                if self.repeat_status == 0:
                    self.current_queue = self.played_queue
                    self.played_queue = []
                else:
                    self.current_action = "finished"
                    return
        elif update_type == "prev":
            if(len(self.played_queue) == 0):
                print("No previous songs")
                return
            previous_song = self.played_queue.pop(len(self.played_queue) - 1)
            self.current_queue.insert(0, previous_song)
            self.player.delete()
            self.player = pyglet.media.Player()
        return

    def get_queue(self):
        return self.current_queue

    def pause_music(self):
        self.current_action = "paused"
        self.player.pause()

    def next_song(self):
        self.set_action("next")
        self.player.pause()

    def prev_song(self):
        self.set_action("prev")

    def queue_song(self, audio_file):
        self.current_queue.append(audio_file)

    def get_list(self, list_type):
        songs_list = []
        songs_queue = []
        if(list_type == "next"):
            songs_queue = self.current_queue
        elif(list_type == "previous"):
            songs_queue = self.played_queue
        for song in songs_queue:
            songs_list.append(os.path.basename(song))
        return songs_list

    def restart_player(self):
        self.player.delete()
        self.player = pyglet.media.Player()
        self.current_queue = []
        self.current_action = "initialized"

    def shuffle(self):
        queue = self.current_queue + self.played_queue
        random.shuffle(queue)
        self.current_queue = queue

    def set_repeat(self, repeat_status):
        self.repeat_status = repeat_status


class PlayerPrompt(Cmd):

    def __init__(self, music_player, music_library):
        super(PlayerPrompt, self).__init__()
        self.music_player = music_player
        self.music_library = music_library
        self.song_names = []

    def split_args(self, args):
        return [re.sub("\"", "", p) for p in re.split("( |\\\".*?\\\"|'.*?')", args) if p.strip()]

    def add_to_queue(self, args):
        current_queue = self.music_player.get_queue()

        if len(args) == 0 and len(current_queue) == 0:
            return
        mp3_files = []
        args_passed = self.split_args(args)

        for arg in args_passed:
            if os.path.isfile(arg):
                mp3_files.append(arg)
                continue
            song_from_library = self.music_library.get_song(arg)
            if song_from_library:
                mp3_files.append(song_from_library)
                continue
            songs = self.music_library.get_playlist_songs(arg)
            if songs:
                mp3_files = mp3_files + songs
                continue
            print("Invalid argument ", arg, ". Couldn't find either a playlist with that name, \
                    or a song in the music library, or in the specified path")

        for mp3_file in mp3_files:
            self.music_player.queue_song(mp3_file)
            self.song_names.append(os.path.basename(mp3_file))

    def do_play(self, args):
        """Start Playing Music.\
        Enter a music file name or a playlist name with this command"""
        self.add_to_queue(args)
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
        self.add_to_queue(args)

    def do_next(self, args):
        """Play next song in queue, skip current one"""
        self.music_player.next_song()

    def do_prev(self, args):
        """Play previous song in queue, skip current one"""
        self.music_player.prev_song()

    def do_list(self, args):
        """List songs in current queue. Use argument 'next' to list all upcoming songs, \
                and 'previous' to list songs which have already played. \nDefault is next."""
        if args == "":
            args = "next"
        if args not in ['next', 'previous']:
            print("Invalid argument passed. Please use 'next' to list all upcoming songs and previous to list songs which have already played")
            return
        songs_list = self.music_player.get_list(args)
        if songs_list is None:
            print("No songs in queue")
            return
        for index, song in enumerate(songs_list):
            print(song)

    def complete_list(self, text, line, start_index, end_index):
        commands = ["next", "previous"]
        if text:
            return [command for command in commands
                    if command.startswith(text)]
        else:
            return commands

    def do_delete_queue(self, args):
        """Delete current queue, so you can create a new one"""
        self.music_player.restart_player()

    def do_shuffle(self, args):
        """Shuffle all songs in the current queue"""
        self.music_player.shuffle()

    def do_repeat(self, args):
        """Enable/Disable repeat for current queue of songs. Use '1' to enable, and '0' to disable"""
        if args not in ["0", "1"]:
            print(
                "Invalid argument. Please enter 1 to enable repeat, or 0 to disable repeat")
        self.music_player.set_repeat(args)
