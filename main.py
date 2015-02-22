# Imports
import pygame
from pygame.locals import *
import sys, os, traceback, random

# Options
title = "PyDog"
screenSize = 600, 300
devmode = True

# Code
pygame.display.init()
pygame.font.init()

surface = pygame.display.set_mode(screenSize)

pygame.display.set_caption(title)

font = pygame.font.SysFont('Arial',22)

cache = {}

class Engine:

    def __init__(self):
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

    def fpscounter(self):

        self.drawText("FPS: " + str(round(float(clock.get_fps()) ) ), 0, 0)


class Callbacks:

    def __init__(self):
        print("Loaded Callbacks")

    # Input Callback
    def input(self):
        print("Input")

    # Draw Callback
    def draw(self):
        surface.fill((50,0,0))
        engine.fpscounter()

    def input(self):

        for event in pygame.event.get():
        
            if event.type == QUIT: return False
            
            elif event.type == KEYDOWN:
                
                if event.key == K_ESCAPE: return False

        return True

engine = Engine()
call = Callbacks()

def main():

    global clock
    clock = pygame.time.Clock()

    while True:

        if not call.input(): break

        call.draw()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()