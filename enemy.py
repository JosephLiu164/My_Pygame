# Import relevant modules
import pygame
import supply
import bullet
from math import *
from random import *

# =============Define the common behavior of the enemy=============
class Enemy():
    def move(self,angle = -90):
        if self.rect.top < self.bg_height:
            self.rect.top -= self.speed * sin((angle * pi) / 180)
            self.rect.left += self.speed * cos((angle * pi) / 180)
        else:
            self.reset()

# ====================Define the small enemy plane behaviors====================
class SmallEnemy(pygame.sprite.Sprite, Enemy):  # Inheriting from Sprite class
    initial_energy = 1
    upgraded_energy = 1

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
                                         randint(-800, 0))
        # Define the initializing position
        # ensuring that the enemy plane won't appear in the very beginning

        self.energy = SmallEnemy.initial_energy
        self.crashing_power = 30 # The damage cause to my plane when it is hit by my plane directly
        self.destroy_score = 100
        self.hit = False
        self.active = True  # Set the attribute indicating whether the plane is alive.


    def reset(self):  # When the enemy planes move downwards out of the screen
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),
                                         randint(-800, 0))  # The spot where the plane appears
        self.active = True  # Reset the alive status. The same for the rest.
        self.hit = False
        self.energy = SmallEnemy.upgraded_energy


class SmallEnemy2(pygame.sprite.Sprite, Enemy):
    initial_energy = 1
    upgraded_energy = 1

    def position(self):
        horizontal_distance = randint(400, 800)
        vertical_distance = horizontal_distance * tan(pi/3)
        horizontal_position = choice([-horizontal_distance, self.bg_width+horizontal_distance])
        vertical_position = -vertical_distance + randint(-100,300)
        return (horizontal_position, vertical_position)

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/enemy1-2.png")  # Load enemy plane image
        self.mask = pygame.mask.from_surface(self.image)
        self.destroy_images = []  # Load damaging images
        self.destroy_images.extend([pygame.image.load("image/enemy1_down1.png"),
                                    pygame.image.load("image/enemy1_down2.png"),
                                    pygame.image.load("image/enemy1_down3.png"),
                                    pygame.image.load("image/enemy1_down4.png")])
        self.rect = self.image.get_rect()  # Get enemy plane position
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]  # Localize the position of bg_size
        self.speed = 6  # Set the speed of enemy plane
        self.rect.left,self.rect.top = \
            self.init_position_left,self.init_position_top = self.position()
        # Define the initializing position
        # ensuring that the enemy plane won't appear in the very beginning

        self.energy = SmallEnemy2.initial_energy
        self.crashing_power = 45
        self.destroy_score = 200
        self.hit = False
        self.active = True  # Set the attribute indicating whether the plane is alive.


    def reset(self):  # When the enemy planes move downwards out of the screen
        self.rect.left, self.rect.top = \
            self.init_position_left, self.init_position_top = self.position()
        self.active = True  # Reset the alive status. The same for the rest.
        self.hit = False
        self.energy = SmallEnemy.upgraded_energy


# ====================Define the mid enemy behaviors====================
class MidEnemy(pygame.sprite.Sprite, Enemy):
    shooting_time_index = 0
    initial_shooting_interval = 100
    upgraded_shooting_interval = 100
    initial_energy = 5
    upgraded_energy = 5

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
                                         randint(-1400, -600))  # The spot where the plane appears
        self.supply = self.generate_supply()
        self.bullet = bullet.EnemyBullet1
        self.crashing_power = 60
        self.destroy_score = 700
        self.energy = MidEnemy.initial_energy
        self.shooting_interval = MidEnemy.initial_shooting_interval
        self.active = True
        self.hit = False

    def reset(self):
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),
                                         randint(-1400, -600))  # The spot where the plane appears

        self.active = True
        self.hit = False
        self.energy = MidEnemy.upgraded_energy
        self.shooting_interval = MidEnemy.upgraded_shooting_interval

    def generate_supply(self):  # middle enemy has several bullet supplies when generated
        random_supply = randint(0, 100)
        if 0 <= random_supply <= 33:
            return None
        elif 34 <= random_supply <= 56:
            return supply.BulletSupply()
        elif 57<= random_supply<= 79:
            return supply.LifeSupply()
        elif 80 <= random_supply:
            return supply.Shield()



