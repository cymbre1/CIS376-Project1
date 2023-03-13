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

class Background(egs.Game_objects.drawable):
    def __init__(self):
        super().__init__()

        filename = "image\\background.png"

        self.dirty = 2
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        

# class Brick(egs.Game_objects.drawable):
    # # Sets the initial state of the Square class
    # def __init__(self, pos):
    #     super().__init__()

    #     filename = "ground.png"

    #     piece_ss = SpriteSheet(filename)

    #     brick_rect = (0, 0, 64, 64)
    #     ground_image = piece_ss.image_at(brick_rect)

    # # This function switches whether the square is black or colored
    # def update(self):
    #     print("Update and stuff")

class Flag(egs.Game_objects.drawupdateable):
    flag_sprites = []
    index = 0
    counter = 0
    # Sets the initial state of the Square class
    def __init__(self, pos):
        super().__init__()

        # self.reached = True
        
        filename = "image\\flag.png"
        piece_ss = SpriteSheet(filename)
        for i in range(9):
            flag_rect = (i*128, 0, 128, 705)
            flag_image = piece_ss.image_at(flag_rect)
            self.flag_sprites.append(flag_image)
        self.body = world.CreateStaticBody(position = pos, shapes = b2PolygonShape(box = (p2b* 64, p2b*352)))
        self.dirty = 2
        self.image = self.flag_sprites[self.index].convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.image = self.flag_sprites[self.index].convert_alpha()
        self.rect = self.image.get_rect()

        if self.counter == 5:
            self.counter = 0
            if self.index < 8:
                self.index += 1       
        else:
            self.counter += 1

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p
                    
class Goomba(egs.Game_objects.drawupdateable):
    goomba_sprites = []
    counter = 0
    current_index = 0
    force = -13
    last_center = None
    dead = False

    def __init__(self, pos):
        super().__init__()
        filename = "image\\enemies.png"

        piece_ss = SpriteSheet(filename)
        for i in range (2):
            goomba_rect = (i*64, 0, 64, 64)
            goomba_image = piece_ss.image_at(goomba_rect)
            self.goomba_sprites.append(goomba_image)

        goomba_rect = (128, 0, 64, 64)
        self.goomba_dying = piece_ss.image_at(goomba_rect)

        self.body = world.CreateDynamicBody(position= pos, )
        shape = b2PolygonShape(box = (p2b* 32,p2b*32))
        fixDef = b2FixtureDef(shape=shape, friction = 0.3, restitution=0, density = 1)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        self.image = self.goomba_sprites[self.current_index % 2].convert_alpha()
        self.rect = self.image.get_rect()

    # This function switches whether the square is black or colored
    def update(self):
        if self.dead and self.counter < 30:
            bigger_img = pygame.transform.scale(self.goomba_dying, (64, 64))
            self.image = bigger_img.convert_alpha()
            self.rect = self.image.get_rect()
            self.counter += 1
            self.rect.center = self.body.position[0] * b2p, 775 - self.body.position[1] * b2p
            enemiesGroup.remove(self)
            return
        if self.dead and self.counter == 30:
            self.kill()
            return
        
        if self.dead:
            return

        if self.rect.right > -100:
            if self.counter == 10:
                self.current_index = self.current_index + 1
                self.counter = 0
                self.image = self.goomba_sprites[self.current_index % 2].convert_alpha()
                self.rect = self.image.get_rect()

                self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p
                groundCollided = pygame.sprite.spritecollide(self, groundGroup, False)
                if groundCollided:
                    self.body.ApplyForce(b2Vec2(self.force, 0), self.body.position, True)

                collidedWithEnemy = pygame.sprite.spritecollide(self, marioGroup, False)
                if(collidedWithEnemy):
                    for e in enemiesGroup:
                        if self.collided_with_top(e.rect):
                            self.dead = True
                            self.counter = 0
                            return

            else:
                self.last_center = self.rect.center
                self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p
                self.counter = self.counter + 1 
        else:
            self.kill()          

    def collided_with_top(self, rect):
        return rect.collidepoint(self.rect.topleft) or rect.collidepoint(self.rect.topright) or rect.collidepoint(self.rect.midtop)

class Ground(egs.Game_objects.drawable):

    # Sets the initial state of the Square class
    def __init__(self, x, y, w, h):
        super().__init__()

        filename = "image\\ground.png"

        piece_ss = SpriteSheet(filename)

        self.dirty = 2

        width_in_pixels = w * b2p * 2
        height_in_pixels = h * b2p * 2
        
        # Pixels may be off due to scaling issues.  Everything is currently multiplied by 4 other places
        ground_rect = (0, 0, width_in_pixels, height_in_pixels)
        ground_image = piece_ss.image_at(ground_rect)

        self.dirty = 2

        self.body = world.CreateStaticBody(position=(x, y), shapes=b2PolygonShape(box=(w, h)))
        # self.image = pygame.Surface((2*w*b2w, 2*h*b2w))
        # self.image.fill((0, 255, 0))
        self.image = ground_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2p, height - self.body.position.y * b2p

