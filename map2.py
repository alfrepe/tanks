from ast import Num
import sys
from turtle import back

import pygame
from pygame.locals import *
from utils import *



fps = 60
fpsClock = pygame.time.Clock()

SCREEN_WIDHT, SCREEN_HEIGHT = 1200, 700
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos,side,num=0) -> None:
        super().__init__()

        self.images = load_folder_images('nuevos')
        #assert 0 <= num < len(self.images)
        self.image = self.images[num]
        self.rect = self.image.get_rect(topleft=pos)
        #print(self.image.get_size())
        self.side = side
        self.hit_rect_height = 15
        offset_x = 10
        self.hit_rect_x = self.rect.left+offset_x
        self.hit_rect_y = self.rect.bottom-self.hit_rect_height
        self.hit_rect = pygame.Rect(self.hit_rect_x,self.hit_rect_y,self.image.get_width()-offset_x*2,self.hit_rect_height)
    
    def update(self):
        #pygame.draw.rect(screen,'red',self.rect,1)
        pass

class Map:
    def __init__(self):
        self.obstacles = pygame.sprite.Group()
        self.left_obstacles = pygame.sprite.Group()
        self.bottom_obstacles = pygame.sprite.Group()
        self.right_obstacles = pygame.sprite.Group()
        self.top_obstacles = pygame.sprite.Group()

        obtacles_per_row, obstacles_per_column = 28,19
        x= 0
        # fila arriba
        for _ in range(obtacles_per_row):
            self.top_obstacles.add(Obstacle((20+x,20),'top',randint(0,2)))
            x += self.top_obstacles.sprites()[-1].image.get_width()-62

        # img = self.top_obstacles.sprites()[-1].image
        # width, height = img.get_width(), img.get_height()

        # # columna izquierda
        # offset_y= height-30 # los offsets son inevitables...
        # y = 0
        # for _ in range(obstacles_per_column):
        #     self.left_obstacles.add(Obstacle((20,y+20),'left',0))
        #     y += offset_y
        
        # # # columna derecha
        # y= 0
        # for _ in range(obstacles_per_column):
        #     self.right_obstacles.add(Obstacle((x+20,y+20),'right',0))
        #     y += offset_y

        # #print(y-7)
        # # fila abajo
        # x= 0
        # for _ in range(obtacles_per_row):
        #     self.bottom_obstacles.add(Obstacle((20+x,y-7),'bottom',0))
        #     x += width-2
        
        for x in (self.top_obstacles,self.left_obstacles,self.right_obstacles,self.bottom_obstacles):
            self.obstacles.add(x)
    
    def update(self):
        self.obstacles.update()

    def draw(self,surface):
        
        self.obstacles.draw(surface)
        
        

if __name__ == '__main__':
    pygame.init()
    base_rotations = load_folder_images('tank/base')
    cannon_rotations = load_folder_images('tank/turret')
    cur_ani = base_rotations[0]
    turret = cannon_rotations[0]
    tank_surf = pygame.Surface((cur_ani.get_size()),SRCALPHA)
    tank_surf.blit(cur_ani,(0,0))
    tank_surf.blit(turret,(0,0))
    tank_rect = tank_surf.get_rect(topleft=(200,300))
    mapa = Map()
    top_obstacles = pygame.sprite.Group()
    top_obstacles.add(Obstacle((5,5),'top'))
    # Game loop.
    ind  =0
    while True:
        screen.fill('lightblue')
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                top_obstacles.add(Obstacle(pos,'top'))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pass
                    
        #print("top ",tank_rect.top-mapa.top_obstacles.sprites()[-1].rect.top)
        #print("bottom ",tank_rect.bottom-mapa.bottom_obstacles.sprites()[-1].rect.bottom)
        #print("left ",tank_rect.left-mapa.left_obstacles.sprites()[-1].rect.left)
        #print("right ",tank_rect.right-mapa.right_obstacles.sprites()[-1].rect.right)
        #top_obstacles.sprites()[-1].rect.topleft = pos
        tank_rect.topleft = pos
        mapa.top_obstacles.draw(screen)
        screen.blit(tank_surf,tank_rect)
        mapa.left_obstacles.draw(screen)
        mapa.right_obstacles.draw(screen)
        mapa.bottom_obstacles.draw(screen)
        mapa.update()
        pygame.draw.rect(screen,'red',tank_rect,1)
        #mapa.draw(screen)
        
        # top_obstacles.draw(screen)
        # top_obstacles.update()
        debug(str(pygame.mouse.get_pos()))

        pygame.display.update()
        fpsClock.tick(fps)
