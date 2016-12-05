import pygame
import traceback
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
clock = pygame.time.Clock()  # Set frame rate
frame_rate = 60

# ==================Load sound and music================
pygame.mixer.music.load("sound/game_music.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)  # Repeat background music
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/game_over.wav")
me_down_sound.set_volume(0.2)
SmallEnemy_destroy_sound = SmallEnemy2_destroy_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
SmallEnemy_destroy_sound.set_volume(0.2)
SmallEnemy2_destroy_sound.set_volume(0.2)
MidEnemy_destroy_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
MidEnemy_destroy_sound.set_volume(0.2)
BigEnemy_destroy_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
BigEnemy_destroy_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_double_laser.wav")
get_bullet_sound.set_volume(0.2)
level_up_sound = pygame.mixer.Sound("sound/achievement.wav")
level_up_sound.set_volume(0.2)


# ===============Colors in common use =================
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (181,75,0)
GREEN = (0,181,24)
YELLOW = (181,175,0)

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

def add_small_enemies2(small_enemies2, enemies, num):
    for i in range(num):
        e = enemy.SmallEnemy2(bg_size)
        small_enemies2.add(e)
        enemies.add(e)

def increase_speed(plane):
    for each in plane:
        if each.bullet:
            each.bullet.shooting_interval -= each.bullet.shooting_interval//3

def main():

    # =============Set background image==============
    background = pygame.image.load("image/background.png")  # Load background image
    gameover_image = pygame.image.load("image/game_over.png")  # game over background image
    gameover_rect = gameover_image.get_rect()
    game_over = False
    restart_button_normal = pygame.image.load("image/restart.png")
    restart_button_hover = pygame.image.load("image/restart_hover.png")
    restart_button_rect = restart_button_normal.get_rect()
    restart_button_rect.left, restart_button_rect.top = (170,500)

    x = 0  # Set the initial background position
    y = 0
    x1 = 0
    y1 = -HEIGHT

    # ==============Create enemy plane instances==============
    enemies = pygame.sprite.Group()  # Creating all enemy plane groups
    small_enemies = pygame.sprite.Group()  # Creating small enemy plane group
    add_small_enemies(small_enemies, enemies, 1)
    mid_enemies = pygame.sprite.Group()  # Create middle enemy plane group
    add_mid_enemies(mid_enemies, enemies, 1)
    big_enemies = pygame.sprite.Group()  # Create big enemy plane group
    add_big_enemies(big_enemies, enemies, 1)
    small_enemies2 = pygame.sprite.Group()  # Creating small enemy plane group
    add_small_enemies2(small_enemies2, enemies, 1)
    supplies = pygame.sprite.Group()

    # ==============Initializing my plane==============
    me = myplane.MyPlane(bg_size)

    # ===============user score=================
    score = 0
    score_font = pygame.font.SysFont("Chalkboard", 24)
    game_over_player_score_font = pygame.font.SysFont("Chalkboard", 48)
    high_score_font = pygame.font.SysFont("Chalkboard", 36)

    # =========== current game difficulty level ===========
    level = 1

    # ===============Create all the bullets=================
    enemy_bullets = pygame.sprite.Group()
    
    my_bullets = [] # Generate my bullets
    my_bullet_index = 0
    my_bullet_num = 300  # Amount of bullet instances
    for i in range(my_bullet_num):
        b = bullet.MyBullet()
        my_bullets.append(b)

    enemy_bullets1 = [] # Generate enemy bullets of middle enemy
    enemy_bullet1_index = 0
    enemy_bullet1_num = 300
    for i in range(enemy_bullet1_num):
        b = bullet.EnemyBullet1()
        enemy_bullets1.append(b)
        enemy_bullets.add(b)

    enemy_bullets2 = [] # Generate enemy bullets of big enemy
    enemy_bullet2_index = 0
    enemy_bullet3_num = 300
    for i in range(enemy_bullet3_num):
        b = bullet.EnemyBullet2()
        enemy_bullets2.append(b)
        enemy_bullets.add(b)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        # =================Control the plane=================
        control_plane_x = 0
        control_plane_y = 0
        if me.active:
            key_pressed = pygame.key.get_pressed()  # Get user input sequence
            if key_pressed[K_w] or key_pressed[K_UP]:
                control_plane_y = 1
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                control_plane_y = -1
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                control_plane_x = -1
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                control_plane_x = 1
            movement_angle = atan2(control_plane_y,control_plane_x)
            if control_plane_x == 0 and control_plane_y == 0:
                me.move(movement_angle, False)
            else:
                me.move(movement_angle, True)

            # ==============Game difficulty level================
            critical_score = 4000 * 3 ** (level-1)
            if score >= critical_score:
                level += 1
                level_up_sound.play()
                add_small_enemies(small_enemies, enemies, 3)
                add_small_enemies2(small_enemies2, enemies, 2)
                add_mid_enemies(mid_enemies, enemies, 2)
                add_big_enemies(big_enemies, enemies, 1)
                bullet.EnemyBullet1.shooting_interval -= bullet.EnemyBullet1.shooting_interval//4
                bullet.EnemyBullet2.shooting_interval -= bullet.EnemyBullet2.shooting_interval//4
                for e in enemies:
                    e.energy += e.energy *1.3


        # ============Set the background to scroll (repeatedly blit same two images)========
        screen.blit(background, (x, y))
        screen.blit(background, (x1, y1))
        y1 += 3
        y += 3
        if y > HEIGHT:
            y = -HEIGHT
        if y1 > HEIGHT:
            y1 = -HEIGHT

        # =========Shooting bullets according to different bullet levels of my plane==========
        me.shooting_time_index += 1 # Shooting time index of my plane increase by 1 in every frame

        if me.active:
            if me.bullet_level <= 3:
                if me.bullet_level == 1:
                    bullet.MyBullet.shooting_interval = 20
                elif me.bullet_level == 2:
                    bullet.MyBullet.shooting_interval = 15
                elif me.bullet_level == 3:
                    bullet.MyBullet.shooting_interval = 11
                if me.shooting_time_index % bullet.MyBullet.shooting_interval == 0:  # Shoot a bullet at a certain interval
                    bullet_sound.play()
                    my_bullets[my_bullet_index].shoot(me.rect.midtop)
                    my_bullet_index = (my_bullet_index + 1) % my_bullet_num
            elif 4 <= me.bullet_level <= 6:
                if me.bullet_level == 4:
                    bullet.MyBullet.shooting_interval = 17
                elif me.bullet_level == 5:
                    bullet.MyBullet.shooting_interval = 12
                elif me.bullet_level == 6:
                    bullet.MyBullet.shooting_interval = 8
                if me.shooting_time_index % bullet.MyBullet.shooting_interval == 0:
                    bullet_sound.play()
                    my_bullets[my_bullet_index].shoot((me.rect.centerx - 28, me.rect.centery))
                    my_bullets[my_bullet_index + 1].shoot((me.rect.centerx + 23, me.rect.centery))
                    my_bullet_index = (my_bullet_index + 2) % my_bullet_num
                    if my_bullet_index >= my_bullet_num-1:
                        my_bullet_index = 0

            elif 7<= me.bullet_level <= 9:
                if me.bullet_level == 7:
                    bullet.MyBullet.shooting_interval = 9
                elif me.bullet_level == 8:
                    bullet.MyBullet.shooting_interval = 7
                elif me.bullet_level == 9:
                    bullet.MyBullet.shooting_interval = 4
                if me.shooting_time_index % bullet.MyBullet.shooting_interval == 0:
                    bullet_sound.play()
                    my_bullets[my_bullet_index].shoot((me.rect.centerx - 28, me.rect.centery),105)
                    my_bullets[my_bullet_index + 1].shoot((me.rect.centerx-4, me.rect.centery),90)
                    my_bullets[my_bullet_index + 2].shoot((me.rect.centerx + 23, me.rect.centery),75)
                    my_bullet_index = (my_bullet_index + 3) % my_bullet_num
                    if my_bullet_index >= my_bullet_num - 2:
                        my_bullet_index = 0

            elif me.bullet_level == 10:
                bullet.MyBullet.shooting_interval = 4
                if me.shooting_time_index % bullet.MyBullet.shooting_interval == 0:
                    bullet_sound.play()
                    my_bullets[my_bullet_index].shoot((me.rect.centerx - 25, me.rect.centery), 120)
                    my_bullets[my_bullet_index + 1].shoot((me.rect.centerx - 4, me.rect.centery), 90)
                    my_bullets[my_bullet_index + 2].shoot((me.rect.centerx + 17, me.rect.centery), 60)
                    my_bullets[my_bullet_index + 3].shoot((me.rect.centerx + 14, me.rect.centery), 75)
                    my_bullets[my_bullet_index + 4].shoot((me.rect.centerx - 22, me.rect.centery), 105)
                    my_bullet_index = (my_bullet_index + 5) % my_bullet_num
                    if my_bullet_index >= my_bullet_num - 4:
                        my_bullet_index = 0

        # ================The move of my bullets===========
        if me.active:
            for b in my_bullets:
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
        for b in my_bullets:
            if b.active:
                enemies_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                if enemies_hit:
                    b.active = False
                    for e in enemies_hit:
                        e.energy -= 1
                        e.hit = True  # Plane is hit
                        if e.energy <= 0:
                            e.active = False

        # =========Detect whether my plane touches enemy_bullets1===========
        if me.active:
            bullets_hit = pygame.sprite.spritecollide(me, enemy_bullets, False,
                                                       pygame.sprite.collide_mask)
            for b in bullets_hit:
                if b.active:
                    me.hit = True
                    me.life -= b.power
                    b.active = False


        # =====Detect whether there is a collision between my plane and enemy planes======
        if me.active:
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down:  # If the list of collision detection is not empty, then collision happens.
                for e in enemies_down:
                    if e.active:
                        me.life -= e.crashing_power
                        e.active = False  # Enemy plane destroyed

        # =====Detect whether the plane touches the supply======
        if me.active:
            supplies_got = pygame.sprite.spritecollide(me, supplies, True, pygame.sprite.collide_mask)
            for s in supplies_got:
                if s.show:
                    get_bomb_sound.play()

                    # ================Bullet Supply==============
                    if isinstance(s, supply.BulletSupply):
                        me.bullet_level += 1
                        if me.bullet_level >= 10:
                            me.bullet_level = 10
                    elif isinstance(s, supply.LifeSupply):
                        me.life += 30
                        if me.life >= 100:
                            me.life = 100
                    s.show = False


        # =========Blit the big enemies and have them move==========
        for each in big_enemies:
            if each.active:
                each.move()
                each.shooting_time_index += 1
                screen.blit(animation_frame("big_enemy_{}".format(id(each)), each.images, 3), each.rect)
                if each.shooting_time_index % bullet.EnemyBullet2.shooting_interval == 0:  # Shoot a bullet at a certain interval
                    bullet3_angle = (180/pi)*atan2((each.rect.centery - me.rect.centery),
                                             (me.rect.centerx- each.rect.centerx))
                    enemy_bullets2[enemy_bullet2_index].shoot((each.rect.centerx - 10, each.rect.centery), bullet3_angle)  # Big enemy shooting bullets
                    enemy_bullet2_index = (enemy_bullet2_index + 1) % enemy_bullet3_num


        # =========Blit the mid enemies and have them move==========
        for each in mid_enemies:
            if each.active:
                each.move()
                each.shooting_time_index += 1
                screen.blit(each.image, each.rect)
                if each.shooting_time_index % bullet.EnemyBullet1.shooting_interval == 0:  # Shoot a bullet at a certain interval
                    enemy_bullets1[enemy_bullet1_index].shoot((each.rect.centerx - 3, each.rect.centery),
                                                  -90)  # Shooting bullets by middle enemy
                    enemy_bullet1_index = (enemy_bullet1_index + 1) % enemy_bullet1_num


        # =========Blit the small enemies and have them move==========
        for each in small_enemies:
            if each.active:
                each.move()
                screen.blit(each.image, each.rect)

        # =========Blit the small enemies2 and have them move==========
        for each in small_enemies2:
            if each.active:
                if each.init_position_left < 0:
                     each.move(-60)
                else:
                     each.move(-120)
                screen.blit(each.image, each.rect)

        # =========When the big enemy is hit==============
        for each in big_enemies:
            if each.active:
                if each.hit:
                    screen.blit(each.image_hit, each.rect)
                    each.hit = False

        # =========When the middle enemy is hit==============
        for each in mid_enemies:
            if each.active:
                if each.hit:
                    screen.blit(each.image_hit, each.rect)
                    each.hit = False

        # =========When enemy is destroyed===========
        for each in enemies:
            destroy_sound = globals()["{}_destroy_sound".format(each.__class__.__name__)]
            destroy_frame_len = len(each.destroy_images)
            if not each.active:
                destroy_sound.play()
                screen.blit(animation_frame("enemy_{}".format(id(each)),
                                            each.destroy_images,
                                            destroy_frame_len),
                            each.rect)
                if all_animation.get("enemy_{}".format(id(each))).is_finished:
                    score += each.destroy_score
                    if getattr(each, "supply", False):
                        each.supply.drop(((each.rect.centerx - each.supply.rect.width / 2),
                                          each.rect.centery))  # Dropping supplies when destroyed
                        supplies.add(each.supply)
                    each.reset()

        # ================The move of the bullets from big enemy===========-
        for b in enemy_bullets2:
            if b.active:
                b.move()
                screen.blit(b.image, b.rect)

        # ================The move of the bullets from middle enemy===========-
        for b in enemy_bullets1:
            if b.active:
                b.move()
                screen.blit(b.image, b.rect)

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
                screen.blit(animation_frame("me_hit", me.images_hit, 1), me.rect)
                if all_animation.get("me_hit").is_finished:
                    me.hit = False

        # =============Display the user score====================
        score_text = score_font.render("Score: {}".format(str(score)), True, BLACK)
        screen.blit(score_text, (10, 40))

        # =============Draw the remaining blood of my plane================
        pygame.draw.line(screen, (75,75,75), (10,20),(200,20), 30)
        if me.life/100 > 0.3:
            energy_color = GREEN
        elif 0.15<= me.life/100 <= 0.3:
            energy_color = YELLOW
        elif 0 <= me.life/100 < 0.15:
            energy_color = RED
        pygame.draw.line(screen, energy_color, (10,20), ((me.life/100)*190+11,20), 30)
        blood_bar = Rect(10, 20, 190, 20)

        # =============Detect whether my plane is destroyed==============
        if game_over == False:
            if me.life <= 0:
                me.life = 0
                me.active = False
                # When my plane is destroyed, create the animation
                screen.blit(animation_frame("me_destroy", me.destroy_images, 5), me.rect)

        # =============Show the game over screen============
        if me.active == False:
            if all_animation.get("me_destroy").is_finished:
                game_over = True

        # =============When game over==============
        if game_over: # Detect the restart button
            restart_button = restart_button_normal
            if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
                restart_button = restart_button_hover
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        game_over = False
                        pygame.mixer.music.play(-1)
                        main()

            with open("high_score.txt", "r") as f: # Load the high score data from txt file
                high_score = int(f.read())
            if score > high_score:  # If player's scoring is higher, then save it
                with open("high_score.txt", "w") as f:
                    f.write(str(score))
            player_score_text = game_over_player_score_font.render("{}".format(score), True, WHITE)
            high_score_text = high_score_font.render("{}".format(high_score), True, WHITE)
            screen.blit(gameover_image, gameover_rect) # Show game over screen
            screen.blit(player_score_text, (230, 210))
            screen.blit(high_score_text, (230, 390))
            screen.blit(restart_button, restart_button_rect)
            pygame.mixer.music.stop()  # Stop the background music

        pygame.display.flip()
        clock.tick(frame_rate)  # Set the frame rate to 60

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()