import pygame
from pygame.locals import *
import math
import random
import time
import threading

class Book:
    def __init__(self, position, speed=8):
        self.image = pygame.image.load("resources/images/book.png")
        self.position = position
        self.rect = None
        self.speed = speed

class Player:
    def __init__(self, speed=5):
        self.position = [100,100]
        self.image = pygame.image.load("resources/images/player.png")
        self.rect = None
        self.speed = speed
        self.health = Health()

class Health:
    def __init__(self, count=200):
        self.image = pygame.image.load("resources/images/healthbar.png")
        self.fill = pygame.image.load("resources/images/health.png")
        self.count = count
        self.position = [5,5]

class Troll:
    def __init__(self, position=[200,200], speed=6, health=4):
        self.position = position
        self.image = [pygame.image.load("resources/images/enemy2.png"),pygame.image.load("resources/images/healed.png")]
        self.select = 0
        self.rect = None
        self.speed = speed
        self.health = health

class Background:
    def __init__(self):
        self.image = [pygame.image.load("resources/images/bg.png"), pygame.image.load("resources/images/gameover.png")]
        self.position = [0,0]

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1000, 800
        self.background = Background()
        self.player = Player()
        self.keys = [False, False, False, False] 
        self.enemies = []
        self.books = []
        self.gameover = False
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
        self.enemies.append(Troll(list([self.weight, random.randint(50,self.height - 200)]), random.randint(6,10)))
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
            if self.player.position[0] > (self.weight - self.player.image.get_width()):
                self.player.position[0] = (self.weight - self.player.image.get_width())
            else:
                self.player.position[0] += self.player.speed

        self.player.rect = pygame.Rect(self.player.position[0], self.player.position[1], self.player.image.get_width(), self.player.image.get_height())
        
        # Move book
        for idx,book in enumerate(self.books):
            if book.position[0] > (self.weight + 31):
                self.books.pop(idx)
            book.position[0] += book.speed 
            book.rect = pygame.Rect(book.position[0], book.position[1], book.image.get_width(), book.image.get_height())
        
        if self.flag:
            t = threading.Thread(target=self.summon_enemy)
            t.start()

        # Move enemy
        for idx,enemy in enumerate(self.enemies):
            enemy.position[0] -= enemy.speed
            enemy.rect = pygame.Rect(enemy.image[enemy.select].get_rect())
            enemy.rect.top = enemy.position[1]
            enemy.rect.left = enemy.position[0]
            # Collision between player and enemy
            if enemy.select == 0 and enemy.rect.colliderect(self.player.rect):
                self.player.health.count -= 2 
            
            elif enemy.select == 0 and enemy.position[0] < (0 - enemy.rect.width):
                self.enemies.pop(idx)
                self.player.health.count -= 25

            # Collision between book and enemy
            else:
                for idx2,book in enumerate(self.books):
                    if enemy.rect.colliderect(book.rect):
                        self.books.pop(idx2)
                        if enemy.health == 0:
                            #self.enemies.pop(idx)
                            enemy.select = 1
                            enemy.speed = 15
                            break
                        enemy.health -= 1 
            if self.player.health.count <= 0:
                self.gameover = True;

    # Draw screen with changes made
    def on_render(self):
        self._display_surf.fill(0)
        if not self.gameover:
            self._display_surf.blit(self.background.image[0], self.background.position)
            self._display_surf.blit(self.player.image, self.player.position)
            self._display_surf.blit(self.player.health.image, self.player.health.position)
            for i in range(self.player.health.count):
                self._display_surf.blit(self.player.health.fill, (self.player.health.position[0] + 3 + i, self.player.health.position[1] + 3))
            for enemy in self.enemies:
                self._display_surf.blit(enemy.image[enemy.select], enemy.position)
            for book in self.books:
                self._display_surf.blit(book.image, book.position)
        else:
            self._display_surf.blit(self.background.image[1], self.background.position)

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
