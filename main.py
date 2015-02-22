# Imports
import pygame
from pygame.locals import *
import sys, os, traceback, random

# Options
title = "PyDog"
screenSize = 600, 300
devmode = True
soundlabels = ["test1", "test2", "test3", "test4"]

# Code
pygame.mixer.init()
pygame.display.init()
pygame.font.init()

surface = pygame.display.set_mode(screenSize)

pygame.display.set_caption(title)

font = pygame.font.SysFont('Arial',22)

cache = {}

soundchannel = pygame.mixer.Channel(1)

sounds = [None] * len(soundlabels)

for x in range(0, len(sounds)):
    sounds[x] = pygame.mixer.Sound('sounds/' + soundlabels[x] + ".wav")

class Engine:

    def __init__(self):
        self.playingSound = False
        print("Loaded Engine Functions")

    def getCache(self, msg, aa): #Font cache. Work in Progress.
    
        if not msg in cache:
            
          cache[msg] = font.render(msg, aa , (255,255,255))

          if devmode is True:
              print("Added string " + msg + " to the cache.")
          
        return cache[msg]

    def drawText(self, string, posx, posy, aa = None):

        if aa is None:
            aa = False

        msg = string

        textobj = self.getCache(msg, aa)
        
        surface.blit(textobj, (posx,posy))

    def playSound(self, name):
        if self.playingSound == False:
            for x in range(0, len(soundlabels)):
                if name == soundlabels[x]:
                        print("Playing sound " + soundlabels[x] + ".wav")
                        soundchannel.play(sounds[x])
                        self.playingSound = True
                        while self.playingSound == True:
                            if soundchannel.get_busy() == False:
                                self.playingSound = False
                        break

    def fpscounter(self):

        self.drawText("FPS: " + str(round(float(clock.get_fps()) ) ), 0, 0)


class Callbacks:

    def __init__(self):
        print("Loaded Callbacks")

    # Draw Callback
    def draw(self):
        surface.fill((50,0,0))
        engine.fpscounter()

    # Input Callback
    def input(self):

        for event in pygame.event.get():
        
            if event.type == QUIT: return False
            
            elif event.type == KEYDOWN:
                
                if event.key == K_ESCAPE: return False

                if event.key == K_LEFT: engine.playSound("test1")

                if event.key == K_UP: engine.playSound("test2")

                if event.key == K_RIGHT: engine.playSound("test3")

                if event.key == K_DOWN: engine.playSound("test4")

        return True

engine = Engine()
call = Callbacks()

def main():

    global clock
    clock = pygame.time.Clock()

    while True:

        if not call.input(): break

        call.draw()

        pygame.display.flip() # Push to Display.

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()