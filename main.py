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

delay = frame_rate # control the frequency of switching the images of my plane (delay parameter)


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

# ====================Index of the destroy images====================
e1_destroy_index = 0
e2_destroy_index = 0
e3_destroy_index = 0
me_destroy_index = 0

# =================Destroy animation of my plane=================
destroy_my_plane = pyganim.PygAnimation([("image/hero_blowup_n1.png", 200),
                                         ("image/hero_blowup_n2.png", 200),
                                         ("image/hero_blowup_n3.png", 200),
                                         ("image/hero_blowup_n4.png", 200)])
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    # ===========Combine the delay value with frame rate to achieve some animations=======
    if delay == 0:
        delay = frame_rate
    delay -= 1

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
    key_pressed = pygame.key.get_pressed()  # Get user input sequence
    if key_pressed[K_w] or key_pressed[K_UP]:
        me.move_up()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        me.move_down()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        me.move_left()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        me.move_right()

    # =========When the plane is destroyed===========
    if not me.active:
        me_down_sound.play()

        me.reset()

    # ========Draw the plane and switch between two images to realize the air-jetting effect======
    if me.active:
        if delay % 3 == 0: # Change the image every 3 frames
            switch_image = not switch_image
        if switch_image:
            screen.blit(me.image1, me.rect)  #
        else:
            screen.blit(me.image2, me.rect)

    # =====Detect whether there is a collision between my plane and enemy planes======
    enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
    if enemies_down: # If the list of collision detection is not empty, then collision happens.
        me.active = False
        for e in enemies_down:
            e.active = False # Enemy plane destroyed

    # =========Blit the small enemies and have them move==========
    for each in small_enemies:
        each.move()
        screen.blit(each.image, each.rect)


    # =====Drawing the destroying image of my plane and enemy plane======
    if not me.active:
        destroy_my_plane.blit(screen, me.rect)

    # if not me.active:
    #     if delay % 3 == 0:
    #         screen.blit(me.destroy_images[me_destroy_index], me.rect)  # Drawing the destroying animation
    #         me_destroy_index = (me_destroy_index + 1) % 4
    #     if me_destroy_index == 0:

    pygame.display.flip()
    clock.tick(frame_rate)  # Set the frame rate to 60






