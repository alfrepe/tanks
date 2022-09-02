import pygame
import sys
from map import Map
from utils import *
from random import *
from math import *

pygame.init()

SCREEN_WIDHT, SCREEN_HEIGHT = 1200,620
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Missile(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = load_image('shell_rect_resized.png')
        
        self.copy_img = self.image.copy()
        self.image = pygame.transform.rotozoom(self.copy_img,angle,1)
        self.rect = self.image.get_rect(center=pos)
        self.pos = vec(pos)
        
        self.angle = angle
        self.vel = vec(3,3)
        self.dir = vec(1,0).rotate(-self.angle)
        self.reversed = False
        self.bounces = 0        
        self.collision_type = None


    def update(self):

        self.pos.x += self.vel.x * self.dir.x
        self.pos.y += self.vel.y * self.dir.y
        self.rect.center = round(self.pos.x),round(self.pos.y)
        pass
    
    def reverse_dir(self, offset_angle=0):
        
        #self.bounces += 1
        self.reversed = True
        self.angle = -self.angle+offset_angle
        self.image = pygame.transform.rotozoom(self.copy_img,self.angle,1)
        self.rect = self.image.get_rect(center=self.pos)

class Turret(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.imgs = load_folder_images('tank/turret')
        self.image = self.imgs[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.angle = 0
        self.pos = pos
        
    def update(self):
        #print(self.angle)
        self.image = self.imgs[round(self.angle)%360]

class Tank(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.base_imgs = load_folder_images('tank/base')
        self.image = self.base_imgs[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.turret = pygame.sprite.GroupSingle(Turret((self.rect.center)))
        self.turret_angle = 0

    def update(self):
        mouse_pos = vec(pygame.mouse.get_pos())
        my_pos = vec(self.rect.center)-vec(0,14)
        #print(dst_vec.length())
        
        self.turret_angle = vec(my_pos-mouse_pos).angle_to(vec(-1,0))
        self.turret.sprite.angle = self.turret_angle
        self.turret.sprite.rect.center = self.rect.center
        self.turret.update()
        #pygame.draw.rect(screen,'red',self.rect,2)
        
        

if __name__ == '__main__':
    missiles = pygame.sprite.Group()
    mapa = Map()
    positions = []
    tank = pygame.sprite.GroupSingle(Tank((400,400)))
    rect = pygame.Rect(*tank.sprite.rect.center,60,45)

    while True:
        pos = vec(pygame.mouse.get_pos())
        ini = vec(SCREEN_WIDHT//2,SCREEN_HEIGHT//2+150)
        #angle = vec(ini-pos).angle_to(vec(-1,0)) 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            tank.sprite.turret.sprite.angle += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pass
                    # tank.sprite.turret.sprite.angle += 1
                    
                if event.key == pygame.K_d:
                    pass
                    #tank.sprite.turret.sprite.angle += 1
                    # missile = missiles.sprites()[-1]
                    # missile.dir.y *= -1
                    # missile.reverse_dir()
            if event.type == pygame.MOUSEBUTTONDOWN:
                positions.append(pos)
                pass
                #explosion.add(Explosion(pos))
        
        screen.fill('lightblue')
        missiles.update()
        missiles.draw(screen)

        # if missiles.sprites():
        #     x0, y0 = -12,0
        #     missile = missiles.sprites()[-1]
        #     rad = radians(missile.angle)
        #     x1 = cos(rad) *x0 + sin(rad) *y0
        #     y1 = -sin(rad) *x0 + cos(rad) *y0
        #     new_pos = missile.rect.center+vec(x1,y1)
            # positions.append(new_pos)
        
        # x0, y0 = 25,8
        # rad = radians(tank.sprite.turret_angle)
        # x1 = cos(rad) *x0 + sin(rad) *y0
        # y1 = -sin(rad) *x0 + cos(rad) *y0
        # new_pos = tank.sprite.rect.center-vec(0,14)+vec(x1,y1)
        
        #print(positions)
        #pygame.draw.circle(screen,'green',new_pos,2)
        '''
        x: 60, y:45
        '''
        tank.update()
        tank.draw(screen)
        tank.sprite.turret.draw(screen)
        rect.center = tank.sprite.rect.center-vec(0,14) # 450,436
        points = []

        angle = tank.sprite.turret_angle
        a, b = (rect.right-rect.left)/2,(rect.bottom-rect.top)/2
        print(a,b)
        # equations parametric of the ellipse
        x = rect.centerx+a*cos(radians(-angle))
        y = rect.centery+b*sin(radians(-angle))
        print(x,y)
        pygame.draw.circle(screen,'black',(x,y),2)
        #pygame.draw.ellipse(screen,'red',rect,1)

        
        pygame.draw.line(screen,'green',rect.center,(x,y))
        # for posi in positions:
        #     pygame.draw.circle(screen,'red',posi,2)

        
        #dir = vec(1,0).rotate(angle)
        #print("2 ",vec(1,0).angle_to(dir))
        # pygame.draw.line(screen,'blue',pos,pos+dir*125)
        # pygame.draw.line(screen,'red',ini,pos)

        debug(str(pos))
        pygame.display.update()
        clock.tick(60)
