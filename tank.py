# juego inspirado en el minijeugo de los tanques de wii play, fantástico juego
import sys
 
import pygame
from pygame.locals import *
from utils import *
from map import Map
from explosion import ShootAnimation
from shoot import Missile, collision_type,collisions
from math import *
from footprints import FootPrint

# FIXME
'''
utilizar keydown para los disparos
misiles colisiones con las paredes
el tanque no tiene volumen cuando sube o baja
en wii play el tanque tiene sombra
'''

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1200, 620
screen = pygame.display.set_mode((width, height))


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

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, mapa) -> None:
        super().__init__()
        self.mapa = mapa
        self.base_imgs = load_folder_images('tank/base')
        self.image = self.base_imgs[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.turret = pygame.sprite.GroupSingle(Turret((self.rect.center)))
        self.direction = vec(0,0)
        self.speed = 3
        self.angle = 0
        self.hit_rect = pygame.rect.Rect(0,0,self.image.get_width(),self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)
        self.shoot = False
        self.facing = 'right'
        self.angle_inc = 3
        self.footprints = pygame.sprite.Group()
        self.diagonal_angles = (45,135,225,315)
        self.diagonal_dir = vec(1,0).normalize()
        self.pos = vec(self.rect.center)
        self.moving = False
        self.turret_pos = vec(0,0)
        self.turret_angle = 0
        self.time_elapsed = 0
        self.shoot_duration = 130
        self.missiles = pygame.sprite.Group()
        self.shoot_animations = pygame.sprite.Group()
        self.footprints_time = 0

    def rotate(self):
        self.image = self.base_imgs[round(self.angle)%180]

    def wd(self):
        self.direction = vec(self.speed,-self.speed)
        if self.angle != 225:
            if 0 <= self.angle <= 90: # 1º cuadrante
                if self.angle-45 > 0:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,45)
                else:
                    self.angle += self.angle_inc
                    self.angle = min(self.angle,45)

                if vec(1,0).angle_to(self.diagonal_dir) != 45:
                    self.diagonal_dir = vec(1,0).normalize().rotate(45)
            elif 270 <= self.angle <= 360:
                if self.angle >= 360:
                    self.angle = 0
                if 315 <= self.angle <= 360:
                    self.angle += self.angle_inc
                else:
                    self.angle -= 1
                    self.angle = max(self.angle,0)
            elif 180 <= self.angle <= 270:
                if 180 <= self.angle <= 225:
                    self.angle += self.angle_inc
                    self.angle = min(self.angle,225)
                else:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,225)
                if self.diagonal_dir.angle_to(vec(-1,0)) != 225:
                    self.diagonal_dir = vec(-1,0).normalize().rotate(225)
            elif 90 <= self.angle <= 180:
                if self.angle-135 > 0:
                    self.angle += self.angle_inc
                    self.angle = min(self.angle,225)
                else:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,45)
        self.diagonal = True

    def wa(self):
        # aw
        self.direction = vec(-self.speed,-self.speed)
        if self.angle != 315:
            if 90 <= self.angle <= 180:
                if self.angle-135 < 0:
                    self.angle += self.angle_inc
                    self.angle = min(self.angle,135)
                else:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,135)

                if self.diagonal_dir.angle_to(vec(-1,0) ) != self.diagonal_angles[1]:
                    self.diagonal_dir = vec(-1,0).normalize().rotate(-self.diagonal_angles[1])
            elif 270 <= self.angle <= 360:
                if self.angle-315 > 0:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,315)
                else:
                    self.angle += self.angle_inc
                    self.angle = min(self.angle,315)
                if vec(1,0).angle_to(self.diagonal_dir) != 315:
                    self.diagonal_dir = vec(1,0).normalize().rotate(-315)
                
            elif 180 <= self.angle <= 270:
                if self.angle-225 > 0:
                    self.angle += self.angle_inc
                else:
                    self.angle -= self.angle_inc
            elif 0 <= self.angle <= 90:
                if self.angle-45 > 0:
                    self.angle += self.angle_inc
                else:
                    self.angle -= self.angle_inc
                    if self.angle <= 0:
                        self.angle = 360
        self.diagonal = True

    def sa(self):
        print("s a")
        self.direction = vec(-self.speed,self.speed)
        if self.angle != 45:
            if 180 <= self.angle <= 270:
                if self.angle-225 < 0:
                    self.angle += self.angle_inc
                    self.angle = min(self.angle,225)
                else:
                    self.angle -=self.angle_inc
                    self.angle = max(self.angle,225)   
                if self.diagonal_dir.angle_to(vec(-1,0)) != self.diagonal_angles[2]:
                    self.diagonal_dir = vec(-1,0).normalize().rotate(self.diagonal_angles[2])
            elif 0 <= self.angle <= 90:    
                # if not self.angle:
                #     self.angle = 360
                if self.angle-45 > 0:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,45)
                else:
                    self.angle += self.angle_inc          
                    self.angle = min(self.angle,45)
                #print(self.diagonal_dir.angle_to(vec(-1,0)))
                if self.diagonal_dir.angle_to(vec(-1,0)) != 45:
                    self.diagonal_dir = vec(1,0).normalize().rotate(45)
            elif 270 <= self.angle <= 360:
                if self.angle-315 > 0:
                    self.angle += self.angle_inc
                else:
                    self.angle -= self.angle_inc
                if self.angle >= 360:
                    self.angle = 0
            elif 90 <= self.angle <= 180:
                if self.angle-135 > 0:
                    self.angle += self.angle_inc
                else:
                    self.angle -= self.angle_inc         
        self.diagonal = True

    def sd(self):
        print("d s")
        self.direction = vec(self.speed,self.speed)
        #print(self.angle)
        assert self.angle >= 0
        if self.angle != 135:
            if 0 <= self.angle <= 90:
                if self.angle-45 > 0:
                    self.angle += self.angle_inc
                else:
                    self.angle -= self.angle_inc
                if self.angle <= 0:
                    self.angle = 360
            elif 270 <= self.angle <= 360:
                if self.angle-315 < 0:
                    self.angle += self.angle_inc
                    self.angle = min(self.angle,315)
                else:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,315)
                if vec(1,0).angle_to(self.diagonal_dir) != 315:
                    self.diagonal_dir = vec(1,0).normalize().rotate(-315)
                
            elif 180 <= self.angle <= 270:
                if self.angle-225 > 0:
                    self.angle += self.angle_inc
                else:
                    self.angle -= self.angle_inc
            elif 90 <= self.angle <= 180:
                if self.angle-135 > 0:
                    self.angle -= self.angle_inc
                else:
                    self.angle += self.angle_inc
        self.diagonal = True

    def key_a(self):
        pass
    def key_d(self):
        pass
    def key_w(self):
        pass
    def key_s(self):
        pass

    def get_input(self):
        # TODO: hace falta normalizar el vector?
        keys=pygame.key.get_pressed()
        self.direction = vec(0,0)
        self.diagonal = False
        self.moving = False
        print(self.angle)
        if keys[K_w] and keys[K_d]:
            print("d w")
            self.wd()            
            # print("diagonal",self.angle)
        elif keys[K_w] and keys[K_a]:
            print("w a")
            #print(self.diagonal_dir.angle_to(vec(-1,0) ),  vec(-1,0).angle_to(self.diagonal_dir)) # 225,-225 con vec(1,0) sería angulo 1º cuadrante 45º
            self.wa()

        elif keys[K_s] and keys[K_a]:
            self.sa()
        elif keys[K_d] and keys[K_s]:
            self.sd()            
            #print("diagonal",self.angle)
        else:
            if keys[K_a]:
                print("a")
                if 90 <= self.angle <= 180:
                    self.angle += self.angle_inc
                    self.angle = min(self.angle,180)
                elif 180 <= self.angle <= 270:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,-180)
                elif 270 <= self.angle <= 360:
                    self.angle += self.angle_inc
                    
                    if self.angle >= 360: # FIXME: utilizar modulo y en la resta igual
                        self.angle = 0
                elif 0 <= self.angle <= 90:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,0)
                    #self.angle = max(self.angle,)
                if self.angle == 180 or self.angle == -180:
                    self.facing = 'left'
                self.direction.x = -self.speed
            if keys[K_d]:
                print("d")
                if 270 <= self.angle <= 360:
                    self.angle += self.angle_inc
                    if self.angle >= 360:
                        self.angle = 0
                elif 0 <= self.angle <= 90:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,0)
                elif 90 <= self.angle <= 180:
                    self.angle += self.angle_inc
                    self.angle = min(self.angle,180)
                if 180 <= self.angle <= 270:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,180)
                if not self.angle:
                    self.facing ='right'
                self.direction.x = self.speed
                
            if keys[K_w]:
                print("w")
                # FIXME: y si estoy en up y no completo los 90º ?
                if 0 <= self.angle <= 90:
                    self.angle += self.angle_inc
                    self.angle = min(self.angle,90)
                elif 90 <= self.angle <= 180:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,90)
                elif 270 <= self.angle <= 360:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,270)
                elif 180 <= self.angle <= 270:
                    self.angle += self.angle_inc
                    self.angle = min(self.angle,270)
                if self.angle == 90:
                    self.facing = 'up'
                self.direction.y = -self.speed

            if keys[K_s]: 
                print("s")
                self.direction.y = self.speed
                if 180 <= self.angle <= 270:
                    self.angle += self.angle_inc
                    self.angle = min(self.angle,270)
                elif 270 <= self.angle <= 360:
                    if self.angle <= 0:
                        self.angle = 360
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,270)
                elif 0 <= self.angle <= 90:
                    self.angle += self.angle_inc
                    self.angle = min(self.angle,90)
                elif 90 <= self.angle <= 180:
                    self.angle -= self.angle_inc
                    self.angle = max(self.angle,90)
                if self.angle == 270:
                    self.facing = 'down'
        if keys[K_SPACE] and pygame.time.get_ticks()-self.time_elapsed >= self.shoot_duration: # utilizar KEYDOWN para no disparar varios a la vez
            # angulo que forma
            self.time_elapsed = pygame.time.get_ticks()
            self.shoot_animations.add(ShootAnimation(self.turret_pos))
            self.missiles.add(Missile(self.turret_pos,self.turret_angle))
        #print("angle: ",self.direction.angle_to(vec(1,0)))
        # tienen que ser divisxores de self.angle_inc!
        if self.angle in (90,180,270,0) or self.angle in self.diagonal_angles and self.diagonal:
            offset = 1
            self.moving = True
            #print("yes",self.direction)
            #wprint("muevete")
            if self.diagonal:
                offset = 0.7071
                self.pos.x += self.direction.x*self.diagonal_dir.x
                self.pos.y += self.direction.y*self.diagonal_dir.y
            else:
                self.pos.x += self.direction.x
                self.pos.y += self.direction.y
            self.rect.center = self.pos
        if self.direction != vec(0,0):
            if pygame.time.get_ticks()-self.footprints_time > 50:
                self.footprints_time = pygame.time.get_ticks()
                x0, y0 = -18,8
                rad = radians(self.angle)
                x1 = cos(rad) *x0 + sin(rad) *y0
                y1 = -sin(rad) *x0 + cos(rad) *y0
                pos1 = self.rect.center+vec(x1,y1)

                x0, y0 = -20,-8
                x1 = cos(rad) *x0 + sin(rad) *y0
                y1 = -sin(rad) *x0 + cos(rad) *y0
                pos2 = self.rect.center+vec(x1,y1)

                self.footprints.add(FootPrint(pos1))
                self.footprints.add(FootPrint(pos2))
            #print("moviendo")
            
    def limits(self):
        blocks_hit_list = pygame.sprite.spritecollide(self, self.mapa.top_obstacles, False)
        for obstacle in blocks_hit_list:
            if abs(self.rect.top-obstacle.rect.top) <= 16:
                self.rect.top = obstacle.rect.top+16
                self.pos = vec(self.rect.center)
        blocks_hit_list = pygame.sprite.spritecollide(self, self.mapa.bottom_obstacles, False)
        for obstacle in blocks_hit_list:
            if self.rect.bottom-obstacle.rect.bottom >= 2: 
                self.rect.bottom = obstacle.rect.bottom+2
                self.pos = vec(self.rect.center)
        blocks_hit_list = pygame.sprite.spritecollide(self, self.mapa.left_obstacles, False)
        for obstacle in blocks_hit_list:
            if self.rect.left-obstacle.rect.left < 11: 
                self.rect.left = obstacle.rect.left+11
                self.pos = vec(self.rect.center)
        blocks_hit_list = pygame.sprite.spritecollide(self, self.mapa.right_obstacles, False)
        for obstacle in blocks_hit_list:
            if abs(self.rect.right-obstacle.rect.right) < 9: 
                self.rect.right = obstacle.rect.right-9
                self.pos = vec(self.rect.center)


    def update(self):
        
        self.get_input()
        self.rotate()
               
        self.turret.update()
        self.footprints.draw(screen)
        self.missiles.update()
        self.limits()
        self.turret.sprite.rect.topleft = self.rect.topleft 
        
        mouse_pos = vec(pygame.mouse.get_pos())
        
        my_pos = vec(self.rect.center)-vec(0,14) # centro ajustado de la torreta, lo que sería el centro de la elipse que describe la rotación de la torreta
        #print(dst_vec.length())
        
        self.turret_angle = vec(my_pos-mouse_pos).angle_to(vec(-1,0))
        
        
        rect = pygame.Rect(0,0,60,45) 
        a, b = (rect.right-rect.left)/2,(rect.bottom-rect.top)/2 # width//2, height//2 del rectangulo que se utiliza para dibujar la elipse
        x = my_pos.x+a*cos(radians(-self.turret_angle))
        y = my_pos.y+b*sin(radians(-self.turret_angle))

        self.turret_pos = vec(x,y)
        self.turret.sprite.angle = self.turret_angle
        
        
        #pygame.draw.ellipse(screen,'red',rect,1)
        #pygame.draw.rect(screen,'red',self.rect,2)
        #pygame.draw.rect(screen,'red',self.turret.sprite.rect,2)
                
class Game:
    def __init__(self):
        self.map = Map()
        self.player = pygame.sprite.GroupSingle(Player((300,400),self.map))
        
    
    def update(self):
        self.player.update()

    def draw(self,surface):
        player = self.player.sprite

        self.map.top_obstacles.draw(screen)
        self.player.draw(surface)
        self.player.sprite.turret.draw(screen)
        player.missiles.draw(screen)
        self.map.left_obstacles.draw(screen)
        self.map.right_obstacles.draw(screen)
        self.map.bottom_obstacles.draw(screen)
        player.shoot_animations.draw(screen)  
        player.shoot_animations.update()  
        #collisions()    


if __name__ == '__main__':
    pygame.init()
    game = Game()
    while True:
        screen.fill('lightblue')
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        game.update()
        game.draw(screen)
        debug(str(pos))
        pygame.display.update()
        fpsClock.tick(fps)