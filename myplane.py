import pygame


class MyPlane(pygame.sprite.Sprite):
    shooting_time_index = 0

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load("image/hero1.png"),
                       pygame.image.load("image/hero2.png")]# Load 2 plane images
        self.images_hit = [pygame.image.load("image/hero_hit1.png"),
                           pygame.image.load("image/hero_hit2.png")]
        self.mask = pygame.mask.from_surface(self.images[0])  # Get plane image mask to accurately detect collision
        self.destroy_images = []  # 加载飞机损毁图片
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

    # ====================Define the movement in four directions====================
    def move_up(self):  # Function of moving upwards. Other function of movements are similar.
        if self.rect.top > 0:  # If my plane hasn't moved out of the screen
            self.rect.top -= self.speed
        else:  # If it is about to move out of the screen, then adjust the position
            self.rect.top = 0

    def move_down(self):
        if self.rect.bottom < self.bg_height:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.bg_height

    def move_left(self):
        if self.rect.left > 0 - 30:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0 - 30

    def move_right(self):
        if self.rect.right < self.bg_width + 30:
            self.rect.right += self.speed
        else:
            self.rect.right = self.bg_width + 30

    def reset(self):
        self.rect.left, self.rect.top = (self.bg_width - self.rect.width) // 2,\
                                        (self.bg_height - self.rect.height - 30)
        self.active = True
        self.life = 100






