#!/usr/bin/env python
import pygame

import sys
from Box2D import *
import egs

gravity = b2Vec2(.5, -10)
world = b2World(gravity, doSleep=False)
timeStep = 1.0/60
vec_iters, pos_iters = 6,2
w2b = 1/100
b2w = 100

class Brick(egs.Game_objects.drawable):
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

class Ground(egs.Game_objects.drawable):

    # Sets the initial state of the Square class
    def __init__(self, x, y, w, h):
        super().__init__()
        color = (0,255,0)
        self.body = world.CreateStaticBody(position = (x,y), shapes=b2PolygonShape(box=(w,h)))
        self.surf = pygame.Surface((2*w*b2w, 2*h*b2w))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.rect.center = self.body.position.x *b2w, (720-self.body.position.y * b2w)

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

class Mario(pygame.sprite.DirtySprite):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class SuperMario(egs.Game_objects.drawupdateable):
    # Sets the initial state of the Square class
    x, y = 100, 100

    def __init__(self):
        super().__init__()
        self.body = world.CreateDynamicBody(position=(100,100))
        self.shape = b2PolygonShape(box=((.35, .7)))
        fixDef = b2FixtureDef(shape=self.shape, friction=.3, restitution=.5, density=.5)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2 
        self.surf = pygame.Surface((70,140))
        self.surf.fill((255,0,0))     
        self.rect = self.surf.get_rect()
        pygame.draw.rect(self.surf, (255,0,0), self.rect)

    def update(self):
        self.rect.center = (self.body.position[0] *b2w, 720 - self.body.position[1]*b2w)
        #collided = pygame.sprite.spritecollide(self, groundGroup, False)
        print("mario")


class QuestionBlock(egs.Game_objects.drawable):
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

class SolidStone(egs.Game_objects.drawable):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class Updater(egs.Game_objects.updateable):
    def __init__(self):
        super().__init__()

    def update(self):
        world.Step(timeStep, vec_iters, pos_iters)
        world.ClearForces()
        print("Update")



engine = egs.Engine("Mario 1-1")

scene = egs.Scene("Scene 1")
engine.screen = scene

ground = Ground(0,650,20, .35)
mario = SuperMario()

groundGroup = pygame.sprite.Group()
groundGroup.add(ground)

scene.add(ground)
scene.add(mario)

scene.updateables.append(Updater())
scene.updateables.append(mario)
engine.start_game()
