import pygame

class InputBox:

    def __init__(self, x, y, new_name=''):
        self.x = x
        self.y = y
        self.name = ''
        self.active = False
        self.font = pygame.font.Font("BERNHC.TTF", 32)
        self.player_name_surface = self.font.render(new_name, True, WHITE)
        self.border = pygame.Rect(self.x, self.y, 150, 50)

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

        if self.active:
            pygame.draw.rect(screen, WHITE, self.border, 2)
            screen.blit(self.player_name_surface, self.x + 5, self.y+2 )

