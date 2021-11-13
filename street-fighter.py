import pygame
from pygame.constants import K_SPACE

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


# load images
# background image
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


# fighter class
class Fighter:
    def __init__(self, x, y, name, max_hp, img_scale):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.alive = True
        self.action = 'idle'
        self.scale = img_scale  # scale to adjust the size of the character image
        img = pygame.image.load(f'char_img/{self.name}/{self.action}.gif')
        self.image = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        self.frame_index = 0
        self.x = x  # Position of fighter respect to x axis
        self.y = y  # Position of fighter respect to y axis
        self.special_power = ['Guile', 'Ryu']
        self.speed = 10
        self.jump = False
        self.in_air = False
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0

    def move(self, move_left, move_right):  # method for moving left and right
        """Method for character movement left, right"""
        if move_left and self.x >= 0:  # check move and set boundary so the image won't move outside the screen
            self.x -= self.speed
            self.flip = True
        if move_right and self.x <= screen_width - self.image.get_width() - self.speed:
            self.x += self.speed
            self.flip = False

    def jumping(self):
        """Method for jump"""
        jump_step = 0
        GRAVITY = 0.3
        if first_fighter.jump and self.in_air == False:
            self.action = 'jump'
            self.draw()
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

    def draw(self):  # draw the character
        """Draw the fighter"""
        img = pygame.image.load(f'char_img/{self.name}/{self.action}.gif')
        self.image = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.x, self.y))

    def attack(self):
        if self.action == 'punch':
            self.draw()
        if self.action == 'kick':
            self.draw()
        if self.action == 'special_power':
            self.draw()
        if pygame.time.get_ticks() - self.update_time > 600:
            self.update_time = pygame.time.get_ticks()
            self.action = 'idle'
            self.draw()


# game variables
background_img = Background()
first_fighter = Fighter(250, 250, 'Guile', 30, 0.8)
second_fighter = Fighter(950, 250, 'Ryu', 30, 0.7)
move_left = False
move_right = False
run = True

while run:  # the run loop
    punch = False
    kick = False
    special_power = False
    clock.tick(fps)  # set up the same speed of display for any animation in the game

    # draw background
    background_img.update()
    background_img.draw()

    # draw fighters:
    first_fighter.draw()
    # first_fighter.test()
    second_fighter.draw()

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
            if event.key == pygame.K_k:  # kick
                first_fighter.action = 'kick'
            if event.key == pygame.K_s:  # special power
                first_fighter.action = 'special_power'

        if event.type == pygame.KEYUP:  # check for key releases
            if event.key == pygame.K_b:  # key B released
                move_left = False
            if event.key == pygame.K_f:  # key F is released
                move_right = False

    if first_fighter.alive:
        first_fighter.move(move_left, move_right)
        first_fighter.attack()
        first_fighter.jumping()

    pygame.display.update()  # to update all added images
pygame.quit()