import pygame
import pyganim
import myplane
import enemy
import supply
import bullet

from pygame.locals import *
from math import *
from sys import exit

# =========================Game initialization==========================
pygame.init()
pygame.mixer.init()  # Initialize mixer
bg_size = WIDTH, HEIGHT = 600, 800  # Set background size
screen = pygame.display.set_mode(bg_size)  # Set screen
pygame.display.set_caption("Space Shooter")
background = pygame.image.load("image/background.png")  # Load background image
gameover_image = pygame.image.load("image/game_over.png")  # game over background image
gameover_rect = gameover_image.get_rect()
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
level_up_sound = pygame.mixer.Sound("sound/achievement.wav")
level_up_sound.set_volume(0.2)

# ===============Colors in common use =================
WHITE = (255, 255, 255)
BLACK = (0,0,0)

# ==============Initializing my plane==============
me = myplane.MyPlane(bg_size)
switch_image = False

# ===============user score=================
score = 80000
score_font = pygame.font.SysFont("Chalkboard", 24)
level = 1 # current game difficulty level

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

def increase_speed(target, value):
    for each in target:
        each.speed += value

# ==============Create enemy plane instances==============
enemies = pygame.sprite.Group()  # Creating all enemy plane groups
small_enemies = pygame.sprite.Group()  # Creating small enemy plane group
add_small_enemies(small_enemies, enemies, 1)
mid_enemies = pygame.sprite.Group()  # Create middle enemy plane group
add_mid_enemies(mid_enemies, enemies, 1)
big_enemies = pygame.sprite.Group()  # Create big enemy plane group
add_big_enemies(big_enemies, enemies, 1)
supplies = pygame.sprite.Group()

# ===============Create all the bullets=================
bullets = [] # Generate my bullets
bullet_index = 0
bullet_num = 300  # Amount of bullet instances
for i in range(bullet_num):
    bullets.append(bullet.Bullet1())

bullets2 = [] # Generate enemy bullets of middle enemy
bullet2_index = 0
bullet2_num = 300
for i in range(bullet2_num):
    bullets2.append(bullet.Bullet2())

