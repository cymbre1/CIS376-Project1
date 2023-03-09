import pygame

class SuperMario(pygame.sprite.DirtySprite):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super(SuperMario, self).__init__()
        self.surf = pygame.Surface((70, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class Mario(pygame.sprite.DirtySprite):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super(SuperMario, self).__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")