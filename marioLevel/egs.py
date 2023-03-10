import pygame
from pygame.locals import *
class Engine:
    #initializer, run, end, current scene, mode??, toggle statistics
    events = []
    def __init__(self, identifier, rate=60):
        self.name = identifier
        self.delta = 0
        self.framerate = rate
        self.frameMili = 1000 // self.framerate

        pygame.init()

        self.screen = Scene("Temp")
        self.screen.fill_color(255, 255, 255)

        pygame.key.set_repeat(500)

        self.gameOn = True
    
    def start_game(self):
        # Process inputs
        while self.gameOn:
            elapsed = pygame.time.get_ticks()

            self.events = pygame.event.get()
            for event in self.events:
                if event.type == QUIT:
                    self.endGame()

            self.screen.update()

            self.delta = pygame.time.get_ticks() - elapsed
            difference = self.frameMili - self.delta
            pygame.time.delay(difference)
        pygame.quit()
    
    def endGame(self):
        self.gameOn = False

class Game_objects:
    #initializer, drawable, updateable, both
    def __init__(self):
        print("initialized")

    class updateable(pygame.sprite.DirtySprite):
        def __init__(self):
            super().__init__()
    
    class drawable(pygame.sprite.DirtySprite):
        def __init__(self):
            super().__init__()
    
    class drawupdateable(pygame.sprite.DirtySprite):
        def __init__(self):
            super().__init__()

class Scene:
    #initializer, name, 
    def __init__(self, identifier):
        self.name = identifier
        self.drawables = []
        self.updateables = []
        self.screen = pygame.display.set_mode((1024,768))
        self.screen.fill((255, 255, 255))
    
    def update(self):
        for item in self.updateables:
            item.update()
        for item in self.drawables:
            self.screen.blit(item.surf, item.body.position)
        pygame.display.flip()
    
    def fill_color(self, red, green, blue):
        self.screen.fill((red, green, blue))

    def add(self, showed):
        self.screen.blit(showed.surf, showed.body.position)