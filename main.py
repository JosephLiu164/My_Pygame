import pygame
import pyganim
import myplane
import enemy

from pygame.locals import *
from sys import exit


# =========================Game initialization==========================
pygame.init()
pygame.mixer.init()  # Initialize mixer
bg_size = WIDTH, HEIGHT = 600, 800  # Set background size
screen = pygame.display.set_mode(bg_size)  # Set screen
pygame.display.set_caption("Space Shooter")
background = pygame.image.load("image/background.png")  # Load background image
background_size = w,h = background.get_size()
background_rect = background.get_rect()
clock = pygame.time.Clock() # Set frame rate
frame_rate = 60

x=0 #Set the initial background position
y=0
x1=0
y1=-h

# ==================Load sound and music================
pygame.mixer.music.load("sound/game_music.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1) # Repeat background music
me_down_sound = pygame.mixer.Sound("sound/game_over.wav")
me_down_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)

#=================A general animation class and function==================
class Animation():
    current_frame = 0
    current_image = -1
    is_finished = False

    def __init__(self,name,images,interval = 5):
        self.name = name
        self.images = images
        self.interval = interval

all_animation = {}


# usage: screen.blit(animation_frame("destroy_me",me.destroy_images,5),me.rect)
def animation_frame(name, images, interval):
    if all_animation.get(name):
        animation = all_animation[name]
    else:
        animation = Animation(name, images, interval)
        all_animation.update({name:animation})
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

# ========Controlling function of initializing enemy plane=======
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

# ==============Initializing my plane==============
me = myplane.MyPlane(bg_size)
switch_image = False

# ==============Creating enemy plane instances==============
enemies = pygame.sprite.Group() # Creating all enemy plane groups
small_enemies = pygame.sprite.Group()  # Creating small enemy plane group
add_small_enemies(small_enemies, enemies, 1)  # Creating small enemy plane instances


# =================Variables related to destroying animation =================
plane_jet_f = frame_rate # control the frequency of switching the images (animation) of my plane


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    # ===========Combine the plane jet value with frame rate to achieve some animations=======
    if plane_jet_f == 0:
        plane_jet_f = frame_rate
    plane_jet_f -= 1

    # ============Set the background to scroll (repeatedly blit same two images)========
    screen.blit(background, (x,y))
    screen.blit(background,(x1,y1))
    y1 += 5
    y += 5
    if y > h:
        y = -h
    if y1 > h:
        y1 = -h

    # =================Control the plane=================
    if me.active == True:
        key_pressed = pygame.key.get_pressed()  # Get user input sequence
        if key_pressed[K_w] or key_pressed[K_UP]:
            me.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.move_right()

    # ========Draw the plane and switch between two images to realize the air-jetting effect======
    if me.active == True:
        screen.blit(animation_frame("me", me.images, 3), me.rect) # Change the image every 3 frames

    # =====Detect whether there is a collision between my plane and enemy planes======
    enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
    my_plane_destroyed = USEREVENT + 1
    if enemies_down: # If the list of collision detection is not empty, then collision happens.
        me.active = False
        for e in enemies_down:
            e.active = False # Enemy plane destroyed

    # =========When my plane is destroyed, create the animation===========
    if me.active == False:
        screen.blit(animation_frame("me_destroy", me.destroy_images, 5), me.rect)
        if is_finished("me_destroy"):# When the anmation is over
            me.reset()

    # =========Blit the small enemies and have them move==========
    for each in small_enemies:
        if each.active:
            each.move()
            screen.blit(each.image, each.rect)

    # =========When small enemy plane is destroyed, create the animation===========
    for each in small_enemies:
        if not each.active:
            enemy1_down_sound.play()
            screen.blit(animation_frame("enemy_{}".format(id(each)), each.destroy_images, 5), each.rect)
            if all_animation.get("enemy_{}".format(id(each))).is_finished:
                each.reset()

    pygame.display.flip()
    clock.tick(frame_rate)  # Set the frame rate to 60






