import pygame
from pygame.locals import *
import math
import random
import time
import threading

class Pokebola:
	def __init__(self, position, speed=2):
		self.image = pygame.image.load("resources/images/pokebola.png") 
		self.position = position
		self.speed = speed

class Player:
    def __init__(self, speed=2):
        self.position = [100,100]
        self.image = pygame.image.load("resources/images/player.png")
        self.rect = None
        self.speed = speed
        self.health = Health()

class Health:
    def __init__(self, count=200):
        pass

class Pokemon:
    def __init__(self, position=[200,200], speed=4, health=4):
        self.position = position
        self.speed = speed
        self.health = health
        self.image = pygame.image.load("resources/images/homerchu.png")

class Background:
    def __init__(self):
        pass

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1000, 800
        self.background = Background()
        self.player = Player()
        self.keys = [False, False, False, False] 
        self.enemies = []
        self.pokebolas = []
        self.pokemons = []
        self.gameover = False
        # To control thread call
        self.flag = True
 
    # Inicia a configuração do jogo
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
    # Gerenciador de eventos (como cliques na tela, pressionamento de botões)
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            # Movimento
            if event.key == K_w:
                self.keys[0] = True
            elif event.key == K_a:
                self.keys[1] = True
            elif event.key == K_s:
                self.keys[2] = True
            elif event.key == K_d:
                self.keys[3] = True

            # Throw pokebola
            elif event.key == K_SPACE:
                self.pokebolas.append(Pokebola(list([self.player.position[0]+45, self.player.position[1]+50])))

        if event.type == pygame.KEYUP:
            if event.key == K_w:
                self.keys[0] = False
            elif event.key == K_a:
                self.keys[1] = False
            elif event.key == K_s:
                self.keys[2] = False
            elif event.key == K_d:
                self.keys[3] = False

    def summon_pokemon(self):
        self.flag = False
        self.pokemons.append(Pokemon(list([self.width, random.randint(50, self.height - 200)]), random.randint(6,10)))
        time.sleep(random.randint(1,3))
        self.flag = True

    # Process program logic
    def on_loop(self):
        # Move player
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
            if self.player.position[0] > (self.width - self.player.image.get_width()):
                self.player.position[0] = (self.width - self.player.image.get_width())
            else:
                self.player.position[0] += self.player.speed

        self.player.rect = pygame.Rect(self.player.position[0], self.player.position[1], self.player.image.get_width(), self.player.image.get_height())
        
        # Move pokebola
        for idx,pokebola in enumerate(self.pokebolas):
            if pokebola.position[0] > (self.width + 31):
                self.pokebolas.pop(idx)
            pokebola.position[0] += pokebola.speed 
            pokebola.rect = pygame.Rect(pokebola.position[0], pokebola.position[1], pokebola.image.get_width(), pokebola.image.get_height())
        
        if self.flag:
            t = threading.Thread(target=self.summon_pokemon)
            t.start()

        # TODO: Move enemy
        for idx,pokemon in enumerate(self.pokemons):
            pokemon.position[0] -= pokemon.speed
            pokemon.rect = pygame.Rect(pokemon.image.get_rect())
            pokemon.rect.top = pokemon.position[1]
            pokemon.rect.left = pokemon.position[0]
            # Collision between player and enemy
            if pokemon.rect.colliderect(self.player.rect):
                #self.player.health.count -= 2 
                pass
                            
            elif pokemon.position[0] < (0 - pokemon.rect.width):
                self.pokemons.pop(idx)
                #self.player.health.count -= 25

            # Collision between book and enemy
            else:
                for idx2,pokebola in enumerate(self.pokebolas):
                    if pokemon.rect.colliderect(pokebola.rect):
                        self.pokebolas.pop(idx2)
                        if pokemon.health == 0:
                            self.pokemons.pop(idx)
                            break
                        pokemon.health -= 1

    # Draw screen with changes made
    def on_render(self):
        self._display_surf.fill(0)
        #self._display_surf.blit(self.background.image[0], self.background.position)
        self._display_surf.blit(self.player.image, self.player.position)
        for pokemon in self.pokemons:
            self._display_surf.blit(pokemon.image, pokemon.position) 
        #self._display_surf.blit(self.player.health.image, self.player.health.position)
        #for i in range(self.player.health.count):
            #self._display_surf.blit(self.player.health.fill, (self.player.health.position[0] + 3 + i, self.player.health.position[1] + 3))
        for pokebola  in self.pokebolas:
            self._display_surf.blit(pokebola.image, pokebola.position)

        pygame.display.flip()

    # Finish pygame
    def on_cleanup(self):
        pygame.quit()
 
    # Method that controls game flow
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