class Koopa(egs.Game_objects.drawupdateable):
    flipped = False
    koopa_walking = []
    current_koopa = 0
    counter = 0
    step_counter = 0
    dead = False

    # Sets the initial state of the Square class
    def __init__(self, pos):
        super().__init__()
        
        filename = "image\\enemies.png"
        piece_ss = SpriteSheet(filename)
        
        koopa_rect = (0, 64, 64, 96)
        koopa_image = piece_ss.image_at(koopa_rect)
        self.koopa_walking.append(koopa_image)

        self.body = world.CreateDynamicBody(position=pos, fixedRotation = True)
        shape=b2PolygonShape(box=(p2b*16, p2b*16))
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=0, density=1)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2

        koopa_rect = (64, 64, 64, 96)
        koopa_image = piece_ss.image_at(koopa_rect)
        self.koopa_walking.append(koopa_image)

        self.image = self.koopa_walking[self.current_koopa].convert_alpha()
        self.current_koopa = (self.current_koopa + 1) % 2

        self.rect = self.image.get_rect()

    # This function switches whether the square is black or colored
    def update(self):
        if self.dead:
            return

        if self.counter == 30:
            self.image = self.koopa_walking[self.current_koopa].convert_alpha()
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
        # collided = pygame.sprite.spritecollide(self, groundGroup, False)

        collidedWithEnemy = pygame.sprite.spritecollide(self, marioGroup, False)
        if(collidedWithEnemy):
            for e in enemiesGroup:
                if self.collided_with_top(e.rect):
                    self.dead = True
                    self.kill()
                    return

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    def collided_with_top(self, rect):
        return rect.collidepoint(self.rect.topleft) or rect.collidepoint(self.rect.topright) or rect.collidepoint(self.rect.midtop)

class KoopaShell(egs.Game_objects.drawupdateable):
    counter = 0
    dead = False

    # Sets the initial state of the Square class
    def __init__(self, pos):
        super().__init__()
        
        filename = "image\\enemies.png"
        piece_ss = SpriteSheet(filename)
        
        koopa_rect = (128, 96, 64, 64)
        self.koopa_shell = piece_ss.image_at(koopa_rect)

        koopa_rect = (192, 96, 64, 64)
        self.koopa_shell_legs = piece_ss.image_at(koopa_rect)

        self.body = world.CreateDynamicBody(position=pos, fixedRotation = True)
        shape=b2PolygonShape(box=(p2b*16, p2b*16))
        fixDef = b2FixtureDef(shape=shape, friction=0.05, restitution=0, density=1)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2

        self.image = self.koopa_shell.convert_alpha()
        self.rect = self.image.get_rect()

    # This function switches whether the square is black or colored
    def update(self):
        if self.dead:
            return

        if self.counter == 560:
            koopa = Koopa(self.body.position)
            enemiesGroup.add(koopa)
            scene.drawables.add(koopa)
            scene.updateables.append(koopa)
            self.dead = True
            self.kill()
            return
        
        if self.counter == 360:
            self.image = self.koopa_shell_legs.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p   

            collidedWithEnemy = pygame.sprite.spritecollide(self, marioGroup, False)
            if(collidedWithEnemy):
                for e in enemiesGroup:
                    if e.rect.collidepoint(self.rect.topright):
                        self.body.ApplyForce(b2Vec2(10, 0), self.body.position, True)
                        self.counter = 0
                    elif e.rect.collidepoint(self.rect.topleft):
                        self.body.ApplyForce(b2Vec2(-10, 0), self.body.position, True)
                        self.counter = 0
                        
        self.counter += 1
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

