import pygame
from random import *


# ====================Define the bullet upgrading supply====================
class BulletSupply(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/ufo1.png")
        self.rect = self.image.get_rect()
        self.speed = 5
        self.show = False
        self.mask = pygame.mask.from_surface(self.image)

    def drop(self, position):
        self.rect.left, self.rect.top = position
        self.show = True

    def move(self, bg_size):
        if self.rect.top < bg_size[1]:
            self.rect.top += self.speed
        else:
            self.show = False


# ====================定义超级炸弹补给包====================
class BombSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/ufo2.png")
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100
        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100


