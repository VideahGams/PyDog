# Imports
import pygame
from pygame.locals import *
import sys, os, traceback, random, time
import cwiid

# Options

title = u"PyDog"
screenSize = 656, 416
devmode = True
soundlabels = [u"ForScience", u"GetToTheChopper", u"Earthling", u"Squirrel", u"Disco"]
imagelabels = [u"placekitten.jpg"]
animationfolders = [u"idle", u"kawaii", u"choppa", u"squirrel", u"science"]

animstate = u"idle"

# Setup Display

pygame.mixer.init()
pygame.display.init()
pygame.font.init()

surface = pygame.display.set_mode(screenSize)

pygame.display.set_caption(title)

font = pygame.font.SysFont(u'Arial',22)

cache = {}

soundchannel = pygame.mixer.Channel(1)

sounds = [None] * len(soundlabels)
images = [None] * len(imagelabels)
animations = [[0 for x in xrange(120)] for x in xrange(len(animationfolders))]

# Remote Connection Screen

syncSuccess = False
syncscreen = pygame.image.load(u'images/syncscreen.png')

def trySync():

	surface.blit(syncscreen, (0, 0))
	pygame.display.flip()
	time.sleep(3)
	remote = cwiid.Wiimote()
	syncSuccess = True

try:
	trySync()
except RuntimeError:
	print u"Can't find wiimote, trying again..."
	trySync()

if syncSuccess == True:

	for x in xrange(0, len(sounds)):
		sounds[x] = pygame.mixer.Sound(u'sounds/' + soundlabels[x] + u".wav")
	for x in xrange(0, len(images)):
		images[x] = pygame.image.load(u'images/' + imagelabels[x])
	for x in xrange(0, len(animationfolders)):
		path = u"images/" + animationfolders[x]
		num_files = len([f for f in os.listdir(path)
					if os.path.isfile(os.path.join(path, f))])
		for y in xrange(0, num_files - 1):
			print u"Loaded animation frame for '" + animationfolders[x] + u"': " + unicode((y + 1))
			framenumlength = len(unicode(y + 1))
			multiplytimes = 4 - framenumlength
			numofzeros = u'0'*multiplytimes
			
			animations[x][y] = pygame.image.load(u'images/{animfolder}/frame{num}.png'.format(animfolder = animationfolders[x], num = numofzeros + unicode(y + 1)))
			animations[x][y] = animations[x][y].convert_alpha()

	def changeAnim(anim):

		global animstate

		if animstate == u"idle":
			idle.reset()
		elif animstate == u"kawaii":
			kawaii.reset()
		elif animstate == u"choppa":
			choppa.reset()
		elif animstate == u"squirrel":
			squirrel.reset()
		elif animstate == u"science":
			science.reset()
		
		animstate = anim


	class Engine(object):

		def __init__(self):
			self.playingSound = False
			print u"Loaded Engine Functions"

		def getCache(self, msg, aa): #Font cache. Work in Progress.
		
			if not msg in cache:
				
			  cache[msg] = font.render(msg, aa , (255,255,255))

			  if devmode is True:
				  print u"Added string " + msg + u" to the cache."
			  
			return cache[msg]

		def drawText(self, string, posx, posy, aa = None):

			if aa is None:
				aa = False

			msg = string

			textobj = self.getCache(msg, aa)
			
			surface.blit(textobj, (posx,posy))

		def drawImage(self, image, posx = 0, posy = 0):
			for x in xrange(0, len(imagelabels)):
				if image == imagelabels[x]:
					surface.blit(images[x], (posx, posy))

		def playSound(self, name):
			if soundchannel.get_busy() == False:
				for x in xrange(0, len(soundlabels)):
					if name == soundlabels[x]:
							print u"Playing sound " + soundlabels[x] + u".wav"
							soundchannel.play(sounds[x])
							self.playingSound = True

		def fpscounter(self):

			self.drawText(u"FPS: " + unicode(round(clock.get_fps())), 0, 0)

		class Animation(object):

			def __init__(self, name):
				for x in xrange(0, len(animationfolders)):
					if name == animationfolders[x]:
						self.name = animationfolders[x]
						self.folderindex = x

				self.animationindex = 0

			def draw(self, posx = 0, posy = 0):

				global animstate
				
				surface.blit(animations[self.folderindex][self.animationindex], (posx, posy))
				self.animationindex += 1

				path = u"images/" + animationfolders[self.folderindex]
				num_files = len([f for f in os.listdir(path)
							if os.path.isfile(os.path.join(path, f))])

				if self.animationindex == num_files - 1:
					changeAnim(u"idle")
					self.animationindex = 0

			def reset(self):
				self.animationindex = 0

	engine = Engine()

	#testanim = engine.Animation("testanim")
	idle = engine.Animation(u"idle")
	kawaii = engine.Animation(u"kawaii")
	choppa = engine.Animation(u"choppa")
	squirrel = engine.Animation(u"squirrel")
	science = engine.Animation(u"science")

	class Callbacks(object):

		def __init__(self):
			print u"Loaded Callbacks"

		# Draw Callback
		def draw(self):
			offsetx =  75
			offsety = 0

			surface.fill((50,0,0))
			#engine.drawImage("placekitten.jpg")
			#testanim.draw(0, 0)
			#idle.draw(0, 0)
			#kawaii.draw(0, 0)
			#choppa.draw(0, 0)
			#squirrel.draw(0, 0)

			if animstate == u"idle":
				idle.draw(offsetx,offsety)
			elif animstate == u"kawaii":
				kawaii.draw(offsetx, offsety)
			elif animstate == u"choppa":
				choppa.draw(offsetx, offsety)
			elif animstate == u"squirrel":
				squirrel.draw(offsetx, offsety)
			elif animstate == u"science":
				science.draw(offsetx, offsety)
			
			engine.fpscounter()

		# Input Callback
		def input(self):

			global animstate

			for event in pygame.event.get():
			
				if event.type == QUIT: return False
				
				elif event.type == KEYDOWN:
					
					if event.key == K_ESCAPE: return False

					if event.key == K_LEFT:
						changeAnim(u"squirrel")
						engine.playSound(u"Squirrel")

					if event.key == K_UP:
						changeAnim(u"choppa")
						engine.playSound(u"GetToTheChopper")

					if event.key == K_RIGHT:
						changeAnim(u"kawaii")
						engine.playSound(u"Earthling")

					if event.key == K_DOWN:
						changeAnim(u"science")
						engine.playSound(u"ForScience")

					if event.key == K_RETURN: engine.playSound(u"Disco")

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

	if __name__ == u"__main__":
		try:
			main()
		except:
			traceback.print_exc()
			pygame.quit()