class Mario(egs.Game_objects.drawupdateable):
     # Sets the initial state of the Square class
    mario_running = []
    flipped = False
    counter = 0
    current_mario = 0
    previous_center = ()
    previous_bottom = ()
    dead = False

    def __init__(self, pos):
        super().__init__()

        filename = "image\\marioSprites.png"

        piece_ss = SpriteSheet(filename)
        for i in range(3):
            mario_rect = (i*68, 0, 68, 70)
            mario_image = piece_ss.image_at(mario_rect)
            self.mario_running.append(mario_image)

        mario_rect = (204, 0, 68, 70)
        mario_image = piece_ss.image_at(mario_rect)
        self.mario_running.append(mario_image)

        mario_rect = (0, 0, 68, 70)
        self.mario_still = piece_ss.image_at(mario_rect)

        mario_rect = (272, 0, 68, 70)
        self.mario_jump = piece_ss.image_at(mario_rect)

        mario_rect = (340, 0, 68, 70)
        self.mario_dying = piece_ss.image_at(mario_rect)


        self.body = world.CreateDynamicBody(position=pos)
        shape=b2PolygonShape(box=(p2b*32, p2b*32))
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=0, density=1)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        self.image = self.mario_running[self.current_mario].convert_alpha()
        if(self.flipped):
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()

    def update(self):
        if self.dead and self.counter < 30:
            bigger_img = pygame.transform.scale(self.mario_dying, (64, 64))
            self.image = bigger_img.convert_alpha()
            self.rect = self.image.get_rect()
            self.counter += 1
            self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p
            return
        if self.dead and self.counter == 30:
            self.kill()
            return
        
        if self.dead:
            return

        if not self.previous_bottom == self.rect.bottom:
            bigger_img = self.mario_jump
        elif self.previous_center == self.rect.center:
            bigger_img = self.mario_still
        else:
            bigger_img = self.mario_running[self.current_mario]
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

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p
        collided = pygame.sprite.spritecollide(self, groundGroup, False)

        # Deal with Collisions with Enemies
        collidedWithEnemy = pygame.sprite.spritecollide(self, enemiesGroup, False)
        if(collidedWithEnemy):
            for e in enemiesGroup:
                if not self.collided_with_bottom(e.rect):
                    self.dead = True
                    self.counter = 0
                    return

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
        
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    def collided_with_bottom(self, rect):
        return rect.collidepoint(self.rect.bottomleft) or rect.collidepoint(self.rect.bottomright) or rect.collidepoint(self.rect.midbottom)

class SuperMario(egs.Game_objects.drawupdateable):
    # Sets the initial state of the Square class
    mario_running = []
    flipped = False
    counter = 0
    current_mario = 0
    previous_center = ()
    previous_bottom = ()
    collision = [False] * 9
    dead = False

    def __init__(self, pos):
        super().__init__()

        filename = "image\\superMarioSprites.png"

        piece_ss = SpriteSheet(filename)
        for i in range(3):
            mario_rect = (i*68, 0, 68, 134)
            mario_image = piece_ss.image_at(mario_rect)
            self.mario_running.append(mario_image)

        mario_rect = (204, 0, 68, 134)
        mario_image = piece_ss.image_at(mario_rect)
        self.mario_running.append(mario_image)

        mario_rect = (0, 0, 68, 134)
        self.mario_still = piece_ss.image_at(mario_rect)

        mario_rect = (272, 0, 68, 134)
        self.mario_jump = piece_ss.image_at(mario_rect)

        self.body = world.CreateDynamicBody(position=pos, fixedRotation = True)
        shape=b2PolygonShape(box=(p2b*32, p2b*64))
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=0, density=.5)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        self.image = self.mario_running[self.current_mario].convert_alpha()
        if(self.flipped):
            pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()

    def update(self):
        if(self.dead):
            return

        if not self.previous_bottom == self.rect.bottom:
            bigger_img =self.mario_jump
        elif self.previous_center == self.rect.center:
            bigger_img = self.mario_still
        else:
            bigger_img = self.mario_running[self.current_mario]
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

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p
        collided = pygame.sprite.spritecollide(self, groundGroup, False)
        
        # Deal with Collisions with Enemies
        collidedWithEnemy = pygame.sprite.spritecollide(self, enemiesGroup, False)
        if(collidedWithEnemy):
            for e in enemiesGroup:
                if not self.collided_with_bottom(e.rect):
                    self.dead = True
                    mario = Mario(self.body.position)
                    scene.drawables.add(mario)
                    scene.updateables.append(mario)
                    marioGroup.add(mario)
                    self.kill()
                    return

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
        
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    def collided_with_bottom(self, rect):
        return rect.collidepoint(self.rect.bottomleft) or rect.collidepoint(self.rect.bottomright) or rect.collidepoint(self.rect.midbottom)
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
height = 832
engine = egs.Engine("Mario 1-1", width = width, height = height)

scene = egs.Scene("Scene 1")
egs.Engine.current_scene = scene

background = Background()


ground = Ground(5.12,.64,5.76, .64)
platform = Ground(2.56 ,2.56,.64,.64)
mario = SuperMario((2.24, 3.52))
# goomba = Goomba((4,3.52))
flag = Flag((9.6,4.8))
koopa = KoopaShell((4.8,1.76))

groundGroup = pygame.sprite.Group()
groundGroup.add(ground)
groundGroup.add(platform)

enemiesGroup = pygame.sprite.Group()
# enemiesGroup.add(goomba)
enemiesGroup.add(koopa)

marioGroup = pygame.sprite.Group()
marioGroup.add(mario)

scene.drawables.add(background)
scene.drawables.add(ground)
scene.drawables.add(platform)
scene.drawables.add(mario)
# scene.drawables.add(goomba)
scene.drawables.add(koopa)
scene.drawables.add(flag)

scene.updateables.append(Updater())
scene.updateables.append(mario)
# scene.updateables.append(goomba)
scene.updateables.append(koopa)
scene.updateables.append(flag)

engine.start_game()
