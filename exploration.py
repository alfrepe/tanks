import sys

import pygame
from pygame.locals import *
from utils import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 1200, 600
screen = pygame.display.set_mode((width, height))

class FootPrint(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((2,3),SRCALPHA)
        pygame.draw.rect(self.image,'lightgrey',(0,0,2,3))
        self.rect = self.image.get_rect(topleft=pos)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.image = load_image('tank.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.angle = 30
        self.speed = 3
        self.velocity = vec(0,0)
        self.copy_img = self.image.copy()
        self.footprints = pygame.sprite.Group()
        self.move_x = 0
        self.dire = vec(1,0).rotate(30)
        self.pos = vec(self.rect.center)
    
    def rotate(self):
        print("uno")
        self.image = pygame.transform.rotozoom(self.copy_img,self.angle,1)
        self.rect = self.image.get_rect(center=self.rect.topleft)
        #self.angle = (self.angle+1)%360

    def update(self):
        keys = pygame.key.get_pressed()
        print(self.angle)
        self.velocity = vec(0,0)
        if keys[pygame.K_d]:
            self.velocity.x += self.speed
        if keys[pygame.K_s]:
            self.velocity.y += self.speed
        if keys[pygame.K_w]:
            self.velocity.y -= self.speed
        if keys[pygame.K_a]:
            self.velocity.x -= self.speed
       
        self.move_x = (self.move_x+self.velocity.x)%9
        if not self.move_x %9:
            if self.velocity.x > 0:
                self.footprints.add(FootPrint(self.rect.topleft))
                self.footprints.add(FootPrint(self.rect.bottomleft))
            elif self.velocity.x <0:
                self.footprints.add(FootPrint(self.rect.topright))
                self.footprints.add(FootPrint(self.rect.bottomright))

        self.pos.x += self.velocity.x*self.dire.x
        self.pos.y += self.velocity.y*self.dire.y
        self.rect.center = self.pos
        self.footprints.draw(screen)
        pygame.draw.rect(screen,'red',self.rect,2)
# Game loop.
player = pygame.sprite.GroupSingle(Player((300,300)))

while True:
    screen.fill('black')
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player.sprite.rotate()
    
    player.update()
    player.draw(screen)
    
    pygame.display.update()
    fpsClock.tick(fps)
