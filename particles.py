import pygame
from random import *
from utils import *

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1200, 768
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

    def add_smoke_up(self, pos):
        #if len(self.particles) < randint(10,15):
        for _ in range(8):
            particle = Particle(pos, [uniform(-0.2,0.2), uniform(-3,-1) ], randint(3, 5) ,[169, 169, 169])
            self.particles.append(particle)

    def draw(self):
        for particle in self.particles:
            particle.render()
            particle.opacity -= 10
            particle.image.set_alpha(particle.opacity)
            if particle.opacity <= 0:
                self.particles.remove(particle)

if __name__ == '__main__':
    pygame.init()
    smoke = Smoke()
    while True:
        screen.fill('black')
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                smoke.add_smoke_up(pos)
        
        smoke.draw()

        debug(str(fpsClock.get_fps()))
        pygame.display.update()
        fpsClock.tick(fps)