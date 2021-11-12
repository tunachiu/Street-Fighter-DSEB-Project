import pygame

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
        self.frame_index = 0
        img = pygame.image.load(f'char_img/{self.name}/{self.action}.gif')
        self.image = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        self.x = x  # Position of fighter respect to x axis
        self.y = y  # Position of fighter respect to y axis
        self.special_power = ['Guile', 'Ryu']
        self.speed = 10
        self.flip = False
        self.jump = False

    def update_action(self, new_action):
        """Check if the new action is different to the previous one"""
        if new_action != self.action:
            self.action = new_action

    def image_update(self):
        """Update character image according to char action"""
        img = pygame.image.load(f'char_img/{self.name}/{self.action}.gif')
        self.image = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))

    def move(self, move_left, move_right, jump):  # method for moving left and right
        if move_left and self.x >= 0:  # check move and set boundary so the image won't move outside the screen
            self.x -= self.speed
            self.flip = True
        if move_right and self.x <= screen_width - self.image.get_width() - self.speed:
            self.x += self.speed
            self.flip = False


        jump_step = 20
        if self.jump and self.y >= 50:  # jump up
            self.action = 'jump'
            self.image_update()
            self.y -= jump_step
            jump_step -= 20
            # jump back to the ground
            # gravity = 10
            #if self.y == 100:
                #jump_step = 250 - self.y
                #self.y += jump_step
                #self.action = 'idle'
                #self.image_update()
            #self.jump = False

    def attack(self):
        if self.action == 'punch':
            self.image_update()
        elif self.action == 'kick':
            self.image_update()
        elif self.action == 'special_power':
            self.image_update()

    def draw(self):  # draw the character
        """Draw the fighter"""
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.x, self.y))


background_img = Background()
first_fighter = Fighter(250, 250, 'Guile', 30, 0.8)
second_fighter = Fighter(950, 250, 'Ryu', 30, 0.7)
move_left = False
move_right = False
run = True


while run:  # the run loop
    clock.tick(fps)  # set up the same speed of display for any animation in the game

    # draw background
    background_img.update()
    background_img.draw()

    # draw fighters:
    first_fighter.draw()
    # first_fighter.test()
    second_fighter.draw()
    first_fighter.image_update()

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
            if event.key == pygame.K_j:
                first_fighter.jump = True
            elif event.key == pygame.K_p:  # punch
                first_fighter.action = 'punch'
            elif event.key == pygame.K_k:  # punch
                first_fighter.action = 'kick'
            elif event.key == pygame.K_s:  # punch
                first_fighter.action = 'special_power'

        if event.type == pygame.KEYUP:  # check for key releases
            if event.key == pygame.K_b:  # key B released
                move_left = False
            elif event.key == pygame.K_f:  # key F is released
                move_right = False

    if first_fighter.alive:
        first_fighter.move(move_left, move_right, first_fighter.jump)
        first_fighter.attack()
        #if first_fighter.action != 'idle':
            #first_fighter.update_action('idle')
            #first_fighter.image_update()


    pygame.display.update()  # to update all added images
pygame.quit()
