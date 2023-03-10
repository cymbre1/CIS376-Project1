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

        self.mode = 0

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
        self.background = None
        self.paused = False
    
    def start_game(self):
        # Process inputs
        while self.gameOn:
            elapsed = pygame.time.get_ticks()

            if self.mode == 0:
                self.background = pygame.Surface([self.width, self.height])
                self.background.fill(Engine.current_scene.fill_Color)
                self.screen.fill(Engine.current_scene.fill_Color)
                Engine.current_scene.drawables.clear(self.screen, self.background)

            Engine.events = pygame.event.get()
            for event in self.events:
                if event.type == QUIT:
                    self.endGame()
        

            self.current_scene.update()

            if self.mode == 1:
                self.screen.fill(Engine.current_scene.fill_Color)

            if self.mode ==1:
                Engine.current_scene.drawables.draw(self.screen)
            else:
                rects = Engine.current_scene.drawables.draw(self.screen)

            if self.mode == 1:
                pygame.display.flip()
            else:
                pygame.display.update(rects)

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
        self.title = identifier
        self.drawables = pygame.sprite.LayeredDirty()
        self.updateables = []
    
    def update(self):
        for item in self.updateables:
            item.update()