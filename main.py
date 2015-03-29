# Imports
import pygame
from pygame.locals import *
import sys, os, traceback, random

# Options
title = "PyDog"
screenSize = 320, 240
devmode = True
soundlabels = ["ForScience", "GetToTheChopper", "Earthling", "Squirrel", "Disco"]
imagelabels = ["placekitten.jpg"]
animationfolders = ["testanim"]

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
images = [None] * len(imagelabels)
animations = [[0 for x in range(60)] for x in range(len(animationfolders))]

for x in range(0, len(sounds)):
    sounds[x] = pygame.mixer.Sound('sounds/' + soundlabels[x] + ".wav")
for x in range(0, len(images)):
    images[x] = pygame.image.load('images/' + imagelabels[x])
for x in range(0, len(animationfolders)):
    path = "images/" + animationfolders[x]
    num_files = len([f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))])
    for y in range(0, num_files - 1):
        animations[x][y] = pygame.image.load('images/{animfolder}/frame{num}.png'.format(animfolder = animationfolders[x], num = y + 1))

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

    def drawImage(self, image, posx = 0, posy = 0):
        for x in range(0, len(imagelabels)):
            if image == imagelabels[x]:
                surface.blit(images[x], (posx, posy))

    def playSound(self, name):
        if soundchannel.get_busy() == False:
            for x in range(0, len(soundlabels)):
                if name == soundlabels[x]:
                        print("Playing sound " + soundlabels[x] + ".wav")
                        soundchannel.play(sounds[x])
                        self.playingSound = True

    def fpscounter(self):

        self.drawText("FPS: " + str(round(clock.get_fps())), 0, 0)

    class Animation:

        def __init__(self, name):
            for x in range(0, len(animationfolders)):
                if name == animationfolders[x]:
                    self.name = animationfolders[x]
                    self.folderindex = x

            self.animationindex = 0

        def draw(self, posx = 0, posy = 0):
            surface.blit(animations[self.folderindex][self.animationindex], (posx, posy))
            self.animationindex += 1

            if self.animationindex == 3:
                self.animationindex = 0

        def reset(self):
            self.animationindex = 0

engine = Engine()
testanim = engine.Animation("testanim")

class Callbacks:

    def __init__(self):
        print("Loaded Callbacks")

    # Draw Callback
    def draw(self):
        surface.fill((50,0,0))
        engine.drawImage("placekitten.jpg")
        testanim.draw(0, 0)
        engine.fpscounter()

    # Input Callback
    def input(self):

        for event in pygame.event.get():
        
            if event.type == QUIT: return False
            
            elif event.type == KEYDOWN:
                
                if event.key == K_ESCAPE: return False

                if event.key == K_LEFT: engine.playSound("Squirrel")

                if event.key == K_UP: engine.playSound("GetToTheChopper")

                if event.key == K_RIGHT: engine.playSound("Earthling")

                if event.key == K_DOWN: engine.playSound("ForScience")

                if event.key == K_RETURN: engine.playSound("Disco")

                if event.key == K_s: pygame.mixer.stop()

        return True

call = Callbacks()

clock = pygame.time.Clock()

def main():

    while True:

        if not call.input(): break

        clock.tick(30)

        call.draw()

        pygame.display.flip() # Push to Display.

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
