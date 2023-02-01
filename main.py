import pygame
import random

from pygame.locals import *
# Kit Bazner Cymbre Spoehr
class Square(pygame.sprite.DirtySprite):
    color = ()

    # Sets the initial state of the Square class
    def __init__(self):
        super(Square, self).__init__()

        self.surf = pygame.Surface((35, 35))

        self.color = ((0, 0, 0))

        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()

    # This function sets the color of the square to be some random color.
    def born(self):
        value = random.randint(0,255)

        self.color = ((value, 200, 255))

        self.surf.fill(self.color)
        self.dirty = 1

    # This functino sets the color of the square to be black
    def die(self):
        self.color = ((0,0,0))

        self.surf.fill(self.color)
        self.dirty = 1

    # This function switches whether the square is black or colored
    def update(self):
        if(self.color == (0, 0, 0)):
            value = random.randint(0, 255)
            self.color = ((value, 200, 255))
        else:
            self.color = (0,0,0)
        self.surf.fill(self.color)
        self.dirty = 1

class Player(pygame.sprite.DirtySprite):
    # This sets the initial values for the player
    def __init__(self):
        super(Player, self).__init__()

        self.surf = pygame.Surface((35, 35))

        self.color = ((255, 255, 255))

        self.x= 0
        self.y= 0

        self.dirty = 2

        self.body = pygame.draw.circle(self.surf, self.color, (18, 18), 15)

    # This function return whether the desired position is a valid place that a player token can move
    # Params: 
    # Square[][] squares, which represents the board
    # int row, which represents the row the player token would like to move to
    # int column, which represents the  column the player token would like to move to
    # Returns: boolean, whether or not that is a valid move
    def can_move(self, squares, row, col):
        return -1 < row < 20 and -1 < col < 20 and squares[row][col].color == (0, 0, 0)

    # This function is a helper function to move the player token back to start
    def reset_position(self):
        self.x = 0
        self.y = 0

    # This function facilitates player token movement
    # Params:
    # Square[][] squares, which represents the board
    # int xMove, which represents the row the player token would like to move to
    # int yMove, which represents the  column the player token would like to move to
    def update(self, squares, rows, cols, xMove, yMove):
        self.x += xMove
        self.y += yMove
        if not self.can_move(squares, self.x//36, self.y//36):
            self.x -= xMove
            self.y -= yMove
            return
        if self.x//36 == 19 == self.y//36:
            print("You won.")
            reset(squares, rows, cols, self)



# Checks to see if a given index is valid on the board
# 
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

def reset(squares, rows, cols, playerToken):
    for x in range(rows):
        for y in range(cols):
            squares[x][y].die()
    playerToken.reset_position()

def generate_maze(squares, rows, cols):
    alive = 0
    for x in range(rows):
        for y in range(cols):
            if squares[x][y].color != (0,0,0):
                alive += 1
            num_living = get_num_living(squares, find_neighbors((x,y)))
            if num_living == 3:
                squares[x][y].born()
            if num_living < 1 or num_living > 3:
                squares[x][y].die()
    return alive

def gen_random_seed(squares, rows, cols):
    distance = random.randint(0, 5)
    for x in range(rows):
        for y in range (cols):
            if distance == 0:
                distance = random.randint(1, 6)
                squares[x][y].born()
            distance -= 1

def start_game(gameOn):
    # Process inputs
    numAlive = 0
    is_generating_maze = False
    cols = 20
    rows = 20

    FRAMERATE = 60
    frameMili = 1000 // FRAMERATE
    squares = [[Square() for j in range(cols)] for i in range(rows)]
    token = Player()

    while gameOn:
        elapsed = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    gameOn = False
                if event.key == K_g:
                    is_generating_maze = True
                if event.key == K_r:
                    gen_random_seed(squares, rows, cols)
                if event.key == K_UP or event.key == K_w:
                    token.update(squares, rows, cols, 0,-36)
                if event.key == K_DOWN or event.key == K_s:
                    token.update(squares, rows, cols, 0,36)
                if event.key == K_RIGHT or event.key == K_d:
                    token.update(squares, rows, cols, 36,0)
                if event.key == K_LEFT or event.key == K_a:
                    token.update(squares,  rows, cols, -36,0)
            if event.type == MOUSEBUTTONUP:
                x = pygame.mouse.get_pos()[0] // 36
                y = pygame.mouse.get_pos()[1] // 36
                if x < 20 and y < 20:
                    squares[x][y].update()
            elif event.type == QUIT:
                gameOn = False

        if is_generating_maze:
            newAlive = generate_maze(squares, rows, cols)
            if newAlive == numAlive:
                is_generating_maze = False
            numAlive = newAlive
            squares[0][0].die()
            token.reset_position()

        for i in range(rows):
            for j in range(cols):
                if squares[i][j].dirty == 1:
                    screen.blit(squares[i][j].surf, (i*36, j*36))
        screen.blit(token.surf, (token.x, token.y))

        
        pygame.display.flip()

        delta = pygame.time.get_ticks() - elapsed
        difference = frameMili - delta
        pygame.time.delay(difference)


pygame.init()

screen = pygame.display.set_mode((720,720))
screen.fill((255, 255, 255))
gameState = True
start_game(gameState)
