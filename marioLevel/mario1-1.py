#!/usr/bin/env python
import pygame

import sys
from Box2D import *
import egs

gravity = b2Vec2(.5, -10.0)
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
        self.body = world.CreateStaticBody(position=(x, y), shapes=b2PolygonShape(box=(w, h)))
        self.image = pygame.Surface((2*w*b2w, 2*h*b2w))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2w, 768 - self.body.position.y * b2w

        # self.body = world.CreateStaticBody(position=(x, y), shapes=b2PolygonShape(box=(w, h)))
        # self.image = pygame.Surface((2*w*b2w, 2*h*b2w))
        # self.image.fill((0, 255, 0))
        # self.rect = self.image.get_rect()
        # self.rect.center = self.body.position.x * b2w, 768  - ((self.body.position.y * b2w) / 2)

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

    def __init__(self):
        super().__init__()

        self.body = world.CreateDynamicBody(position=(5,5))
        shape=b2PolygonShape(box=(.25, .25))
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=.5, density=.5)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        d=.25*b2w*2
        self.image = pygame.Surface((d,d), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        #self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image,(0, 101, 164) , self.rect)
        # self.body = world.CreateDynamicBody(position=pos)
        # half_width = 0.25
        # half_height = 0.35
        # vertices = [
        #     Box2D.b2Vec2(-half_width, -half_height),
        #     Box2D.b2Vec2(half_width, -half_height),
        #     Box2D.b2Vec2(half_width, half_height),
        #     Box2D.b2Vec2(-half_width, half_height)
        # ]
        # shape = b2PolygonShape(vertices=vertices)
        # fixDef = b2FixtureDef(shape=shape, friction=.3, restitution=.07, density=.5)
        # box = self.body.CreateFixture(fixDef)
        # self.dirty = 2 
        # self.image = pygame.Surface((.5*b2w*2, .7*b2w*2))
        # self.image.fill((255,0,0))     
        # self.rect = self.image.get_rect()
        # pygame.draw.rect(self.image, (255,0,0), self.rect)

    def update(self):
        #self.rect.center = (self.body.position[0] *b2w, 768 -(( self.body.position[1]*b2w) / 2))
        self.rect.center = self.body.position[0] * b2w, 770 - self.body.position[1] * b2w
        collided = pygame.sprite.spritecollide(self, groundGroup, False)
        for event in egs.Engine.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.body.ApplyForce(b2Vec2(-10, 0), self.body.position, True)
                if event.key == pygame.K_d:
                    self.body.ApplyForce(b2Vec2(10,0), self.body.position, True)
                if event.key == pygame.K_w:
                    if collided:
                        self.body.ApplyLinearImpulse(b2Vec2(0,1), self.body.position, True)

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



engine = egs.Engine("Mario 1-1")

scene = egs.Scene("Scene 1")
egs.Engine.current_scene = scene

#engine.mode = 1

ground = Ground(0,1,25, .5)
mario = SuperMario()

groundGroup = pygame.sprite.Group()
groundGroup.add(ground)

scene.drawables.add(ground)
scene.drawables.add(mario)

scene.updateables.append(Updater())
scene.updateables.append(mario)

engine.start_game()
