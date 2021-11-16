import pygame
COLOR_INACTIVE = (255,140,0)
class InputBox:

    def __init__(self, x, y, w, h, font_size,new_name=''):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.name = ''
        self.active = False
        self.color = COLOR_INACTIVE

        self.font = pygame.font.Font("BERNHC.TTF", font_size)
        self.player_name_surface = self.font.render(new_name, True, self.color)
        self.border = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, screen):

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.border.collidepoint(event.pos):
                    self.active = True

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        if len(self.name) < 6:
                            self.name += event.unicode


        pygame.draw.rect(screen, self.color, self.border, 2)
        screen.blit(self.player_name_surface, self.x + 5, self.y+2 )

