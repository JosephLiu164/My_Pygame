import pygame
from math import *


class MyPlane(pygame.sprite.Sprite):
    shooting_time_index = 0
    life = 100

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load("image/hero1.png"),
                       pygame.image.load("image/hero2.png")]# Load 2 plane images
        self.images_hit = [pygame.image.load("image/hero_hit1.png"),
                           pygame.image.load("image/hero_hit2.png")]
        self.mask = pygame.mask.from_surface(self.images[0])  # Get plane image mask to accurately detect collision
        self.destroy_images = []  # Load plane destroying image
        self.destroy_images.extend([pygame.image.load("image/hero_blowup_n1.png"),
                                    pygame.image.load("image/hero_blowup_n2.png"),
                                    pygame.image.load("image/hero_blowup_n3.png"),
                                    pygame.image.load("image/hero_blowup_n4.png")])
        self.rect = self.images[0].get_rect()  # Get the position of my plane
        self.rect.left, self.rect.top = (bg_size[0] - self.rect.width) // 2, (bg_size[1] - self.rect.height - 30)  # 定义飞机初始化位置，底部预留60像素
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.speed = 10  # Set moving speed of the plane
        self.active = True  # Whether the plane is alive or destroyed
        self.invincible = False  # The plane is invincible for 3 seconds when initialized
        self.hit = False
        self.bullet_level = 1  #Bullet level of my plane
        self.life = 100

    # ====================Define the movement of my plane====================
    def move(self, angle, moving = True):
        if self.rect.top < 0:# If my plane were to move out of the screen, adjust the position
            self.rect.top = 0
        if self.rect.bottom > self.bg_height:
            self.rect.bottom = self.bg_height
        if self.rect.left < 0 - 30:
            self.rect.left = 0 - 30
        if self.rect.right > self.bg_width + 30:
            self.rect.right = self.bg_width + 30
        if moving:
            self.rect.top -= self.speed * sin(angle)
            self.rect.left += self.speed * cos(angle)
        else:
            return


    def reset(self):
        self.rect.left, self.rect.top = (self.bg_width - self.rect.width) // 2,\
                                        (self.bg_height - self.rect.height - 30)
        self.active = True
        self.life = 100






