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
p2b = 1/100
b2p = 100

class Brick(egs.Game_objects.drawable):
    color = (255,0,0)

    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((35, 35))

    # This function switches whether the square is black or colored
    def update(self):
        print("Update and stuff")

class Flag(egs.Game_objects.drawupdateable):
    flag_sprites = []
    index = 0
    counter = 0
    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()

        # self.reached = True
        
        filename = "flag.png"
        piece_ss = SpriteSheet(filename)
        for i in range(10):
            flag_rect = (i*32, 0, 32, 176)
            flag_image = piece_ss.image_at(flag_rect)
            self.flag_sprites.append(flag_image)
        self.body = world.CreateStaticBody(position = (6, 5), shapes = b2PolygonShape(box = (.64, 3.52)))
        self.dirty = 1
        bigger_img = pygame.transform.scale(self.flag_sprites[self.index], (128, 704))
        self.image = bigger_img.convert_alpha()
        self.rect = self.image.get_rect()

    # This function switches whether the square is black or colored
    def update(self):
        # print("update")
        bigger_img = pygame.transform.scale(self.flag_sprites[self.index], (128, 704))
        self.image = bigger_img.convert_alpha()
        self.rect = self.image.get_rect()

        if self.counter == 5:
            self.counter = 0
            if self.index < 9:
                self.index += 1
                self.dirty = 1
            else:
                self.dirty = 0
        else:
            self.counter += 1

        self.rect.center = self.body.position[0] * b2p, 775 - self.body.position[1] * b2p
                    
class Goomba(egs.Game_objects.drawupdateable):
    goomba_sprites = []
    counter = 0
    current_index = 0
    force = -13
    last_center = None
    def __init__(self, pos):
        super().__init__()
        filename = "enemies.png"

        piece_ss = SpriteSheet(filename)
        for i in range (2):
            goomba_rect = (i*16, 0, 16, 16)
            goomba_image = piece_ss.image_at(goomba_rect)
            self.goomba_sprites.append(goomba_image)

        self.body = world.CreateDynamicBody(position= pos)
        shape = b2PolygonShape(box = (.32,.32))
        fixDef = b2FixtureDef(shape=shape, friction = 0.3, restitution=0, density = 1)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        bigger_img = pygame.transform.scale(self.goomba_sprites[self.current_index % 2], (64,64))
        self.image = bigger_img.convert_alpha()
        self.rect = self.image.get_rect()

    # This function switches whether the square is black or colored
    def update(self):
        if self.rect.right > -100:
            if self.counter == 10:
                self.current_index = self.current_index + 1
                self.counter = 0
                bigger_img = pygame.transform.scale(self.goomba_sprites[self.current_index % 2], (64,64))
                self.image = bigger_img.convert_alpha()
                self.rect = self.image.get_rect()

                self.rect.center = self.body.position[0] * b2p, 775 - self.body.position[1] * b2p
                groundCollided = pygame.sprite.spritecollide(self, groundGroup, False)
                if groundCollided:
                    self.body.ApplyForce(b2Vec2(self.force, 0), self.body.position, True)
                if self.rect.center == self.last_center:
                    self.force = 0 - self.force
            else:
                self.last_center = self.rect.center
                self.rect.center = self.body.position[0] * b2p, 775 - self.body.position[1] * b2p
                self.counter = self.counter + 1 
        else:
            self.kill()           

