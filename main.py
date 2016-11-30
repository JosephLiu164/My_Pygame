import pygame
import pyganim
import myplane
import enemy
import supply
import bullet

from pygame.locals import *
from sys import exit

# =========================Game initialization==========================
pygame.init()
pygame.mixer.init()  # Initialize mixer
bg_size = WIDTH, HEIGHT = 600, 800  # Set background size
screen = pygame.display.set_mode(bg_size)  # Set screen
pygame.display.set_caption("Space Shooter")
background = pygame.image.load("image/background.png")  # Load background image
#background_size = w, h = background.get_size()
#background_rect = background.get_rect()
clock = pygame.time.Clock()  # Set frame rate
frame_rate = 60

x = 0  # Set the initial background position
y = 0
x1 = 0
y1 = -HEIGHT

# ==================Load sound and music================
pygame.mixer.music.load("sound/game_music.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)  # Repeat background music
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/game_over.wav")
me_down_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_double_laser.wav")
get_bullet_sound.set_volume(0.2)

# ===============Colors in common use =================
WHITE = (255, 255, 255)
BLACK = (0,0,0)

# ==============Initializing my plane==============
me = myplane.MyPlane(bg_size)
switch_image = False

# ================Bullet level of my plane=================
bullet_level = 1

# ===============user score=================
score = 0
score_font = pygame.font.SysFont("Chalkboard", 24)

# ============Use frame_num value to achieve some animations==============
frame_num = 0

# =========Generate bullets=========
bullets = []
bullet_index = 0
bullet_num = 200  # Amount of bullet instances
for i in range(bullet_num):
    bullets.append(bullet.Bullet())

# =================A general animation class and function==================
all_animation = {}

class Animation():
    current_frame = 0
    current_image = -1
    is_finished = False

    def __init__(self, name, images, interval=5):
        self.name = name
        self.images = images
        self.interval = interval

# Usage: screen.blit(animation_frame("destroy_me",me.destroy_images,5),me.rect)
def animation_frame(name, images, interval):
    if all_animation.get(name):
        animation = all_animation[name]
    else:
        animation = Animation(name, images, interval)
        all_animation.update({name: animation})
    animation.is_finished = False
    if animation.current_frame % interval == 0:
        animation.current_image = (animation.current_image + 1) % len(images)
    animation.current_frame += 1
    if animation.current_frame >= animation.interval * len(animation.images):
        animation.current_frame = 0
        animation.is_finished = True
    return animation.images[animation.current_image]


def is_finished(name):
    if all_animation.get(name).is_finished:
        return True
    else:
        return False

# ========Function for initializing enemy plane=======
def add_small_enemies(small_enemies, enemies, num):
    for i in range(num):
        e = enemy.SmallEnemy(bg_size)
        small_enemies.add(e)
        enemies.add(e)


def add_mid_enemies(mid_enemies, enemies, num):
    for i in range(num):
        e = enemy.MidEnemy(bg_size)
        mid_enemies.add(e)
        enemies.add(e)


def add_big_enemies(big_enemies, enemies, num):
    for i in range(num):
        e = enemy.BigEnemy(bg_size)
        big_enemies.add(e)
        enemies.add(e)

# ==============Creating enemy plane instances==============
enemies = pygame.sprite.Group()  # Creating all enemy plane groups
small_enemies = pygame.sprite.Group()  # Creating small enemy plane group
add_small_enemies(small_enemies, enemies, 1)
mid_enemies = pygame.sprite.Group()  # Create middle enemy plane group
add_mid_enemies(mid_enemies, enemies, 1)
big_enemies = pygame.sprite.Group()  # Create big enemy plane group
add_big_enemies(big_enemies, enemies, 1)
supplies = pygame.sprite.Group()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    frame_num += 1

    # =================Control the plane=================
    if me.active:
        key_pressed = pygame.key.get_pressed()  # Get user input sequence
        if key_pressed[K_w] or key_pressed[K_UP]:
            me.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.move_right()

    # ============Set the background to scroll (repeatedly blit same two images)========
    screen.blit(background, (x, y))
    screen.blit(background, (x1, y1))
    y1 += 3
    y += 3
    if y > HEIGHT:
        y = -HEIGHT
    if y1 > HEIGHT:
        y1 = -HEIGHT

    # ========Draw the plane and switch between two images to realize the air-jetting effect======
    if me.active:
        screen.blit(animation_frame("me", me.images, 3), me.rect)  # Change the image every 3 frames

    # =========Shooting bullets according to different bullet levels==========
    if bullet_level <= 3:
        if bullet_level == 1:
            shooting_interval = 20
        elif bullet_level == 2:
            shooting_interval = 13
        elif bullet_level == 3:
            shooting_interval = 8
        if frame_num % shooting_interval == 0:  # Shoot a bullet at a certain interval
            bullet_sound.play()
            bullets[bullet_index].shoot(me.rect.midtop)
            bullet_index = (bullet_index + 1) % bullet_num
    elif 4 <= bullet_level <= 6:
        if bullet_level == 4:
            shooting_interval = 11
        if bullet_level == 5:
            shooting_interval = 7
        if bullet_level == 6:
            shooting_interval = 5
        if frame_num % shooting_interval == 0:
            bullet_sound.play()
            bullets[bullet_index].shoot((me.rect.centerx - 35, me.rect.centery))
            bullets[bullet_index + 1].shoot((me.rect.centerx + 30, me.rect.centery))
            bullet_index = (bullet_index + 2) % bullet_num

    # ================The move of the bullets===========-
    for b in bullets:
        if b.active:
            b.move()
            if bullet_level == 1 or bullet_level == 4:
                image = b.image1
            elif bullet_level == 2 or bullet_level == 5:
                image = b.image2
            elif bullet_level == 3 or bullet_level == 6:
                image = b.image3
            screen.blit(image, b.rect)

    # ================Collision between the bullets and enemy planes============
    for b in bullets:
        if b.active:
            enemies_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
            if enemies_hit:
                b.active = False
                for e in enemies_hit:
                    e.energy -= 1
                    e.hit = True  # Plane is hit
                    if e.energy == 0:
                        e.active = False

    # =====Detect whether there is a collision between my plane and enemy planes======
    enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
    if enemies_down:  # If the list of collision detection is not empty, then collision happens.
        for e in enemies_down:
            if e.active:
                me.active = False
                e.active = False  # Enemy plane destroyed

    # =====Detect whether the plane touches the supply======
    supplies_got = pygame.sprite.spritecollide(me, supplies, True, pygame.sprite.collide_mask)
    for s in supplies_got:
        if s.show:
            get_bomb_sound.play()
            if isinstance(s, supply.BulletSupply):
                bullet_level += 1
            s.show = False

    # =========When my plane is destroyed, create the animation===========
    if not me.active:
        screen.blit(animation_frame("me_destroy", me.destroy_images, 5), me.rect)
        if is_finished("me_destroy"):  # When the anmation is over
            me.reset()

    # =========Blit the small enemies and have them move==========
    for each in small_enemies:
        if each.active:
            each.move()
            screen.blit(each.image, each.rect)

    # =========Blit the mid enemies and have them move==========
    for each in mid_enemies:
        if each.active:
            each.move()
            screen.blit(each.image, each.rect)

    # =========Blit the big enemies and have them move==========
    for each in big_enemies:
        if each.active:
            each.move()
            screen.blit(animation_frame("big_enemy_{}".format(id(each)), each.images, 3), each.rect)

    # =========When the middle enemy is hit==============
    for each in mid_enemies:
        if each.active:
            if each.hit:
                screen.blit(each.image_hit, each.rect)
                each.hit = False

    # =========When the big enemy is hit==============
    for each in big_enemies:
        if each.active:
            if each.hit:
                screen.blit(each.image_hit, each.rect)
                each.hit = False

    # =========When small enemy plane is destroyed, create the animation===========
    for each in small_enemies:
        if not each.active:
            enemy1_down_sound.play()
            screen.blit(animation_frame("enemy_destroy_{}".format(id(each)), each.destroy_images, 5), each.rect)
            if all_animation.get("enemy_destroy_{}".format(id(each))).is_finished:
                score += 100  # User score increases
                each.reset()

    # =========When mid enemy plane is destroyed, create the animation===========
    for each in mid_enemies:
        if not each.active:
            enemy2_down_sound.play()
            screen.blit(animation_frame("enemy_{}".format(id(each)), each.destroy_images, 5), each.rect)
            if all_animation.get("enemy_{}".format(id(each))).is_finished:
                score += 700
                each.reset()

    # =========When big enemy plane is destroyed, create the animation===========
    for each in big_enemies:
        if not each.active:
            enemy3_down_sound.play()
            screen.blit(animation_frame("enemy_{}".format(id(each)), each.destroy_images, 5), each.rect)
            if all_animation.get("enemy_{}".format(id(each))).is_finished:
                score += 1500
                if each.supply:
                    each.supply.drop(((each.rect.centerx-each.supply.rect.width/2),
                                      each.rect.centery)) # Dropping supplies when destroyed
                    supplies.add(each.supply)
                each.reset()

    # =============The move of the supplies===============
    for each in supplies:
        if each.show:
            each.move(bg_size)
            screen.blit(each.image, each.rect)

    # =============Display the user score====================
    score_text = score_font.render("Score: {}".format(str(score)), True, BLACK)
    screen.blit(score_text, (10, 5))

    pygame.display.flip()
    clock.tick(frame_rate)  # Set the frame rate to 60
