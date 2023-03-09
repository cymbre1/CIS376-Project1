import pygame
from pygame.locals import *
class Engine:
    #initializer, run, end, current scene, mode??, toggle statistics
    def __init__(self, identifier, rate=60):
        self.name = identifier
        self.delta = 0
        self.framerate = rate
        self.frameMili = 1000 // self.framerate

        self.screen = pygame.display.set_mode((720, 720))
        self.screen.fill((255, 255, 255))

        self.gameOn = True
    
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
                    self.endGame()

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
    
    def endGame(self):
        self.gameOn = False

class Game_objects:
    #initializer, drawable, updateable, both
    def __init__(self):
        print("initialized")
    class updateable:
        def __init__():
            self.

class Scene:
    #initializer, name, 
    def __init__(self, identifier):
        self.name = identifier
        self.drawables = []
        self.updateables = []
        self.screen = pygame.display.set_mode((720, 720))
        self.screen.fill((255, 255, 255))
    
    def update(self):
        for item in self.updateables:
            item.update()
    
    def fill_color(self, red, green, blue):
        self.screen.fill((red, green, blue))