class Ground(egs.Game_objects.drawable):

    # Sets the initial state of the Square class
    def __init__(self, x, y, w, h):
        super().__init__()

        filename = "ground.png"

        piece_ss = SpriteSheet(filename)

        self.dirty = 2

        width_in_pixels = w * b2p
        height_in_pixels = h * b2p
        
        # Pixels may be off due to scaling issues.  Everything is currently multiplied by 4 other places
        ground_rect = (0, 0, width_in_pixels//2, height_in_pixels//2)
        ground_image = piece_ss.image_at(ground_rect)

        self.dirty = 2

        self.body = world.CreateStaticBody(position=(x, y), shapes=b2PolygonShape(box=(w, h)))
        # self.image = pygame.Surface((2*w*b2w, 2*h*b2w))
        # self.image.fill((0, 255, 0))
        bigger_img = pygame.transform.scale(ground_image, (width_in_pixels * 2, height_in_pixels * 2))
        self.image = bigger_img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2p, 768 - self.body.position.y * b2p

class Koopa(egs.Game_objects.drawupdateable):
    flipped = False
    koopa_walking = []
    current_koopa = 0
    counter = 0
    step_counter = 0

    # Sets the initial state of the Square class
    def __init__(self):
        super().__init__()
        
        filename = "enemies.png"
        piece_ss = SpriteSheet(filename)
        
        koopa_rect = (0, 16, 16, 24)
        koopa_image = piece_ss.image_at(koopa_rect)
        self.koopa_walking.append(koopa_image)

        self.body = world.CreateDynamicBody(position=(5,5))
        shape=b2PolygonShape(box=(.16, .16))
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=0, density=.1)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2

        koopa_rect = (16, 16, 16, 24)
        koopa_image = piece_ss.image_at(koopa_rect)
        self.koopa_walking.append(koopa_image)

        bigger_img = pygame.transform.scale(self.koopa_walking[self.current_koopa], (64, 96))
        self.image = bigger_img.convert_alpha()
        self.current_koopa = (self.current_koopa + 1) % 2

        self.rect = self.image.get_rect()

    # This function switches whether the square is black or colored
    def update(self):
        if self.counter == 30:
            bigger_img = pygame.transform.scale(self.koopa_walking[self.current_koopa], (64, 96))
            self.image = bigger_img.convert_alpha()
            self.current_koopa = (self.current_koopa + 1) % 2
            self.counter = 0
            if self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)
                self.body.ApplyForce(b2Vec2(5, 0), self.body.position, True)
                if self.step_counter == 15:
                    self.flipped = False
                    self.step_counter = 0
                else:
                    self.step_counter = self.step_counter + 1
            else:
                self.body.ApplyForce(b2Vec2(-5, 0), self.body.position, True)
                if self.step_counter == 15:
                    self.flipped = True
                    self.step_counter = 0
                else:
                    self.step_counter = self.step_counter + 1
        else:
            self.counter = self.counter + 1

        self.rect = self.image.get_rect()
        collided = pygame.sprite.spritecollide(self, groundGroup, False)

        self.rect.center = self.body.position[0] * b2p, 775 - self.body.position[1] * b2p

# class KoopaShell(egs.Game_objects.drawupdateable):


class Mario(egs.Game_objects.drawupdateable):
     # Sets the initial state of the Square class
    mario_running = []
    flipped = False
    counter = 0
    current_mario = 0
    previous_center = ()
    previous_bottom = ()

    def __init__(self):
        super().__init__()

        filename = "superMarioSprites.png"

        piece_ss = SpriteSheet(filename)
        for i in range(3):
            mario_rect = (i*16, 0, 16, 16)
            mario_image = piece_ss.image_at(mario_rect)
            self.mario_running.append(mario_image)

        mario_rect = (48, 0, 16, 16)
        mario_image = piece_ss.image_at(mario_rect)
        self.mario_running.append(mario_image)

        mario_rect = (0,0,16,16)
        self.mario_still = piece_ss.image_at(mario_rect)

        mario_rect = (64,0,16,16)
        self.mario_jump = piece_ss.image_at(mario_rect)

        self.body = world.CreateDynamicBody(position=(5,5))
        shape=b2PolygonShape(box=(.32, .32))
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=0, density=1)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        bigger_img = pygame.transform.scale(self.mario_running[self.current_mario], (64, 64))
        self.image = bigger_img.convert_alpha()
        if(self.flipped):
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()

    def update(self):
        if not self.previous_bottom == self.rect.bottom:
            bigger_img = pygame.transform.scale(self.mario_jump, (64, 64))
        elif self.previous_center == self.rect.center:
            bigger_img = pygame.transform.scale(self.mario_still, (64, 64))
        else:
            bigger_img = pygame.transform.scale(self.mario_running[self.current_mario], (64, 64))
            if self.counter == 10:
                if self.current_mario == 3:
                    self.current_mario = 0
                else:
                    self.current_mario = self.current_mario + 1
                self.counter = 0
            else:
                self.counter = self.counter + 1
        
        self.previous_center = self.rect.center
        self.previous_bottom = self.rect.bottom

        self.image = bigger_img.convert_alpha()
        self.rect = self.image.get_rect()        

        if(self.flipped):
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect.center = self.body.position[0] * b2p, 775 - self.body.position[1] * b2p
        collided = pygame.sprite.spritecollide(self, groundGroup, False)
        for event in egs.Engine.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.body.ApplyForce(b2Vec2(-75, 0), self.body.position, True)
                    self.flipped = True
                if event.key == pygame.K_d:
                    self.body.ApplyForce(b2Vec2(75,0), self.body.position, True)
                    self.flipped = False
                if event.key == pygame.K_w:
                    if collided:
                        self.body.ApplyLinearImpulse(b2Vec2(0,3), self.body.position, True)

