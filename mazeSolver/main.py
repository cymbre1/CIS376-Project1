import pygame
import random

from pygame.locals import *


# Kit Bazner Cymbre Spoehr

class Board(pygame.sprite.DirtySprite):
    rows = 20
    cols = 20

    # Constructor for board
    def __init__(self):
        self.squares = [[Square() for j in range(self.cols)] for i in range(self.rows)]
        self.numAlive = 0
        self.counter = 0

    # This function loops through and generates a maze based on the algorithm given in the assignment
    # returns int: how many living cells are in the board
    def generate_maze(self):
        alive = 0
        for x in range(self.rows):
            for y in range(self.cols):
                if not self.squares[x][y].is_dead():
                    alive += 1
                num_living = self.get_num_living(self.find_neighbors((x, y)))
                if num_living == 3:
                    self.squares[x][y].born()
                if num_living < 1 or num_living > 3:
                    self.squares[x][y].die()
        return alive

    # This function is used to update the board, it will let the game know if it is stable.
    # Parameters:
    # Player token is the player token.
    # Returns bool whether the game is ready to play
    def update(self, token, counter):
        newAlive = self.generate_maze()
        if newAlive == self.numAlive or counter > 20:
            return False
        self.numAlive = newAlive
        self.squares[0][0].die()
        self.squares[self.rows - 1][self.cols - 1].die()
        token.reset_position()
        return True

    # This function creates a random seed
    def gen_random_seed(self):
        distance = random.randint(0, 10)
        for square_row in self.squares:
            for square in square_row:
                if distance == 0:
                    distance = random.randint(1, 6)
                    square.born()
                distance -= 1

    # This function finds all of the neighbors of a cell given the index of that cell.
    # Params: 
    # Tuple index which represents the x,y coordinate of the cell
    # Returns Square[] which contains all neighbors of the cell
    def find_neighbors(self, index):
        neighbors = []
        right = index[0] + 1
        left = index[0] - 1
        up = index[1] + 1
        down = index[1] - 1
        if Square().is_valid_index((index[0], up)): neighbors.append((index[0], up))
        if Square().is_valid_index((right, up)): neighbors.append((right, up))
        if Square().is_valid_index((left, up)): neighbors.append((left, up))
        if Square().is_valid_index((index[0], down)): neighbors.append((index[0], down))
        if Square().is_valid_index((right, down)): neighbors.append((right, down))
        if Square().is_valid_index((left, down)): neighbors.append((left, down))
        if Square().is_valid_index((right, index[1])): neighbors.append((right, index[1]))
        if Square().is_valid_index((left, index[1])): neighbors.append((left, index[1]))
        return neighbors

    # This function gets the number of living cells given an array of squares
    # Params:
    # Squares[] neighbors containing the neighbors of a given cell
    # returns int representing how many of the cells were alive.
    def get_num_living(self, neighbors):
        num_living = 0
        for n in neighbors:
            if not self.squares[n[0]][n[1]].is_dead():
                num_living = num_living + 1
        return num_living

    # Resets the board to all cells being black and the player in the top left corner.
    # Parameters:
    # Player playerToken, which represents the player being moved to the corner
    def reset(self, playerToken):
        for x in range(self.rows):
            for y in range(self.cols):
                self.squares[x][y].die()
        playerToken.reset_position()


class Square(pygame.sprite.DirtySprite):
    color = ()
    dead = (0, 0, 0)

    # Sets the initial state of the Square class
    def __init__(self):
        super(Square, self).__init__()
        self.surf = pygame.Surface((35, 35))
        self.die()

    # This function sets the color of the square to be some random color.
    def born(self):
        self.color = (random.randint(0, 255), 200, 255)
        self.surf.fill(self.color)
        self.dirty = 1

    # This function sets the color of the square to be black
    def die(self):
        self.color = self.dead
        self.surf.fill(self.color)
        self.dirty = 1

    # This function switches whether the square is black or colored
    def update(self):
        if self.is_dead():
            self.born()
        else:
            self.die()

    # Checks to see if a given index is valid on the board
    # Parameters:
    # tuple index, which represents the x,y coordinates for the desired index.
    @staticmethod
    def is_valid_index(index):
        return -1 < index[0] < 20 and -1 < index[1] < 20

        # Checks to see if the square is dead

    # Returns bool of whether the cell is dead
    def is_dead(self):
        return self.color == self.dead


