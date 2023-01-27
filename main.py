import pygame
import random

from pygame.locals import *

class Square(pygame.sprite.DirtySprite):
    color = ()

    def __init__(self):
        super(Square, self).__init__()

        self.surf = pygame.Surface((35, 35))

        value = random.randint(0,255)

        self.color = ((value, 200, 255))

        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()

    def update(self):
        # pygame.sprite.DirtySprite.update(self)
        if(self.color == (0,0,0)):
            value = random.randint(0,255)
            self.color = ((value, 200, 255))
        else:
            self.color = (0,0,0)
        self.surf.fill(self.color)
        self.dirty = 1

def start_game(gameOn):
    # Process inputs

    cols = 20
    rows = 20

    nodes = [[Square() for j in range(cols)] for i in range(rows)]

    for i in range(rows):
        for j in range(cols):
            screen.blit(nodes[i][j].surf, (i*36, j*36))

    while gameOn:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    gameOn = False
            if event.type == MOUSEBUTTONUP:
                x = pygame.mouse.get_pos()[0] // 36
                y = pygame.mouse.get_pos()[1] // 36
                nodes[x][y].update()
            elif event.type == QUIT:
                gameOn = False

        pygame.display.flip()


pygame.init()

screen = pygame.display.set_mode((800,600))
screen.fill((255, 255, 255))



start_game(True)
