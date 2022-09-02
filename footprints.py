

import sys

import pygame
from pygame.locals import *
from utils import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

class FootPrint(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((5,4))
        self.image.fill('black')
        self.image.set_alpha(15)
        #pygame.draw.rect(self.image,'grey',(0,0,2,3))
        self.rect = self.image.get_rect(topleft=pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.image = load_image('tank.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.angle = 0
        self.time = 0
        self.duration = 100
        self.footprints = pygame.sprite.Group()
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if pygame.time.get_ticks()-self.time >= self.duration:
                self.time = pygame.time.get_ticks()
                self.footprints.add(FootPrint(self.rect.topleft+vec(30,40)))
                self.footprints.add(FootPrint(self.rect.bottomleft-vec(-30,40)))
            self.rect.x += 3
        self.footprints.update()
        self.footprints.draw(screen)
            
if __name__ == '__main__':
    player = pygame.sprite.GroupSingle(Player((300,300)))
    while True:
        screen.fill('white')
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        player.update()
        player.draw(screen)
        pygame.display.update()
        fpsClock.tick(fps)
