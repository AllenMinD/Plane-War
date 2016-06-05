#coding=utf-8
import pygame

class Bullet1(pygame.sprite.Sprite):
    def __init__(self, position):   #position为飞机头正中间的位置
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Images/shoot/bullet1.png")
        self.rect = self.image.get_rect() #获取子弹位置
        self.rect.left, self.rect.top = position #确定子弹位置
        self.speed = 12
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True

class Bullet2(pygame.sprite.Sprite):
    def __init__(self, position):   #position为子弹的位置
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Images/shoot/bullet2.png")
        self.rect = self.image.get_rect() #获取子弹位置
        self.rect.left, self.rect.top = position #确定子弹位置
        self.speed = 12
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True

