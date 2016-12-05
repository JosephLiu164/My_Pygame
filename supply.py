import pygame

# ====================Define the bullet upgrading supply====================

class Supply():
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
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

class BulletSupply(pygame.sprite.Sprite, Supply):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/ufo1.png")
        Supply.__init__(self)




class LifeSupply(pygame.sprite.Sprite, Supply):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/life.png")
        Supply.__init__(self)

# class Invincible(pygame.sprite.Sprite, Supply):




