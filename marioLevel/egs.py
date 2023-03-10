import pygame
from pygame.locals import *
class Engine:
    #initializer, run, end, current scene, mode??, toggle statistics
    events = []
    current_scene = None
    def __init__(self, identifier, rate=60, width=1024, height=768):
        self.width = width
        self.height = height
        self.title = identifier
        self.delta = 0
        self.framerate = rate
        self.frameMili = 1000 // self.framerate

        self.gameOn = True

        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.last_checked_time = pygame.time.get_ticks()
        pygame.joystick.init()

        for i in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()

        pygame.key.set_repeat(500)
        self.statistics_font = pygame.font.Font(None,30)
        self.paused = False
        self.background = None
        self.paused = False
    
    def start_game(self):
        # Process inputs
        while self.gameOn:
            elapsed = pygame.time.get_ticks()


            self.events = pygame.event.get()
            for event in self.events:
                if event.type == QUIT:
                    self.endGame()

            self.current_scene.update()
            self.screen.fill((255,255,255))
            self.current_scene.draw(self.screen)

            pygame.display.flip()

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
    fill_Color = (255,255,255)
    #initializer, name, 
    def __init__(self, identifier):
        self.name = identifier
        self.drawables = []
        self.updateables = []
    
    def update(self):
        for item in self.updateables:
            item.update()

    def draw(self, screen):
        for item in self.drawables:
            screen.blit(item.surf, item.rect.center)
    
    def add(self, showed):
        self.drawables.append(showed)