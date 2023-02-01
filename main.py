import pygame
import random

from pygame.locals import *
# Kit Bazner Cymbre Spoehr

class Board():
    rows = 20
    cols = 20

    def __init__(self):
        self.squares = [[Square() for j in range(self.cols)] for i in range(self.rows)]


    def generate_maze(self):
        alive = 0
        for x in range(self.rows):
            for y in range(self.cols):
                if self.squares[x][y].color != (0,0,0):
                    alive += 1
                num_living = get_num_living(self.squares, self.find_neighbors((x,y)))
                if num_living == 3:
                    self.squares[x][y].born()
                if num_living < 1 or num_living > 3:
                    self.squares[x][y].die()
        return alive

    def gen_random_seed(self):
        distance = random.randint(0, 5)
        for square_row in self.squares:
            for square in square_row:
                if distance == 0:
                    distance = random.randint(1, 6)
                    square.born()
                distance -= 1

    def find_neighbors(self, index):
        neighbors = []
        right = index[0] + 1
        left = index[0] - 1
        up = index[1] + 1
        down = index[1] - 1
        if self.is_valid_index((index[0], up)): neighbors.append((index[0], up))
        if self.is_valid_index((right, up)): neighbors.append((right, up))
        if self.is_valid_index((left, up)): neighbors.append((left, up))
        if self.is_valid_index((index[0], down)): neighbors.append((index[0], down))
        if self.is_valid_index((right, down)): neighbors.append((right, down))
        if self.is_valid_index((left, down)): neighbors.append((left, down))
        if self.is_valid_index((right, index[1])): neighbors.append((right, index[1]))
        if self.is_valid_index((left, index[1])): neighbors.append((left, index[1]))
        return neighbors

    def get_num_living(self, squares, neighbors):
        num_living = 0
        for n in neighbors:
            if(self.squares[n[0]][n[1]].color != (0,0,0)):
                num_living = num_living + 1
        return num_living

    def reset(self, playerToken):
        for x in range(self.rows):
            for y in range(self.cols):
                self.squares[x][y].die()
        playerToken.reset_position()

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

class Engine():
    def __init__(self):
        self.delta = 0
        self.FRAMERATE = 60
        self.frameMili = 1000//self.FRAMERATE

        self.screen = pygame.display.set_mode((720, 720))
        self.screen.fill((255, 255, 255))

        self.gameOn = True

        self.board = Board()
        self.token = Player()

        self.numAlive = 0
        self.is_generating_maze = False

    def start_game(self):
        # Process inputs
        while self.gameOn:
            elapsed = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        self.gameOn = False
                    if event.key == K_g:
                        is_generating_maze = True
                    if event.key == K_r:
                        self.board.squares.gen_random_seed(self.board, self.board.rows, self.board.cols)
                    if event.key == K_UP or event.key == K_w:
                        self.token.update(self.board.squares, self.board.rows, self.board.cols, 0, -36)
                    if event.key == K_DOWN or event.key == K_s:
                        self.token.update(self.board.squares, self.board.rows, self.board.cols, 0, 36)
                    if event.key == K_RIGHT or event.key == K_d:
                        self.token.update(self.board.squares, self.board.rows, self.board.cols, 36, 0)
                    if event.key == K_LEFT or event.key == K_a:
                        self.token.update(self.board.squares, self.board.rows, self.board.cols, -36, 0)
                if event.type == MOUSEBUTTONUP:
                    x = pygame.mouse.get_pos()[0] // 36
                    y = pygame.mouse.get_pos()[1] // 36
                    if x < 20 and y < 20:
                        self.board.squares[x][y].update()
                elif event.type == QUIT:
                    self.gameOn = False

            if is_generating_maze:
                newAlive = self.board.generate_maze()
                if newAlive == numAlive:
                    is_generating_maze = False
                numAlive = newAlive
                self.board.squares[0][0].die()
                self.token.reset_position()

            for i in range(self.board.rows):
                for j in range(self.board.cols):
                    if self.board.squares[i][j].dirty == 1:
                        self.screen.blit(self.board.squares[i][j].surf, (i * 36, j * 36))
            self.screen.blit(self.token.surf, (self.token.x, self.token.y))

            pygame.display.flip()

            self.delta = pygame.time.get_ticks() - elapsed
            difference = self.frameMili - self.delta
            pygame.time.delay(difference)


# Checks to see if a given index is valid on the board
# Parameters:
# tuple index, which represents the x,y coordinates for the desired index.
def is_valid_index(index):
    return index[0] > -1 and index[0] < 20 and index[1] > -1 and index[1] < 20 


pygame.init()

game = Engine()
game.start_game()
