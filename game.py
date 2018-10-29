import pygame
from pygame.locals import *
import math
import random
import time
import threading

class Book:
    def __init__(self, position):
        self.image = pygame.image.load("resources/images/book.png")
        self.position = position
        self.rect = None

class Player:
    def __init__(self, speed=5):
        self.position = [100,100]
        self.image = pygame.image.load("resources/images/player2.png")
        self.rect = None
        self.speed = speed

class Enemy:
    def __init__(self, position=[200,200], speed=0.4):
        self.position = position
        self.image = pygame.image.load("resources/images/enemy2.png")
        self.rect = None
        self.speed = speed

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1000, 800
        self.player = Player()
        self.keys = [False, False, False, False] 
        self.enemies = []
        self.enemies.append(Enemy())
        self.books = []
        # To control thread call
        self.flag = True
 
    # Init pygame module
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
    # Event handler
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            # Movement
            if event.key == K_w:
                self.keys[0] = True
            elif event.key == K_a:
                self.keys[1] = True
            elif event.key == K_s:
                self.keys[2] = True
            elif event.key == K_d:
                self.keys[3] = True

            # Throw book
            elif event.key == K_SPACE:
                self.books.append(Book(list([self.player.position[0]+45, self.player.position[1]+50])))

        if event.type == pygame.KEYUP:
            if event.key == K_w:
                self.keys[0] = False
            elif event.key == K_a:
                self.keys[1] = False
            elif event.key == K_s:
                self.keys[2] = False
            elif event.key == K_d:
                self.keys[3] = False

    def summon_enemy(self):
        self.flag = False
        self.enemies.append(Enemy(list([self.weight, random.randint(50,self.height - 100)])))    
        time.sleep(3)
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
            if self.player.position[0] > (self.weight - self.player.image.get_width()):
                self.player.position[0] = (self.weight - self.player.image.get_width())
            else:
                self.player.position[0] += self.player.speed

        self.player.rect = pygame.Rect(self.player.position[0], self.player.position[1], self.player.image.get_width(), self.player.image.get_height())
        
        # Move book
        for idx,book in enumerate(self.books):
            if book.position[0] > (self.weight + 31):
                self.books.pop(idx)
            book.position[0]+=2 
            book.rect = pygame.Rect(book.position[0], book.position[1], book.image.get_width(), book.image.get_height())
        
        if self.flag:
            t = threading.Thread(target=self.summon_enemy)
            t.start()

        # Move enemy
        for idx,enemy in enumerate(self.enemies):
            enemy.position[0] -= enemy.speed
            enemy.rect = pygame.Rect(enemy.image.get_rect())
            enemy.rect.top = enemy.position[1]
            enemy.rect.left = enemy.position[0]
            # Collision between player and enemy
            if enemy.rect.colliderect(self.player.rect):
                self.enemies.pop(idx)
            # Collision between book and enemy
            else:
                for idx2,book in enumerate(self.books):
                    if enemy.rect.colliderect(book.rect):
                        self.enemies.pop(idx)
                        self.books.pop(idx2)

    # Draw screen with changes made
    def on_render(self):
        self._display_surf.fill(0)
        self._display_surf.blit(self.player.image, self.player.position)
        for enemy in self.enemies:
            self._display_surf.blit(enemy.image, enemy.position)
        for book in self.books:
            self._display_surf.blit(book.image, book.position)
        pygame.display.flip()

    # Finish pygame
    def on_cleanup(self):
        pygame.quit()
 
    # Method that controls game flow
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
