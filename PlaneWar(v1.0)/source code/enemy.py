#coding=utf-8
import pygame
from pygame.locals import *
from random import *

class SmallEnemy(pygame.sprite.Sprite):

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Images/shoot/enemy1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("Images/shoot/enemy1_down1.png").convert_alpha(),
                                    pygame.image.load("Images/shoot/enemy1_down2.png").convert_alpha(),
                                    pygame.image.load("Images/shoot/enemy1_down3.png").convert_alpha(),
                                    pygame.image.load("Images/shoot/enemy1_down4.png").convert_alpha()
                                    ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.direction = randint(-2, 2) #控制飞机飞行方向
        self.active = True #飞机是否还存在
        self.mask = pygame.mask.from_surface(self.image)#让image1图片中，非透明的部分设置为mask，方便等下的碰撞检测使用
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), \
                                        randint(-5*self.height, 0)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
            self.rect.left += self.direction
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), \
                                        randint(-5*self.height, 0)

class MidEnemy(pygame.sprite.Sprite):

    energy = 8

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Images/shoot/enemy2.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("Images/shoot/enemy2_down1.png").convert_alpha(),
                                    pygame.image.load("Images/shoot/enemy2_down2.png").convert_alpha(),
                                    pygame.image.load("Images/shoot/enemy2_down3.png").convert_alpha(),
                                    pygame.image.load("Images/shoot/enemy2_down4.png").convert_alpha()])
        self.hit_image = pygame.image.load("Images/shoot/enemy2_hit.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.direction = randint(-1, 1) #控制飞机飞行方向
        self.active = True
        self.hit = False #飞机是否被打中
        self.mask = pygame.mask.from_surface(self.image)#让image1图片中，非透明的部分设置为mask，方便等下的碰撞检测使用
        self.energy = MidEnemy.energy
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), \
                                        randint(-10*self.height, -self.height)

    def move(self):
        if self.rect.top < self.height:
           self.rect.top += self.speed
           self.rect.left += self.direction
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), \
                                            randint(-10*self.height, -self.height)


class BigEnemy(pygame.sprite.Sprite):

    energy = 20

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("Images/shoot/enemy3_n1.png").convert_alpha()
        self.image2 = pygame.image.load("Images/shoot/enemy3_n2.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("Images/shoot/enemy3_down1.png").convert_alpha(),
                                    pygame.image.load("Images/shoot/enemy3_down2.png").convert_alpha(),
                                    pygame.image.load("Images/shoot/enemy3_down3.png").convert_alpha(),
                                    pygame.image.load("Images/shoot/enemy3_down4.png").convert_alpha(),
                                    pygame.image.load("Images/shoot/enemy3_down5.png").convert_alpha(),
                                    pygame.image.load("Images/shoot/enemy3_down6.png").convert_alpha()])
        self.hit_image = pygame.image.load("Images/shoot/enemy3_hit.png").convert_alpha()
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.hit = False
        self.mask = pygame.mask.from_surface(self.image1)#让image1图片中，非透明的部分设置为mask，方便等下的碰撞检测使用
        self.energy = BigEnemy.energy
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), \
                                        randint(-15*self.height, -5*self.height)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = BigEnemy.energy
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), \
                                        randint(-15*self.height, -5*self.height)

#特殊横飞的小飞机
class SpecialEnemy(pygame.sprite.Sprite):
    happen = False #判断特殊小飞机是否在触发

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Images/shoot/game_loading1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.append (pygame.image.load("Images/shoot/enemy1_down4.png").convert_alpha())
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1] #背景长宽
        self.rect.left, self.rect.top = randint(-200, 0), randint(0, self.height - self.rect.height - 60)
        self.speed = 2
        self.active = True
        self.death = False #说明小飞机之前是否死过
        self.hit = False #飞机是否被打中
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.left < self.width:
            self.rect.left += self.speed
        else:
            self.reset()

    def reset(self):
        self.death = True #标记这台小飞机已经死过
        self.active = True
        self.rect.left, self.rect.top = randint(-5*self.width, 0), randint(0, self.height - self.rect.height - 60)