class Player(pygame.sprite.DirtySprite):
    # This sets the initial values for the player
    def __init__(self):
        super(Player, self).__init__()

        self.surf = pygame.Surface((35, 35))

        self.color = ((255, 255, 255))

        self.x = 0
        self.y = 0

        self.clicks = 0

        self.dirty = 2

        self.body = pygame.draw.circle(self.surf, self.color, (18, 18), 15)

    # This function return whether the desired position is a valid place that a player token can move
    # Params: 
    # Board board, which represents the board
    # int row, which represents the row the player token would like to move to
    # int column, which represents the  column the player token would like to move to
    # Returns: boolean, whether or not that is a valid move
    def can_move(self, board, row, col):
        return Square().is_valid_index((row, col)) and board.squares[row][col].is_dead()

    # This function is a helper function to move the player token back to start
    def reset_position(self):
        self.x = 0
        self.y = 0
        self.clicks = 0

    # This function facilitates player token movement
    # Params:
    # Board board, which represents the board
    # int xMove, which represents the row the player token would like to move to
    # int yMove, which represents the  column the player token would like to move to
    def update(self, board, xMove, yMove):
        if xMove == 0 == yMove:
            self.clicks += 1
        self.x += xMove
        self.y += yMove
        if not self.can_move(board, self.x // 36, self.y // 36):
            self.x -= xMove
            self.y -= yMove
            return
        if self.x // 36 == 19 == self.y // 36:
            print("You won with " + str(self.clicks) + " clicks.")
            board.reset(self)


class Engine():

    # Sets the initial state of the engine with a specified framerate.
    # Parameters:
    # int rate, specifies the framerate of the engine.  This defaults to 60
    def __init__(self, rate=60):
        self.delta = 0
        self.framerate = rate
        self.frameMili = 1000 // self.framerate

        self.screen = pygame.display.set_mode((720, 720))
        self.screen.fill((255, 255, 255))

        self.gameOn = True

        self.board = Board()
        self.token = Player()

        self.numAlive = 0
        self.is_generating_maze = False
        self.mazeCounter = 0

    # This is the main game loop.  It processes inputs, then updates elements and the main screen.
    def start_game(self):
        # Process inputs
        while self.gameOn:
            elapsed = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        self.gameOn = False
                    if event.key == K_g:
                        self.is_generating_maze = True
                    if event.key == K_r:
                        self.board.gen_random_seed()
                    if event.key == K_UP or event.key == K_w:
                        self.token.update(self.board, 0, -36)
                    if event.key == K_DOWN or event.key == K_s:
                        self.token.update(self.board, 0, 36)
                    if event.key == K_RIGHT or event.key == K_d:
                        self.token.update(self.board, 36, 0)
                    if event.key == K_LEFT or event.key == K_a:
                        self.token.update(self.board, -36, 0)
                if event.type == MOUSEBUTTONUP:
                    x = pygame.mouse.get_pos()[0] // 36
                    y = pygame.mouse.get_pos()[1] // 36
                    if x < 20 and y < 20:
                        self.board.squares[x][y].update()
                        self.token.update(self.board, 0, 0)
                elif event.type == QUIT:
                    self.gameOn = False

            if self.is_generating_maze:
                self.is_generating_maze = self.board.update(self.token, self.mazeCounter)
                self.mazeCounter += 1
            else:
                self.mazeCounter = 0

            for i in range(self.board.rows):
                for j in range(self.board.cols):
                    if self.board.squares[i][j].dirty == 1:
                        self.screen.blit(self.board.squares[i][j].surf, (i * 36, j * 36))
            self.screen.blit(self.token.surf, (self.token.x, self.token.y))

            pygame.display.flip()

            self.delta = pygame.time.get_ticks() - elapsed
            difference = self.frameMili - self.delta
            pygame.time.delay(difference)


pygame.init()

game = Engine(15)
game.start_game()
