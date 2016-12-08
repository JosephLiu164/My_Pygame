import pygame
from math import *

# ====================Difine all the bullet type====================
class Bullet():

    def move(self):
        if self.rect.top < 0:
            self.active = False

        self.rect.top -= self.speed * sin((self.angle*pi)/180)
        self.rect.left += self.speed * cos((self.angle*pi)/180)

    def shoot(self, position, angle = 90):
        self.rect.left, self.rect.top = position
        self.active = True
        self.angle = angle

# ==============Bullet of my plane===============
class MyBullet(pygame.sprite.Sprite, Bullet):
    shooting_interval = 20

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/mybullet1.png")
        self.image1 = pygame.image.load("image/mybullet1-1.png")
        self.image2 = pygame.image.load("image/mybullet1-2.png")
        self.image3 = pygame.image.load("image/mybullet1-3.png")
        self.rect = self.image.get_rect()
        self.speed = 15
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

class EnemyBullet1(pygame.sprite.Sprite, Bullet):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/enemybullet1.png")
        self.rect = self.image.get_rect()
        self.speed = 5
        self.power = 10
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

class EnemyBullet2(pygame.sprite.Sprite, Bullet):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/enemybullet2.png")
        self.rect = self.image.get_rect()
        self.speed = 5
        self.power = 30
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

class EnemyBullet3(pygame.sprite.Sprite, Bullet):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/enemybullet3.png")
        self.rect = self.image.get_rect()
        self.speed = 7
        self.power = 10
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

class EnemyBullet4(pygame.sprite.Sprite, Bullet):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/enemybullet4.png")
        self.rect = self.image.get_rect()
        self.speed = 5
        self.power = 10
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)


# =============enemy laser bullets================
class Laser(pygame.sprite.Sprite, Bullet):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/laser.png")
        self.rect = self.image.get_rect()
        self.speed = 5
        self.power = 1
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, plane):
        self.rect.left = plane.rect.centerx - 20
        self.rect.top = plane.rect.centery


