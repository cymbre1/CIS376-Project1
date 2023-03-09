import pygame

import egs
from Box2D import *

class SuperMario(egs.Game_objects.drawupdateable):
    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((35,70))
        self.surf.fill((255,0,0))
        self.body = world.CreateDynamicBody(position=(100,100))
        self.shape = b2PolygonShape(box=((.35, .7)))
        fixDef = b2FixtureDef(shape=self.shape, friction=.3, restitution=.5, density=.5)
        self.box = self.body.CreateFixture(fixDef)
        self.dirty = 2      
        self.rect = self.surf.get_rect()  

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class Mario(pygame.sprite.DirtySprite):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class Goomba(egs.Game_objects.drawupdateable):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class Koopa(egs.Game_objects.drawupdateable):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super(self).__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class KoopaShell(egs.Game_objects.drawupdateable):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class Ground(egs.Game_objects.drawable):
    # color = (255,0,0)
    x = 0
    y = 690

    # Sets the initial state of the Square class
    def __init__(self, width, height):
        super().__init__()
        color = (255,0,0)
        self.surf = pygame.Surface((width,height))
        self.surf.fill(color)

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class Brick(egs.Game_objects.drawable):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class SolidStone(egs.Game_objects.drawable):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class QuestionBlock(egs.Game_objects.drawable):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class Platform(egs.Game_objects.drawable):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")


class Platform(egs.Game_objects.drawupdateable):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class Pipe(egs.Game_objects.drawable):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class Updater():
    def __init__(self):
        super.__init__()

    def update(self):
        world.Step(timeStep, vec_iters, pos_iters)
        world.ClearForces()

gravity = b2Vec2(0.5, -10)
world = b2World(gravity)
timeStep = 1.0/60
vec_iters, pos_iters = 6,2
w2b = 1/100
b2w = 100


