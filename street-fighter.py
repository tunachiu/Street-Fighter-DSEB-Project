import pygame
from pygame import mixer

pygame.init()  # call all the features in pygame package

clock = pygame.time.Clock()
fps = 60

# game window
screen_width = 1200
screen_height = 450

screen = pygame.display.set_mode((screen_width, screen_height))  # set the size the the game window
pygame.display.set_caption('Street Fighter')  # setting the title for the game window
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# background music
mixer.music.load('sounds/background music.mp3')
mixer.music.play(-1)
jump_sound = mixer.Sound('sounds/jump.mp3')
punch_sound = mixer.Sound('sounds/attack/punch.mp3')
kick_sound = mixer.Sound('sounds/attack/kick.mp3')


# load images
# background image

def Game_Start():
    pass


def Game_Over():
    pass


class Background:
    def __init__(self):
        """Set components to manage multiple frames of the background"""
        self.background_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(8):
            bg = pygame.image.load(f'background/{i}.gif')
            scale = screen_width / bg.get_width()
            bg = pygame.transform.scale(bg, (bg.get_width() * scale, bg.get_height() * scale))
            self.background_list.append(bg)
        self.background_img = self.background_list[self.frame_index]

    def update(self):
        """Update images for the animation"""
        animation_cooldown = 100
        # handle animation
        # update images
        self.background_img = self.background_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.background_list):
                self.frame_index = 0

    def draw(self):
        """Draw the background"""
        screen.blit(self.background_img, (0, 0))


class Energy_Bar:
    """Class for the energy bar of each fighter"""
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
    def energy_display(self):
        pass

# fighter class
class Fighter:
    def __init__(self, x, y, name, img_scale):
        self.name = name
        self.max_hp = 200
        self.hp = 200
        self.alive = True
        self.action = 'idle'
        self.scale = img_scale  # scale to adjust the size of the character image
        img = pygame.image.load(f'char_img/{self.name}/{self.action}.gif')
        self.image = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        self.frame_index = 0
        self.x = x
        self.y = y
        shot_image = pygame.image.load(f'char_img/{self.name}/power_shot.png')
        self.shot_image = pygame.transform.scale(shot_image, (shot_image.get_width() / 2, shot_image.get_height() / 2))
        self.special_sound = mixer.Sound(f'sounds/attack/power {self.name}.mp3')
        self.speed = 10
        self.jump = False
        self.in_air = False
        self.flip = False
        self.direction = 1
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0
        self.special_power = Power_Shoot(self.x, self.y, self.shot_image, self.special_sound, self.direction)
        self.energy = Energy_Bar(self.name, self.hp)

    def move(self, move_left, move_right):  # method for moving left and right
        """Method for character movement left, right"""
        if move_left and self.x >= 0:  # check move and set boundary so the image won't move outside the screen
            self.x -= self.speed
            self.flip = True
            self.direction = -1
        if move_right and self.x <= screen_width - self.image.get_width() - self.speed:
            self.x += self.speed
            self.flip = False
            self.direction = 1

    def jumping(self):
        """Method for jump"""
        jump_step = 0
        GRAVITY = 0.3
        if first_fighter.jump and self.in_air == False:
            self.action = 'jump'
            self.draw()
            jump_sound.play()
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 20:
            self.vel_y = 20
        jump_step += self.vel_y

        # check collision with floor
        if self.y + jump_step > 250:
            jump_step = 250 - self.y
            self.in_air = False
        # update rectangle position
        self.y += jump_step
        self.special_power.y = self.y

    def draw(self):  # draw the character
        """Draw the fighter"""
        img = pygame.image.load(f'char_img/{self.name}/{self.action}.gif')
        self.image = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.x, self.y))

    def attack(self):
        if self.action == 'punch':
            punch_sound.play()
            self.draw()
        if self.action == 'kick':
            kick_sound.play()
            self.draw()
        if self.action == 'special_power':
            self.special_sound.play()
            self.draw()
            self.special_power.shoot()

        if pygame.time.get_ticks() - self.update_time > 600:
            self.update_time = pygame.time.get_ticks()
            self.action = 'idle'
            self.draw()

    def hp_check(self):
        if self.hp == 0:
            self.alive = False

class Power_Shoot():
    """Create special power object and shooting"""
    def __init__(self, x, y, shot_image, sound, direction):
        self.shot_image = shot_image
        self.sound = sound
        self.x = x
        self.y = y
        self.x_vel = 20
        self.direction = direction
        self.flip = False

    def shoot(self):
        self.x += self.x_vel * self.direction
        self.sound.play()
        if self.direction == 1:
            self.flip = False
        if self.direction == -1:
            self.flip = True
        screen.blit(pygame.transform.flip(self.shot_image, self.flip, False), (self.x, self.y))

# game variables
background_img = Background()
first_fighter = Fighter(250, 250, 'Guile', 0.8)
second_fighter = Fighter(950, 250, 'Ryu', 0.7)
move_left = False
move_right = False
power_count = 3
run = True

Game_Start()
while run:  # the run loop
    clock.tick(fps)  # set up the same speed of display for any animation in the game

    # draw background
    background_img.update()
    background_img.draw()

    # draw fighters:
    first_fighter.draw()
    first_fighter.hp_check()
    # first_fighter.test()
    second_fighter.draw()
    second_fighter.hp_check()

    for event in pygame.event.get():
        """Exit game input"""
        if event.type == pygame.QUIT:
            run = False

        """Character left/right movement input/ Hold pressed key"""
        if event.type == pygame.KEYDOWN:  # check for key presses
            if event.key == pygame.K_b:  # input key is B
                move_left = True
            if event.key == pygame.K_f:  # input key is F
                move_right = True
            if event.key == pygame.K_SPACE:
                first_fighter.jump = True
            if event.key == pygame.K_p:  # punch
                first_fighter.action = 'punch'
                if abs(first_fighter.x - second_fighter.x) < 90 and abs(first_fighter.y - second_fighter.y) < 80:
                    second_fighter.hp -= 10
            if event.key == pygame.K_k:  # kick
                first_fighter.action = 'kick'
                if abs(first_fighter.x - second_fighter.x) < 90 and abs(first_fighter.y - second_fighter.y) < 80:
                    second_fighter.hp -= 10
            if event.key == pygame.K_s:  # special power
                power_count -= 1
                first_fighter.special_power.x = first_fighter.x
                first_fighter.special_power.y = first_fighter.y
                first_fighter.special_power.direction = first_fighter.direction
                if power_count >= 0 and first_fighter.hp >= first_fighter.max_hp * 0.2:
                    first_fighter.action = 'special_power'
                    second_fighter.hp -= 30

        if event.type == pygame.KEYUP:  # check for key releases
            if event.key == pygame.K_b:  # key B released
                move_left = False
            if event.key == pygame.K_f:  # key F is released
                move_right = False

    #if first_fighter.alive:
    first_fighter.move(move_left, move_right)
    first_fighter.attack()
    first_fighter.jumping()
    if first_fighter.hp <= 0 or second_fighter.hp <= 0:
        Game_Over()
    #print(second_fighter.hp)
    print(first_fighter.special_power.x)

    pygame.display.update()  # to update all added images
pygame.quit()
