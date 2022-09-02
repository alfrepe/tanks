import sys
from turtle import back

import pygame
from pygame.locals import *
from utils import *



fps = 60
fpsClock = pygame.time.Clock()

SCREEN_WIDHT, SCREEN_HEIGHT = 938, 536
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.image = load_image('untitled.png')
        self.rect = self.image.get_rect(topleft=pos)
        #print(self.image.get_size())
    
    def update(self):
        # pygame.draw.rect(screen,'red',self.rect,2)
        pass

class Map:
    def __init__(self):
        self.obstacles = pygame.sprite.Group()
        offset_x, offset_y = 36, 30
        x= 0
        for _ in range(31):
            self.obstacles.add(Obstacle((20+x,20)))
            x += offset_x
        # columna izquierda
        height = self.obstacles.sprites()[0].image.get_height()
        y= 21
        for _ in range(17):
            self.obstacles.add(Obstacle((20,y+20)))
            y += offset_y
        
        # columna derecha
        y= offset_y
        for _ in range(17):
            self.obstacles.add(Obstacle((x+20-offset_x,y+20)))
            y += offset_y

        # # fila abajo
        x= 0
        for _ in range(31):
            self.obstacles.add(Obstacle((20+x,545)))
            x += offset_x

    def draw(self,surface):
        #self.obstacles.update()
        self.obstacles.draw(surface)

background = load_image('2.png')
bg_rect = background.get_rect(topleft=(0,0))

class Tank(pygame.sprite.Sprite):   
    def __init__(self, pos) -> None:
        super().__init__()
        # base_rotations = load_folder_images('base rotations')
        # cannon_rotations = load_folder_images('cannon rotations')
        # self.image = base_rotations[0]
        # self.image.blit(cannon_rotations[0],(0,0))
        self.image = load_image('tank.png')
        self.rect = self.image.get_rect(topleft=pos)

if __name__ == '__main__':
    pygame.init()
    mapa = Map()
    top_obstacles = pygame.sprite.Group()
    tanks = pygame.sprite.Group(Tank((0,0)))
    # Game loop.
    ind  =0
    while True:
        screen.fill('white')
        screen.blit(background,bg_rect)  
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                tanks.add(Tank(pos))
            if event.type == pygame.KEYDOWN:
                pass
                    
            
        if tanks.sprites():
            tanks.sprites()[-1].rect.topleft = pos
        

        #mapa.draw(screen)
        tanks.update()
        tanks.draw(screen)
        debug(str(pygame.mouse.get_pos()))

        pygame.display.update()
        fpsClock.tick(fps)
