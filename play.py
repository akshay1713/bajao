import pyglet,sys
from time import sleep
from cmd import Cmd

class MusicPlayer():
    
    def __init__(self, audio_file, action):
        super(MusicPlayer, self).__init__()
        self.audio_file = audio_file
        self.player = pyglet.media.Player()
        self.queue_song(audio_file)

    def play_music(self):
        self.player.play()

    def pause_music(self):
        self.player.pause()

    def delete_player(self):
        self.player.delete()

    def next_song(self):
        self.player.next_source()

    def queue_song(self, audio_file):
        audio_src = pyglet.media.load(audio_file)
        self.player.queue(audio_src)

class PlayerPrompt(Cmd):
    
    def __init__(self, music_player):
        print(music_player)
        super(PlayerPrompt, self).__init__()
        self.music_player = music_player

    def do_play(self, args):
        """Start Playing Music"""
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
        

pm = MusicPlayer("Amplifier.mp3", "play")
while True:
     player_prompt = PlayerPrompt(pm)
     player_prompt.prompt = "bajao>"
     player_prompt.cmdloop("Starting Bajao Music Player")