bullets3 = [] # Generate enemy bullets of big enemy
bullet3_index = 0
bullet3_num = 300
for i in range(bullet3_num):
    bullets3.append(bullet.Bullet3())


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    me.shooting_time_index += 1 # Shooting time index of my plane increase by 1 in every frame

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

    # ==============Game difficulty level================
        if level == 1 and score > 3000:
            # If reaching level 2, add 3 small enemies, 2 middle enemies and 1 big enemies.
            # Increase the speed of small enemy.
            level = 2
            level_up_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            increase_speed(small_enemies, 1)
        elif level == 2 and score > 12000:  # Reaching level 3
            level = 3
            level_up_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            increase_speed(small_enemies, 1)
            increase_speed(mid_enemies, 1)
        elif level == 3 and score > 60000:  # Reacin level 4
            level = 4
            level_up_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            increase_speed(small_enemies, 1)
            increase_speed(mid_enemies, 1)
            increase_speed(big_enemies, 1)

    # ============Set the background to scroll (repeatedly blit same two images)========
    screen.blit(background, (x, y))
    screen.blit(background, (x1, y1))
    y1 += 3
    y += 3
    if y > HEIGHT:
        y = -HEIGHT
    if y1 > HEIGHT:
        y1 = -HEIGHT

    # =============Detect whether my plane is destroyed==============
    if me.life <= 0:
        me.active = False

    # =========Shooting bullets according to different bullet levels of my plane==========
    if me.bullet_level <= 3:
        if me.bullet_level == 1:
            bullet.Bullet1.shooting_interval = 20
        elif me.bullet_level == 2:
            bullet.Bullet1.shooting_interval = 15
        elif me.bullet_level == 3:
            bullet.Bullet1.shooting_interval = 11
        if me.shooting_time_index % bullet.Bullet1.shooting_interval == 0:  # Shoot a bullet at a certain interval
            bullet_sound.play()
            bullets[bullet_index].shoot(me.rect.midtop)
            bullet_index = (bullet_index + 1) % bullet_num
    elif 4 <= me.bullet_level <= 6:
        if me.bullet_level == 4:
            bullet.Bullet1.shooting_interval = 17
        elif me.bullet_level == 5:
            bullet.Bullet1.shooting_interval = 12
        elif me.bullet_level == 6:
            bullet.Bullet1.shooting_interval = 8
        if me.shooting_time_index % bullet.Bullet1.shooting_interval == 0:
            bullet_sound.play()
            bullets[bullet_index].shoot((me.rect.centerx - 35, me.rect.centery))
            bullets[bullet_index + 1].shoot((me.rect.centerx + 28, me.rect.centery))
            bullet_index = (bullet_index + 2) % bullet_num
            if bullet_index >= bullet_num-1:
                bullet_index = 0

    elif 7<= me.bullet_level <= 9:
        if me.bullet_level == 7:
            bullet.Bullet1.shooting_interval = 9
        elif me.bullet_level == 8:
            bullet.Bullet1.shooting_interval = 7
        elif me.bullet_level == 9:
            bullet.Bullet1.shooting_interval = 4
        if me.shooting_time_index % bullet.Bullet1.shooting_interval == 0:
            bullet_sound.play()
            bullets[bullet_index].shoot((me.rect.centerx - 33, me.rect.centery),105)
            bullets[bullet_index + 1].shoot((me.rect.centerx-6, me.rect.centery),90)
            bullets[bullet_index + 2].shoot((me.rect.centerx + 28, me.rect.centery),75)
            bullet_index = (bullet_index + 3) % bullet_num
            if bullet_index >= bullet_num - 2:
                bullet_index = 0

    elif me.bullet_level == 10:
        bullet.Bullet1.shooting_interval = 4
        if me.shooting_time_index % bullet.Bullet1.shooting_interval == 0:
            bullet_sound.play()
            bullets[bullet_index].shoot((me.rect.centerx - 33, me.rect.centery), 120)
            bullets[bullet_index + 1].shoot((me.rect.centerx - 6, me.rect.centery), 90)
            bullets[bullet_index + 2].shoot((me.rect.centerx + 28, me.rect.centery), 60)
            bullets[bullet_index + 3].shoot((me.rect.centerx + 20, me.rect.centery), 75)
            bullets[bullet_index + 4].shoot((me.rect.centerx - 25, me.rect.centery), 105)
            bullet_index = (bullet_index + 5) % bullet_num
            if bullet_index >= bullet_num - 4:
                bullet_index = 0

    # ================The move of the bullets===========-
    for b in bullets:
        if b.active:
            if me.bullet_level == 1 or me.bullet_level == 4 or me.bullet_level == 7:
                b.move()
                bullet_image = b.image1
            elif me.bullet_level == 2 or me.bullet_level == 5 or me.bullet_level == 8:
                b.move()
                bullet_image = b.image2
            elif me.bullet_level == 3 or me.bullet_level == 6 or me.bullet_level == 9 or me.bullet_level == 10:
                b.move()
                bullet_image = b.image3
            screen.blit(bullet_image, b.rect)

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

    # =========Detect whether my plane touches bullets2===========
    bullets2_hit = pygame.sprite.spritecollide(me, bullets2, False, pygame.sprite.collide_mask)
    for b in bullets2_hit:
        if b.active:
            me.hit = True
            me.life -= 10
            b.active = False

    # =========Detect whether my plane touches bullets3===========
    bullets3_hit = pygame.sprite.spritecollide(me, bullets3, False, pygame.sprite.collide_mask)
    for b in bullets3_hit:
        if b.active:
            me.hit = True
            me.life -= 30
            b.active = False

    # =====Detect whether there is a collision between my plane and enemy planes======
    enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
    if enemies_down:  # If the list of collision detection is not empty, then collision happens.
        for e in enemies_down:
            if e.active:
                if isinstance(e, enemy.SmallEnemy):
                    me.life -= 30
                elif isinstance(e, enemy.MidEnemy):
                    me.life -= 60
                elif isinstance(e, enemy.BigEnemy):
                    me.life -= 90
                e.active = False  # Enemy plane destroyed

    # =====Detect whether the plane touches the supply======
    supplies_got = pygame.sprite.spritecollide(me, supplies, True, pygame.sprite.collide_mask)
    for s in supplies_got:
        if s.show:
            get_bomb_sound.play()
            if isinstance(s, supply.BulletSupply):
                me.bullet_level += 1
                if me.bullet_level >= 10:
                    me.bullet_level = 10
            s.show = False

    # =========When my plane is destroyed, create the animation===========
    if not me.active:
        screen.blit(animation_frame("me_destroy", me.destroy_images, 5), me.rect)
        if is_finished("me_destroy"):  # When the anmation is over
            me.reset()

    # =========Blit the big enemies and have them move==========
    for each in big_enemies:
        if each.active:
            each.move()
            each.shooting_time_index += 1
            screen.blit(animation_frame("big_enemy_{}".format(id(each)), each.images, 3), each.rect)
            if each.shooting_time_index % bullet.Bullet3.shooting_interval == 0:  # Shoot a bullet at a certain interval
                bullet3_angle = (180/pi)*atan2((each.rect.centery - me.rect.centery),
                                         (me.rect.centerx- each.rect.centerx))
                bullets3[bullet3_index].shoot((each.rect.centerx - 10, each.rect.centery), bullet3_angle)  # Big enemy shooting bullets
                bullet3_index = (bullet3_index + 1) % bullet3_num

    # ================The move of the bullets from big enemy===========-
    for b in bullets3:
        if b.active:
            b.move()
            screen.blit(b.image, b.rect)

    # =========Blit the mid enemies and have them move==========
    for each in mid_enemies:
        if each.active:
            each.move()
            each.shooting_time_index += 1
            screen.blit(each.image, each.rect)
            if each.shooting_time_index % bullet.Bullet2.shooting_interval == 0:  # Shoot a bullet at a certain interval
                bullets2[bullet2_index].shoot((each.rect.centerx - 3, each.rect.centery),
                                              -90)  # Shooting bullets by middle enemy
                bullet2_index = (bullet2_index + 1) % bullet2_num

    # ================The move of the bullets from middle enemy===========-
    for b in bullets2:
        if b.active:
            b.move()
            screen.blit(b.image, b.rect)

    # =========Blit the small enemies and have them move==========
    for each in small_enemies:
        if each.active:
            each.move()
            screen.blit(each.image, each.rect)

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
            screen.blit(animation_frame("enemy_destroy_{}".format(id(each)), each.destroy_images, 3), each.rect)
            if all_animation.get("enemy_destroy_{}".format(id(each))).is_finished:
                score += 100  # User score increases
                each.reset()

    # =========When mid enemy plane is destroyed, create the animation===========
    for each in mid_enemies:
        if not each.active:
            enemy2_down_sound.play()
            screen.blit(animation_frame("enemy_{}".format(id(each)), each.destroy_images, 3), each.rect)
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

    # ========Draw the plane and switch between two images to realize the air-jetting effect======
    if me.active:
        screen.blit(animation_frame("me", me.images, 3), me.rect)  # Change the image every 3 frames

    # =============When my plane is hit=============
    if me.active:
        if me.hit:
            screen.blit(animation_frame("me_hit", me.images_hit, 2), me.rect)
            if all_animation.get("me_hit").is_finished:
                me.hit = False

    # =============Display the user score====================
    score_text = score_font.render("Score: {}".format(str(score)), True, BLACK)
    screen.blit(score_text, (10, 5))

    pygame.display.flip()
    clock.tick(frame_rate)  # Set the frame rate to 60
