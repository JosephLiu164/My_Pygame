# Import relevant modules
import pygame
import supply
from random import *


# ====================Define the small enemy plane behaviors====================
class SmallEnemy(pygame.sprite.Sprite):  # Inheriting from Sprite class
    small_enemy_energy = 1

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
        self.speed = 4  # Set the speed of enemy plane
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),
                                         randint(-100, 0))
        # Define the initializing position
        # ensuring that the enemy plane won't appear in the very beginning

        self.energy = self.small_enemy_energy
        # To ensure that the enemy plane won't appear from the very beginning
        self.hit = False
        self.active = True  # Set the attribute indicating whether the plane is alive.

    def move(self):  # Define the movement function of the enemy plane
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):  # When the enemy planes move downwards out of the screen
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),
                                         randint(-100, 0))  # The spot where the plane appears
        self.active = True  # Reset the alive status. The same for the rest.
        self.hit = False
        self.energy = SmallEnemy.small_enemy_energy


# ====================Define the mid enemy behaviors====================
class MidEnemy(pygame.sprite.Sprite):
    mid_enemy_energy = 5
    shooting_time_index = 0

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/enemy2.png")  # The plane image
        self.image_hit = pygame.image.load("image/enemy2_hit.png")  # Image when hit
        self.mask = pygame.mask.from_surface(self.image)
        self.destroy_images = []  # Image when destroyed
        self.destroy_images.extend([pygame.image.load("image/enemy2_down1.png"),
                                    pygame.image.load("image/enemy2_down2.png"),
                                    pygame.image.load("image/enemy2_down3.png"),
                                    pygame.image.load("image/enemy2_down4.png")])
        self.rect = self.image.get_rect()  # Get the position
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.speed = 2  # Slower than the small size enemy
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),
                                         randint(-1000, -500))  # The spot where the plane appears
        self.energy = self.mid_enemy_energy
        self.active = True
        self.hit = False

    def move(self):  # Function of movement
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:  # When moving down out of the screen
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),
                                         randint(-1000, -500))  # The spot where the plane appears

        self.active = True
        self.hit = False
        self.energy = MidEnemy.mid_enemy_energy


# ====================Define the big enemy behaviors====================
class BigEnemy(pygame.sprite.Sprite):
    big_enemy_energy = 10
    shooting_time_index = 0

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load("image/enemy3_n1.png"),
                       pygame.image.load("image/enemy3_n2.png")]  # Load the images of the big enemy plane
        self.image_hit = pygame.image.load("image/enemy3_hit.png")  # Load the image when hit
        self.mask = pygame.mask.from_surface(self.images[0])
        self.destroy_images = []  # Load images when destroyed
        self.destroy_images.extend([pygame.image.load("image/enemy3_down1.png"),
                                    pygame.image.load("image/enemy3_down2.png"),
                                    pygame.image.load("image/enemy3_down3.png"),
                                    pygame.image.load("image/enemy3_down4.png"),
                                    pygame.image.load("image/enemy3_down5.png"),
                                    pygame.image.load("image/enemy3_down6.png")])
        self.rect = self.images[0].get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.speed = 2
        self.energy = self.big_enemy_energy
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),
                                         randint(-1500, -1000))  # The spot where the plane appears
        # To ensure that the enemy plane won't appear from the very beginning

        self.active = True
        self.hit = False
        self.supply = self.generate_supply()

    def generate_supply(self):  # Big enemy has several supplies when generated
        random_supply = randint(51, 100)
        if 0 <= random_supply <= 50:
            return None
        elif 51 <= random_supply <= 100:
            return supply.BulletSupply()

    def move(self):
        if self.rect.top < self.bg_height - 60:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):  # When moving down out of the screen
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),
                                         randint(-1500, -1000))  # The spot where the plane appears
        self.active = True
        self.hit = False
        self.energy = BigEnemy.big_enemy_energy
        # self.supply()
