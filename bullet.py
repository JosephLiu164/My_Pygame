import pygame


# ====================Difine the ordinary bullet====================
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/bullet1.png")
        self.image1 = pygame.image.load("image/bullet1-1.png")
        self.image2 = pygame.image.load("image/bullet1-2.png")
        self.image3 = pygame.image.load("image/bullet1-3.png")
        self.rect = self.image.get_rect()
        self.speed = 12
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < 0:
            self.active = False
        else:
            self.rect.top -= self.speed

    def shoot(self,position):
        self.rect.left, self.rect.top = position
        self.active = True


