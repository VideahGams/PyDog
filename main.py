# Imports
import pygame
from pygame.locals import *
import sys, os, traceback, random

# Options
title = "PyDog"
screenSize = 480, 360
devmode = True
soundlabels = ["ForScience", "GetToTheChopper", "Earthling", "Squirrel", "Disco"]
imagelabels = ["placekitten.jpg"]
animationfolders = ["testanim", "idle", "kawaii", "choppa", "squirrel"]

animstate = "idle"

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
animations = [[0 for x in range(120)] for x in range(len(animationfolders))]

for x in range(0, len(sounds)):
    sounds[x] = pygame.mixer.Sound('sounds/' + soundlabels[x] + ".wav")
for x in range(0, len(images)):
    images[x] = pygame.image.load('images/' + imagelabels[x])
for x in range(0, len(animationfolders)):
    path = "images/" + animationfolders[x]
    num_files = len([f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))])
    for y in range(0, num_files - 1):
        print("Loaded animation frame for '" + animationfolders[x] + "': " + str((y + 1)))
        framenumlength = len(str(y + 1))
        multiplytimes = 4 - framenumlength
        numofzeros = '0'*multiplytimes
        
        animations[x][y] = pygame.image.load('images/{animfolder}/frame{num}.png'.format(animfolder = animationfolders[x], num = numofzeros + str(y + 1)))

def changeAnim(anim):

    global animstate

    if animstate == "idle":
        idle.reset()
    elif animstate == "kawaii":
        kawaii.reset()
    elif animstate == "choppa":
        choppa.reset()
    elif animstate == "squirrel":
        squirrel.reset()
    
    animstate = anim


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

            global animstate
            
            surface.blit(animations[self.folderindex][self.animationindex], (posx, posy))
            self.animationindex += 1

            path = "images/" + animationfolders[self.folderindex]
            num_files = len([f for f in os.listdir(path)
                        if os.path.isfile(os.path.join(path, f))])

            if self.animationindex == num_files - 1:
                changeAnim("idle")
                self.animationindex = 0

        def reset(self):
            self.animationindex = 0

engine = Engine()

testanim = engine.Animation("testanim")
idle = engine.Animation("idle")
kawaii = engine.Animation("kawaii")
choppa = engine.Animation("choppa")
squirrel = engine.Animation("squirrel")

class Callbacks:

    def __init__(self):
        print("Loaded Callbacks")

    # Draw Callback
    def draw(self):
        surface.fill((50,0,0))
        #engine.drawImage("placekitten.jpg")
        #testanim.draw(0, 0)
        #idle.draw(0, 0)
        #kawaii.draw(0, 0)
        #choppa.draw(0, 0)
        #squirrel.draw(0, 0)

        if animstate == "idle":
            idle.draw(0, 0)
        elif animstate == "kawaii":
            kawaii.draw(0, 0)
        elif animstate == "choppa":
            choppa.draw(0, 0)
        elif animstate == "squirrel":
            squirrel.draw(0, 0)
        
        engine.fpscounter()

    # Input Callback
    def input(self):

        global animstate

        for event in pygame.event.get():
        
            if event.type == QUIT: return False
            
            elif event.type == KEYDOWN:
                
                if event.key == K_ESCAPE: return False

                if event.key == K_LEFT:
                    changeAnim("squirrel")
                    engine.playSound("Squirrel")

                if event.key == K_UP:
                    changeAnim("choppa")
                    engine.playSound("GetToTheChopper")

                if event.key == K_RIGHT:
                    changeAnim("kawaii")
                    engine.playSound("Earthling")

                if event.key == K_DOWN: engine.playSound("ForScience")

                if event.key == K_RETURN: engine.playSound("Disco")

                if event.key == K_s: pygame.mixer.stop()

        return True

call = Callbacks()

clock = pygame.time.Clock()

def main():

    global animstate

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
