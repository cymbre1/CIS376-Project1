#!/usr/bin/env python
import pygame

import sys
from Box2D import *
import egs
from spriteSheet import SpriteSheet

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

class Mario(pygame.sprite.DirtySprite):

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
        filename = "enemies.png"

        piece_ss = SpriteSheet(filename)
        for i in range (2):
            goomba_rect = ()

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class Ground(egs.Game_objects.drawable):

    # Sets the initial state of the Square class
    def __init__(self, x, y, w, h):
        super().__init__()

        filename = "ground.png"

        piece_ss = SpriteSheet(filename)

        # ground_rect = (0, 208, 3376, 32)
        # ground_image = piece_ss.image_at(ground_rect)


        self.body = world.CreateStaticBody(position=(x, y), shapes=b2PolygonShape(box=(w, h)))
        self.image = pygame.Surface((2*w*b2w, 2*h*b2w))
        self.image.fill((0, 255, 0))
        # bigger_img = pygame.transform.scale(ground_image, (3376*2, 64))
        # self.image = bigger_img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2w, 768 - self.body.position.y * b2w

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
    mario_sprites = []
    mario_version = 1

    def __init__(self):
        super().__init__()

        filename = "superMarioSprites.png"

        piece_ss = SpriteSheet(filename)
        for i in range(4):
            mario_rect = (i*38, 32, 16, 32)
            mario_image = piece_ss.image_at(mario_rect)
            self.mario_sprites.append(mario_image)

        self.body = world.CreateDynamicBody(position=(5,5))
        shape=b2PolygonShape(box=(.32, .64))
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=.5, density=.5)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        bigger_img = pygame.transform.scale(self.mario_sprites[self.mario_version // 10], (64, 128))
        self.image = bigger_img.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        bigger_img = pygame.transform.scale(self.mario_sprites[self.mario_version // 10], (64, 128))
        self.image = bigger_img.convert_alpha()
        self.rect = self.image.get_rect()
        if self.mario_version / 10 > 3:
            self.mario_version = 1
        else:
                self.mario_version = self.mario_version + 1

        # self.mario_version = 1 if self.mario_version == 4 else self.mario_version + 1

        self.rect.center = self.body.position[0] * b2w, 775 - self.body.position[1] * b2w
        collided = pygame.sprite.spritecollide(self, groundGroup, False)
        for event in egs.Engine.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.body.ApplyForce(b2Vec2(-75, 0), self.body.position, True)
                if event.key == pygame.K_d:
                    self.body.ApplyForce(b2Vec2(75,0), self.body.position, True)
                if event.key == pygame.K_w:
                    if collided:
                        self.body.ApplyLinearImpulse(b2Vec2(0,3), self.body.position, True)

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


ground = Ground(0,0.5,25, .5)
platform = Ground(.0,3,.5,.5)
mario = SuperMario()

groundGroup = pygame.sprite.Group()
groundGroup.add(ground)
groundGroup.add(platform)

scene.drawables.add(ground)
scene.drawables.add(platform)
scene.drawables.add(mario)

scene.updateables.append(Updater())
scene.updateables.append(mario)

engine.start_game()
