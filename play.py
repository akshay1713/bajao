import pygame.mixer
from time import sleep
import click, cmd
import threading
import sys


class PlayerInput(threading.Thread):
    
    def __init__(self, status):
        print("passed argument is ", status)
        self.status = status
        super(PlayerInput, self).__init__()

    def get_status(self):
        return self.status

    def run(self):
        while True:
            self.status = input('bajao>')
            if(self.status == 'exit'):
                print("exiting")
                sys.exit()


it = PlayerInput("\n")
it.start()

pygame.mixer.init()
pygame.mixer.music.load(open("Amplifier.mp3","rb"))
pygame.mixer.music.play(-1, 0.0)

while pygame.mixer.music.get_busy():
    if(it.get_status() == 'stop'):
        print("stopping music")
        pygame.mixer.music.stop()
    elif(it.get_status() == 'exit'):
        print("exiting")
        sys.exit()
    sleep(1)



