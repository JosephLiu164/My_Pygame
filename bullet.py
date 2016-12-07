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
        self.image = pygame.image.load("image/bullet1.png")
        self.image1 = pygame.image.load("image/bullet1-1.png")
        self.image2 = pygame.image.load("image/bullet1-2.png")
        self.image3 = pygame.image.load("image/bullet1-3.png")
        self.rect = self.image.get_rect()
        self.speed = 15
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

# =============enemy bullets==============
class EnemyBullet1(pygame.sprite.Sprite, Bullet):
    shooting_interval = 100

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/bullet2.png")
        self.rect = self.image.get_rect()
        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

# =============enemy bullets================
class EnemyBullet2(pygame.sprite.Sprite, Bullet):
    shooting_interval = 100

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/bullet3.png")
        self.rect = self.image.get_rect()
        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

# =============enemy laser bullets================
class Laser(pygame.sprite.Sprite, Bullet):
    shooting_interval = 1

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/laser.png")
        self.rect = self.image.get_rect()
        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def movesp(self,time):
        
        if (time-70)%800>=90 and (time-70)%800<190:
            self.rect.left -= self.speed
            if self.rect.left < 50:
                self.active = False

        elif (time-70)%800>=490 and (time-70)%800<590:
            self.rect.left += self.speed
            if self.rect.left > 520:
                self.active = False


    

    








