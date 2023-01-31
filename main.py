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

    def born(self):
        value = random.randint(0,255)

        self.color = ((value, 200, 255))

        self.surf.fill(self.color)
        self.dirty = 1

    def die(self):
        self.color = ((0,0,0))

        self.surf.fill(self.color)
        self.dirty = 1

    def update(self):
        # pygame.sprite.DirtySprite.update(self)
        if(self.color == (0,0,0)):
            value = random.randint(0,255)
            self.color = ((value, 200, 255))
        else:
            self.color = (0,0,0)
        self.surf.fill(self.color)
        self.dirty = 1

def is_valid_index(index):
    return index[0] > -1 and index[0] < 20 and index[1] > -1 and index[1] < 20 

def find_neighbors(index):
    neighbors = []
    right = index[0] + 1
    left = index[0] - 1
    up = index[1] + 1
    down = index[1] - 1
    if is_valid_index((index[0], up)): neighbors.append((index[0], up))
    if is_valid_index((right, up)): neighbors.append((right, up))
    if is_valid_index((left, up)): neighbors.append((left, up))
    if is_valid_index((index[0], down)): neighbors.append((index[0], down))
    if is_valid_index((right, down)): neighbors.append((right, down))
    if is_valid_index((left, down)): neighbors.append((left, down))
    if is_valid_index((right, index[1])): neighbors.append((right, index[1]))
    if is_valid_index((left, index[1])): neighbors.append((left, index[1]))
    return neighbors

def get_num_living(squares, neighbors):
    num_living = 0
    for n in neighbors:
        if(squares[n[0]][n[1]].color != (0,0,0)):
            num_living = num_living + 1
    return num_living

def generate_maze(squares, rows, cols):
    for x in range(rows):
        for y in range(cols):
            num_living = get_num_living(squares, find_neighbors((x,y)))
            if num_living == 3:
                squares[x][y].born()
            if num_living < 1 or num_living > 3:
                squares[x][y].die()


def start_game(gameOn):
    # Process inputs

    cols = 20
    rows = 20

    squares = [[Square() for j in range(cols)] for i in range(rows)]

    generate_maze(squares, rows, cols)

    while gameOn:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    gameOn = False
            if event.type == MOUSEBUTTONUP:
                x = pygame.mouse.get_pos()[0] // 36
                y = pygame.mouse.get_pos()[1] // 36
                if x < 20 and y < 20:
                    squares[x][y].update()
            elif event.type == QUIT:
                gameOn = False

        for i in range(rows):
            for j in range(cols):
                if squares[i][j].dirty == 1:
                    screen.blit(squares[i][j].surf, (i*36, j*36))

        
        pygame.display.flip()


pygame.init()

screen = pygame.display.set_mode((800,600))
screen.fill((255, 255, 255))

start_game(True)
