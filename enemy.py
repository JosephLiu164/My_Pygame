# Import relevant modules
import pygame
from random import *


# ====================Define the small enemy plane behaviors====================
class SmallEnemy(pygame.sprite.Sprite):  # Inheriting from Sprite class
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/enemy1.png")  # Load enemy plane image
        self.mask = pygame.mask.from_surface(self.image)
        self.destroy_images = []  # Load damaging images
        self.destroy_images.extend([pygame.image.load("image/enemy1_down1.png"),
                                    pygame.image.load("image/enemy1_down2.png"),
                                    pygame.image.load("image/enemy1_down3.png"),
                                    pygame.image.load("image/enemy1_down4.png")])
        self.rect = self.image.get_rect()  # Get enemy plane position
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]  # Localize the position of bg_size
        self.speed = 2  # Set the speed of enemy plane
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),  # Define the initializing position
                                         randint(-50 * self.speed, 0))
        # To ensure that the enemy plane won't appear from the very beginning

        self.active = True  # Set the attribute indicating whether the plane is alive.

    def move(self):  # Define the movement function of the enemy plane
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):  # When the enemy planes move downwards out of the screen
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),
                                         randint(-50*self.speed, 0)
                                         )
        self.active = True  # Reset the alive status. The same for the rest.


# ====================定义中型敌机及其行为====================
class MidEnemy(pygame.sprite.Sprite):
    energy = 5  # 敌机血量

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/enemy2.png")  # 加载敌方飞机图片
        self.image_hit = pygame.image.load("image/enemy2_hit.png")  # 加载敌方飞机中弹图片
        self.mask = pygame.mask.from_surface(self.image)
        self.destroy_images = []  # 加载飞机损毁图片
        self.destroy_images.extend([pygame.image.load("image/enemy2_down1.png"),
                                    pygame.image.load("image/enemy2_down2.png"),
                                    pygame.image.load("image/enemy2_down3.png"),
                                    pygame.image.load("image/enemy2_down4.png")])
        self.rect = self.image.get_rect()  # 获得敌方飞机的位置
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]  # 本地化背景图片位置
        self.speed = 1  # 设置敌机的速度，应该比小型敌机速度稍慢
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),  # 定义敌机出现的位置
                                         randint(-10 * self.rect.height, -self.rect.height)
                                         )
        self.active = True
        self.energy = MidEnemy.energy
        self.hit = False  # 飞机是否被击中标志位

    def move(self):  # 定义敌机的移动函数
        if self.rect.top < self.bg_height - 60:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):  # 当敌机向下移动出屏幕时
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),  # 定义敌机出现的位置
                                         randint(-10 * self.rect.height, -self.rect.height)  # 保证一开始不会有中型敌机出现
                                         )
        self.active = True
        self.energy = MidEnemy.energy
        self.hit = False


# ====================定义大型敌机及其行为====================
class BigEnemy(pygame.sprite.Sprite):
    energy = 15

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("image/enemy3_n1.png")  # 加载敌方飞机图片，其中大型飞机有帧切换的特效
        self.image2 = pygame.image.load("image/enemy3_n2.png")
        self.image_hit = pygame.image.load("image/enemy3_hit.png")  # 加载敌方飞机中弹图片
        self.mask = pygame.mask.from_surface(self.image1)
        self.destroy_images = []  # 加载飞机损毁图片
        self.destroy_images.extend([pygame.image.load("image/enemy3_down1.png"),
                                    pygame.image.load("image/enemy3_down2.png"),
                                    pygame.image.load("image/enemy3_down3.png"),
                                    pygame.image.load("image/enemy3_down4.png"),
                                    pygame.image.load("image/enemy3_down5.png"),
                                    pygame.image.load("image/enemy3_down6.png")])
        self.rect = self.image1.get_rect()  # 获得敌方飞机的位置
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]  # 本地化背景图片位置
        self.speed = 2  # 设置敌机的速度
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),  # 定义敌机出现的位置
                                         randint(-15 * self.rect.height, -5 * self.rect.height)
                                         )
        self.active = True
        self.energy = BigEnemy.energy
        self.hit = False  # 飞机是否被击中标志位

    def move(self):  # 定义敌机的移动函数
        if self.rect.top < self.bg_height - 60:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):  # 当敌机向下移动出屏幕时
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),  # 定义敌机出现的位置
                                         randint(-15 * self.rect.height, -5 * self.rect.height)
                                         )
        self.active = True
        self.energy = BigEnemy.energy
        self.hit = False
