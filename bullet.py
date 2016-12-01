import pygame
from math import *

# ====================Difine all the bullet type====================
class Bullet():

    def move(self):
        if self.rect.top < 0:
            self.active = False
        self.rect.top -= self.speed * cos((self.angle / 180) * pi)
        self.rect.left -= self.speed * cos(((90 - self.angle) / 180) * pi)

    def shoot(self, position, angle = 0):
        self.rect.left, self.rect.top = position
        self.active = True
        self.angle = angle


class Bullet1(pygame.sprite.Sprite, Bullet):
    shooting_interval = 20

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/bullet1.png")
        self.image1 = pygame.image.load("image/bullet1-1.png")
        self.image2 = pygame.image.load("image/bullet1-2.png")
        self.image3 = pygame.image.load("image/bullet1-3.png")
        self.rect = self.image.get_rect()
        self.speed = 15
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)


class Bullet2(pygame.sprite.Sprite, Bullet):
    shooting_interval = 100

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/bullet2.png")
        self.rect = self.image.get_rect()
        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

class Bullet3(pygame.sprite.Sprite, Bullet):
    shooting_interval = 100

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/bullet3.png")
        self.rect = self.image.get_rect()
        self.speed = 3
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)




