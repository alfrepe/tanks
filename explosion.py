
import sys

import pygame
from pygame.locals import *
from utils import *
from random import *



fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

class Particle():
    def __init__(self, pos, vel, radius, color, gravity=None):
        self.pos = vec(pos)
        self.radius = radius
        self.image = pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA)
        #self.image.fill('white')
        self.rect = self.image.get_rect(center=pos)
        self.vel = vec(vel)
        self.opacity = 255
        self.color = (*color,self.opacity)
        self.gravity = gravity
        pygame.draw.circle(self.image, self.color, (self.radius,self.radius), self.radius)

    def render(self):
        
        self.pos += self.vel
        if self.gravity != None:
            self.vel.y += self.gravity
        
        self.rect.center = self.pos
        screen.blit(self.image,self.rect.center)

class Smoke():
    def __init__(self) -> None:
        self.particles = []

    def add_smoke(self, pos):
        #if len(self.particles) < randint(10,15):
        particle = Particle(pos, [uniform(-0.99,0.99), uniform(-0.5,0.5) ], randint(3, 5) ,[169, 169, 169])
        self.particles.append(particle)

    def draw(self):
        for particle in self.particles:
            particle.render()
            particle.opacity -= 10
            particle.image.set_alpha(particle.opacity)
            if particle.opacity <= 0:
                self.particles.remove(particle)

class ShootAnimation(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.image = load_image('ani.png')
        self.rect = self.image.get_rect(center=pos)
        self.copy_img = self.image.copy()
        self.w, self.h = self.image.get_size()
        self.opacity = 255
        self.time = 0
        self.pos = pos
        self.count = 0
        self.smoke = Smoke()
    
    def update(self):
        if 4 <= self.count <= 20:
            self.smoke.add_smoke(self.rect.center)
        self.opacity -= 20
        self.opacity = max(self.opacity,0)
        self.image.set_alpha(self.opacity)
        self.count += 1
        self.smoke.draw() # FIXME dibujarla por encima del tanque, no por detrás


if __name__ == '__main__':
    pygame.init()
    img = load_image('tank.png')
    img = pygame.transform.flip(img,True,False)
    shoot_ani = pygame.sprite.Group()
    cur = load_image('ani.png')
    
    while True:
        screen.fill('lightblue')
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                shoot_ani.add(ShootAnimation((129,295)))
        

        screen.blit(img,(100,240))
        screen.blit(cur,pos)
        shoot_ani.update()
        shoot_ani.draw(screen)
        

        debug(str(pos))
        pygame.display.update()
        fpsClock.tick(fps)
