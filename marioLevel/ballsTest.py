#!/usr/bin/env python
# Make sure the local python is anaconda and that the pybox2d environment is activated
import sys
 
 
sys.path.append("../")
 
 
import egs
import pygame as pg
from Box2D import *
import random
 
 
w2b = 1/100
b2w = 100
gravity = b2Vec2(0.5, -10.0)
world = b2World(gravity,doSleep=False)
 
 
timeStep = 1.0 / 60
vel_iters, pos_iters = 6, 2
 
 
class Ground(egs.Game_objects.drawable):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.body = world.CreateStaticBody(position=(x, y), shapes=b2PolygonShape(box=(w, h)))
        self.image = pg.Surface((2*w*b2w, 2*h*b2w))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2w, 768 - self.body.position.y * b2w
 
 
class Ball(egs.Game_objects.drawupdateable):
    def __init__(self):
        super().__init__()
        self.body = world.CreateDynamicBody(position=(5, 5))
        shape=b2CircleShape(radius=.25)
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=.5, density=.5)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        d=.25*b2w*2
        self.image = pg.Surface((d,d), pg.SRCALPHA, 32)
        self.image.convert_alpha()
        #self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        pg.draw.circle(self.image,(0, 101, 164) , self.rect.center, .25*b2w)
 
 
    def update(self):
        self.rect.center = self.body.position[0] * b2w, 770 - self.body.position[1] * b2w
        collided = pg.sprite.spritecollide(self, groundGroup, False)
        for event in egs.Engine.events:
            #if event.type == pg.MOUSEMOTION:
            #    print(pg.mouse.get_pos())
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if len(collided) > 0:
                        self.body.ApplyLinearImpulse( b2Vec2(0,1), self.body.position, True)
                elif event.key == pg.K_a:
                    self.body.ApplyLinearImpulse( b2Vec2(-0.5, 0), self.body.position, True)
                elif event.key == pg.K_d:
                    self.body.ApplyLinearImpulse( b2Vec2(.5, 0), self.body.position, True)
        
class Updater(egs.Game_objects.updateable):
    def __init__(self):
        super().__init__()
    def update(self):
        world.Step(timeStep, vel_iters, pos_iters)
        world.ClearForces()
 
 
engine = egs.Engine("Ball Physics")
scene = egs.Scene("Scene One")
egs.Engine.current_scene = scene
engine.mode = 0
ground = Ground(0,1,25,.5)
platform = Ground(2,2,1,.25)
platform2 = Ground(6,4,1, .25)
groundGroup = pg.sprite.Group()
groundGroup.add(ground)
groundGroup.add(platform)
groundGroup.add(platform2)
ball = Ball()
scene.drawables.add(platform)
scene.drawables.add(platform2)
scene.drawables.add(ball)
scene.drawables.add(ground)
scene.updateables.append(ball)
scene.updateables.append(Updater())
scene.fill_color = (255,255,255)
engine.start_game()