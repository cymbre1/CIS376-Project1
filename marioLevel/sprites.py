import pygame

class Square(pygame.sprite.DirtySprite):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super(Square, self).__init__()
        self.surf = pygame.Surface((35, 35))
        self.die()

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")