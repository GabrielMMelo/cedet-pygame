import pygame
from pygame.locals import *

class Player:
	def __init__(self, speed=5):
		self.position = [100,100]
		self.image = pygame.image.load("resources/images/player.png")
		self.speed = speed

class App:
	def __init__(self):
		self._running = True
		self._display_surf = None
		self.size = self.weight, self.height = 1000, 800
		self.player = Player()
		self.keys = [False, False, False, False]
	
	def on_init(self):
		pygame.init()
		self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
		self._running = True

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == K_w:
				self.keys[0] = True
			elif event.key == K_a:
				self.keys[1] = True
			elif event.key == K_s:
				self.keys[2] = True
			elif event.key == K_d:
				self.keys[3] = True

		elif event.type == pygame.KEYUP:
			if event.key == K_w:
				self.keys[0] = False
			elif event.key == K_a:
				self.keys[1] = False
			elif event.key == K_s:
				self.keys[2] = False
			elif event.key == K_d:
				self.keys[3] = False

	def on_loop(self):
		if self.keys[0]:
			if self.player.position[1] < 0:
				self.player.position[1] = 0
			else:
				self.player.position[1] -= self.player.speed
		elif self.keys[2]:
			if self.player.position[1] > (self.height - self.player.image.get_height()):
				self.player.position[1] = (self.height - self.player.image.get_height())
			else:
				self.player.position[1] += self.player.speed
		if self.keys[1]:
			if self.player.position[0] < 0:
				self.player.position[0] = 0
			else:
				self.player.position[0] -= self.player.speed
		elif self.keys[3]:
			if self.player.position[0] > (self.weight - self.player.image.get_width()):
				self.player.position[0] = (self.weight - self.player.image.get_width())
			else:
				self.player.position[0] += self.player.speed


	def on_render(self):
		self._display_surf.fill(0)
		self._display_surf.blit(self.player.image, self.player.position)
		pygame.display.flip()

	def on_cleanup(self):
		pygame.quit()

	def on_execute(self):
		if self.on_init() == False:
			self._running = False

		while(self._running):
			for event in pygame.event.get():
				self.on_event(event)
			self.on_loop()
			self.on_render()
		self.on_cleanup()

if __name__ == "__main__":
	theApp = App()
	theApp.on_execute()
