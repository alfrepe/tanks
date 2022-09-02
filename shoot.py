import pygame
import sys
from map import Map
from utils import *
from math import *
from random import *

pygame.init()

SCREEN_WIDHT, SCREEN_HEIGHT = 1200,620
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
clock = pygame.time.Clock()
points = []

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
        self.smoke = pygame.sprite.Group()
        self.time = 0


    def update(self):
        # pos = pygame.mouse.get_pos()
        # self.rect.center = pos

        self.pos.x += self.vel.x * self.dir.x
        self.pos.y += self.vel.y * self.dir.y
        self.rect.center = round(self.pos.x),round(self.pos.y)
        x0, y0 = -12,0
        rad = radians(self.angle)
        x1 = cos(rad) *x0 + sin(rad) *y0
        y1 = -sin(rad) *x0 + cos(rad) *y0
        new_pos = self.rect.center+vec(x1,y1)
        #points.append(new_pos)
        if pygame.time.get_ticks()-self.time >= 60:
            self.time = pygame.time.get_ticks()
            self.smoke.add(Smoke(new_pos,4))
        self.smoke.update()
        self.smoke.draw(screen)

        #pygame.draw.rect(screen,'red',self.rect,2)
    
    def reverse_dir(self, offset_angle=0):
        
        #self.bounces += 1
        self.reversed = True
        self.angle = -self.angle+offset_angle
        self.image = pygame.transform.rotozoom(self.copy_img,self.angle,1)
        self.rect = self.image.get_rect(center=self.pos)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface((40,40)) 
		self.image.fill('red')
		self.rect = self.image.get_rect(center = (300,300))
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		if pygame.mouse.get_pos():
			self.rect.center = pygame.mouse.get_pos()


def collision_type(obstacle, missile):
    if obstacle.side == 'top' and abs(obstacle.rect.top-missile.rect.top) <= 45:
        return 'top'
    elif obstacle.side == 'bottom' and abs(obstacle.rect.bottom-missile.rect.bottom) <= 45:
        return 'bottom'
    elif obstacle.side == 'right' and abs(obstacle.rect.right-missile.rect.right) <= 35:
        return 'right'
    elif obstacle.side == 'left' and abs(obstacle.rect.left-missile.rect.left) <= 35:
        return 'left'
    
def collisions():
    # choco con un
    '''
    NOTE: cuidado con las esquinas, que pueden ser right y top...
    para hacerlo bien, habría que tener en cuenta la esquina del rectángulo, parece que no afecta mucho...
    '''
    for missile in missiles.sprites():
        hit_list = pygame.sprite.spritecollide(missile,mapa.obstacles, False)

        for obstacle in hit_list:
            print(obstacle.side)
            if missile.collision_type:
                if obstacle.side != missile.collision_type and collision_type(obstacle,missile):
                    explosion.add(Explosion(missile.rect.center))
                    missile.kill()
                # si son iguales continua
                continue
            side = collision_type(obstacle,missile)
            if side == 'top':
                missile.reverse_dir()
                missile.dir.y *= -1
                missile.collision_type = obstacle.side                
            elif side == 'bottom':
                missile.dir.y *= -1
                missile.collision_type = obstacle.side
                missile.reverse_dir()
            elif side == 'right':
                missile.dir.x *= -1
                missile.reverse_dir(180)
                missile.collision_type = obstacle.side
            elif side == 'left':
                missile.dir.x *= -1
                missile.collision_type = obstacle.side
                missile.reverse_dir(180)

    # hit_list = pygame.sprite.spritecollide(player.sprite,mapa.obstacles, False)
    # if hit_list:
    #     for obstacle in hit_list:
    #         print(abs(obstacle.rect.bottom-player.sprite.rect.bottom))

class Explosion(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.2
        self.frames = load_folder_images('explosion3/resized')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.animate()

class Smoke(pygame.sprite.Sprite):
    def __init__(self, pos, radius, color=(169,169,169)):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.opacity = 255
        self.color = color
        
        pygame.draw.circle(self.image, self.color, (self.radius,self.radius), self.radius)
    
    def update(self):
        if self.opacity <= 0:
            self.kill()
            return
        self.image.set_alpha(self.opacity)
        self.opacity -= 10

if __name__ == '__main__':
    missiles = pygame.sprite.Group()
    mapa = Map()
    points = []
    player = pygame.sprite.GroupSingle(Player())
    angle = 0
    img = load_image('tank.png')
    explosion = pygame.sprite.Group()
    points = []
    smoke = pygame.sprite.GroupSingle(Smoke((0,0),30))
    while True:
        pos = vec(pygame.mouse.get_pos())
        ini = vec(SCREEN_WIDHT//2,SCREEN_HEIGHT//2+150)
        angle = vec(ini-pos).angle_to(vec(-1,0)) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                missiles.add(Missile(pos,angle))
                pass
                #explosion.add(Explosion(pos))

        screen.fill('lightblue')
        screen.blit(img,(300,400))
        
        missiles.update()
        
        player.update()
        explosion.update()
        collisions()

        mapa.top_obstacles.draw(screen)
        explosion.draw(screen)

        # if missiles.sprites():
        #     pygame.draw.rect(screen,'red',missiles.sprites()[-1].rect,2)
        missiles.draw(screen)
        #player.draw(screen)
        mapa.right_obstacles.draw(screen)
        mapa.left_obstacles.draw(screen)
        mapa.bottom_obstacles.draw(screen)
        # for point in points:
        #     pygame.draw.circle(screen,'red',point,2)
        if smoke.sprite:
            smoke.sprite.rect.center = pos
        smoke.update()
        smoke.draw(screen)
        
        
        
        #print("1 ",angle)

        dir = vec(1,0).rotate(angle)
        #print("2 ",vec(1,0).angle_to(dir))
        pygame.draw.line(screen,'blue',pos,pos+dir*125)
        pygame.draw.line(screen,'red',ini,pos)

        #debug(str(clock.get_fps()))
        pygame.display.update()
        clock.tick(60)