class SuperMario(egs.Game_objects.drawupdateable):
    # Sets the initial state of the Square class
    mario_running = []
    flipped = False
    counter = 0
    current_mario = 0
    previous_center = ()
    previous_bottom = ()

    def __init__(self):
        super().__init__()

        filename = "superMarioSprites.png"

        piece_ss = SpriteSheet(filename)
        for i in range(3):
            mario_rect = (i*16, 0, 16, 32)
            mario_image = piece_ss.image_at(mario_rect)
            self.mario_running.append(mario_image)

        mario_rect = (48, 0, 16, 32)
        mario_image = piece_ss.image_at(mario_rect)
        self.mario_running.append(mario_image)

        mario_rect = (0,0,16,32)
        self.mario_still = piece_ss.image_at(mario_rect)

        mario_rect = (64,0,16,32)
        self.mario_jump = piece_ss.image_at(mario_rect)

        self.body = world.CreateDynamicBody(position=(5,5))
        shape=b2PolygonShape(box=(p2b*32, p2b*64))
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=0, density=.5)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        bigger_img = pygame.transform.scale(self.mario_running[self.current_mario], (64, 134))
        self.image = bigger_img.convert_alpha()
        if(self.flipped):
            pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()

    def update(self):
        if not self.previous_bottom == self.rect.bottom:
            bigger_img = pygame.transform.scale(self.mario_jump, (64, 134))
        elif self.previous_center == self.rect.center:
            bigger_img = pygame.transform.scale(self.mario_still, (64, 134))
        else:
            bigger_img = pygame.transform.scale(self.mario_running[self.current_mario], (64, 134))
            if self.counter == 10:
                if self.current_mario == 3:
                    self.current_mario = 0
                else:
                    self.current_mario = self.current_mario + 1
                self.counter = 0
            else:
                self.counter = self.counter + 1
        
        self.previous_center = self.rect.center
        self.previous_bottom = self.rect.bottom

        self.image = bigger_img.convert_alpha()
        self.rect = self.image.get_rect()        

        if(self.flipped):
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect.center = self.body.position[0] * b2p, 775 - self.body.position[1] * b2p
        collided = pygame.sprite.spritecollide(self, groundGroup, False)
        for event in egs.Engine.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.body.ApplyForce(b2Vec2(-75, 0), self.body.position, True)
                    self.flipped = True
                if event.key == pygame.K_d:
                    self.body.ApplyForce(b2Vec2(75,0), self.body.position, True)
                    self.flipped = False
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


width = 1024
height = 768
engine = egs.Engine("Mario 1-1", width = width, height = height)

scene = egs.Scene("Scene 1")
egs.Engine.current_scene = scene


ground = Ground(0,.64,11.04, .64)
platform = Ground(1,2.5,.64,.64)
mario = Mario()
goomba = Goomba((7,4))
flag = Flag()
koopa = Koopa()

groundGroup = pygame.sprite.Group()
groundGroup.add(ground)
groundGroup.add(platform)

scene.drawables.add(ground)
scene.drawables.add(platform)
scene.drawables.add(mario)
scene.drawables.add(goomba)
scene.drawables.add(koopa)
scene.drawables.add(flag)

scene.updateables.append(Updater())
scene.updateables.append(mario)
scene.updateables.append(goomba)
scene.updateables.append(koopa)
scene.updateables.append(flag)

engine.start_game()