# ====================Define the big enemy behaviors====================
class BigEnemy(pygame.sprite.Sprite, Enemy):
    shooting_time_index = 0
    initial_shooting_interval = 100
    upgraded_shooting_interval = 100
    initial_energy = 10
    upgraded_energy = 10

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
        self.energy = BigEnemy.initial_energy
        self.shooting_interval = BigEnemy.initial_shooting_interval
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),
                                         randint(-1600, -1200))  # The spot where the plane appears
        # To ensure that the enemy plane won't appear from the very beginning

        self.active = True
        self.hit = False
        self.bullet = bullet.EnemyBullet2
        self.supply = self.generate_supply()
        self.crashing_power = 90
        self.destroy_score = 1500


    def generate_supply(self):  # Big enemy has several supplies when generated
        random_supply = randint(0, 100)
        if 0 <= random_supply <= 50:
            return supply.BulletSupply()
        elif 51<= random_supply <= 75:
            return supply.LifeSupply()
        elif 76 <= random_supply:
            return supply.Shield()

    def reset(self):  # When moving down out of the screen
        self.rect.left, self.rect.top = (randint(0, self.bg_width - self.rect.width),
                                         randint(-1600, -1200))  # The spot where the plane appears
        self.active = True
        self.hit = False
        self.energy = BigEnemy.upgraded_energy
        self.shooting_interval = BigEnemy.upgraded_shooting_interval
        self.generate_supply()


class SpEnemy(pygame.sprite.Sprite, Enemy):
    shooting_time_index = 0
    initial_energy = 10
    upgraded_energy = 10
    initial_shooting_interval = 100
    upgraded_shooting_interval = 100

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/sp_enemy.png")  # Load the images of the sp enemy plane
        self.image_hit = pygame.image.load("image/sp_blowup_n2.png")  # Load the image when hit
        self.mask = pygame.mask.from_surface(self.image)
        self.destroy_images = []  # Load images when destroyed
        self.destroy_images.extend([pygame.image.load("image/sp_blowup_n1.png"),
                                    pygame.image.load("image/sp_blowup_n2.png"),
                                    pygame.image.load("image/sp_blowup_n3.png")])
        self.rect = self.image.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.speed = 5
        self.energy = self.initial_energy
        self.shooting_interval = SpEnemy.initial_shooting_interval
        self.rect.left, self.rect.top = ((self.bg_width - self.rect.width) // 2,
                                         -200)  # The spot where the plane appears
        # To ensure that the enemy plane won't appear from the very beginning

        self.active = True
        self.hit = False
        self.supply = self.generate_supply()
        self.crashing_power = 50
        self.destroy_score = 2000

    def sp_move(self, timell):  # special movement
        time = (timell - 70) % 800
        if timell < 70:  # ((self.bg_height//2)//self.speed)
            self.rect.top += self.speed
        elif time >= 40 and time < 90:
            self.rect.left += self.speed
        elif time >= 90 and time < 190:
            self.rect.left -= self.speed
        elif time >= 190 and time < 220:
            self.rect.top -= self.speed
        elif time >= 220 and time < 320:
            self.rect.left += self.speed
        elif time >= 320 and time < 350:
            self.rect.top += self.speed
        elif time >= 350 and time < 400:
            self.rect.left -= self.speed
        elif time >= 440 and time < 490:
            self.rect.left -= self.speed
        elif time >= 490 and time < 590:
            self.rect.left += self.speed
        elif time >= 590 and time < 620:
            self.rect.top -= self.speed
        elif time >= 620 and time < 720:
            self.rect.left -= self.speed
        elif time >= 720 and time < 750:
            self.rect.top += self.speed
        elif time >= 750 and time < 800:
            self.rect.left += self.speed

    def generate_supply(self):  # Special enemy has several supplies when generated
        random_supply = randint(0, 100)
        if 0 <= random_supply <= 50:
            return supply.BulletSupply()
        elif 51 <= random_supply <= 75:
            return supply.LifeSupply()
        elif 76 <= random_supply:
            return supply.Shield()

    def reset(self):  # When moving down out of the screen
        self.rect.left, self.rect.top = ((self.bg_width - self.rect.width) // 2,
                                         -200)  # The spot where the plane appears
        self.active = False
        self.hit = False
        self.energy = SpEnemy.upgraded_energy
        self.shooting_interval = SpEnemy.upgraded_shooting_interval

