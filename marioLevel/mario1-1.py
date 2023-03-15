#!/usr/bin/env python
import pygame

import os
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
        
        if os.name == 'nt':
            filename = "image\\background.png"
        else:
            filename = "image/background.png"

        self.dirty = 2
        self.body = world.CreateStaticBody(position = (135.04/2, height*p2b/2), active = False, shapes = b2PolygonShape(box = (135.04/2, height*p2b/2))) # body should be 121.92 meters.  Use active = false
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2p, height - self.body.position.y * b2p
        
class Brick(egs.Game_objects.drawupdateable):
    # Sets the initial state of the Square class
    def __init__(self, pos, contents = ""):
        super().__init__()

        if os.name == 'nt':
            filename = "image\\tileset.png"
        else:
            filename = "image/tileset.png"

        piece_ss = SpriteSheet(filename)

        self.dirty = 2
        
        self.contents = contents
        self.coinCounter = 288
        self.active = False

        brick_rect = (0, 68, 68, 68)
        ground_image = piece_ss.image_at(brick_rect)
        self.image = ground_image.convert_alpha()
        self.body = world.CreateStaticBody(position = pos, shapes = b2PolygonShape(box = (p2b*32, p2b*32)))
        self.rect = self.image.get_rect()

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    # This function switches whether the square is black or colored
    def update(self):
        collidedWithMario = pygame.sprite.spritecollide(self, groundGroup, False)

        if collidedWithMario:
            for m in marioGroup:
                if m.rect.collidepoint(self.rect.midbottom):
                    if self.coinCounter < 0 and not self.active:
                        print("POSITIVE*************")
                        self.coinCounter = 228
                        self.active = True
                    if self.contents == "coin":
                        if self.coinCounter > 0 and self.active:
                            coin = Coin((self.body.position.x, self.body.position.y +.64))
                            scene.drawables.add(coin)
                            scene.updateables.append(coin)
                        elif self.coinCounter < 0 and self.active:
                            self.coinCounter == 230
                            self.kill()
                            scene.updateables.remove(self)
                            stone = SolidStone(self.body.position, True)
                            self.body.position = (-10,-10)
                            scene.drawables.add(stone)
                            scene.updateables.append(stone)
                    elif self.contents == "star":
                        # star = Star((self.body.position.x, self.body.position.y + .64))
                        # scene.drawables.add(star)
                        # scene.updateables.append(star)
                        stone = SolidStone(self.body.position, True)
                        scene.drawables.add(stone)
                        scene.updateables.append(stone)
                        self.body.position = (-10, -10)
                        self.kill()
                        scene.updateables.remove(self)
                    elif type(m) != Mario:
                        self.kill()
                        scene.updateables.remove(self)
                        self.body.position = (-10.0, -10.0)
        if self.contents == "coin":
            self.coinCounter -= 1  
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p   

class Camera(egs.Game_objects.updateable):
    def __init__(self):
        super().__init__()

        self.total_offset = 0.0
        self.previous_offset = 0.0
        self.offset = 0.0
    
    def update(self):
        self.previous_offset = self.offset

        if self.total_offset <= 124.80 and mario.rect.right > 384:
            self.offset= (mario.rect.right - 384) * p2b
        else:
            self.offset = 0.0
        self.total_offset += self.offset
        for e in scene.drawables:
            e.body.position = (e.body.position[0] - self.offset, e.body.position[1])
            e.rect.center = e.body.position[0] * b2p, height - e.body.position[1] * b2p

class Coin(egs.Game_objects.drawupdateable):
    def __init__(self, pos):
        super().__init__()

        if os.name == 'nt':
            filename = "image\\tileset.png"
        else:
            filename = "image/tileset.png"

        piece_ss = SpriteSheet(filename)

        self.dirty = 2
        self.time_counter = 15
        coin_rect = (134, 0, 68, 68)
        ground_image = piece_ss.image_at(coin_rect)
        self.image = ground_image.convert_alpha()
        self.body = world.CreateStaticBody(position = pos, shapes = b2PolygonShape(box = (p2b*32, p2b*32)))
        self.rect = self.image.get_rect()


        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    # This function switches whether the square is black or colored
    def update(self):
        global coin_count

        if self.time_counter == 15:
            coin_count += 1
        elif self.time_counter == 0:
            self.kill()
            scene.updateables.remove(self)
            self.body.position = (-10,-10)
        self.time_counter -= 1

        self.rect.center = self.body.position[0] * b2p , height - self.body.position[1] * b2p

class FireBall(egs.Game_objects.drawupdateable):
    lifetime = 100
    images = []
    image_index = 0
    
    def __init__(self, pos, direction = 1):
        super().__init__()

        self.direction = direction

        if os.name == 'nt':
            filename = "image\\flames.png"
        else:
            filename = "image/flames.png"

        piece_ss = SpriteSheet(filename)

        self.dirty = 2

        fire_rect = (0, 0, 34, 34)
        fire_image = piece_ss.image_at(fire_rect)
        self.image = fire_image.convert_alpha()

        self.images.append(fire_image)

        fire_rect = (34, 0, 34, 34)
        fire_image = piece_ss.image_at(fire_rect)
        self.images.append(fire_image)

        fire_rect = (68, 0, 34, 34)
        fire_image = piece_ss.image_at(fire_rect)
        self.images.append(fire_image)

        fire_rect = (104, 0, 34, 34)
        fire_image = piece_ss.image_at(fire_rect)
        self.images.append(fire_image)

        self.body = world.CreateDynamicBody(position=pos, fixedRotation = True)
        shape=b2PolygonShape(box=(p2b*16, p2b*16))
        fixDef = b2FixtureDef(shape=shape, friction=0.1, restitution=1, density=.8)
        box = self.body.CreateFixture(fixDef)
        self.rect = self.image.get_rect()

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    def update(self):
        global mario
        
        self.body.ApplyForce(b2Vec2(self.direction, 0), self.body.position, True)

        if self.lifetime % 10 == 0:
            self.image = self.images[self.image_index].convert_alpha()
            self.image_index = 0 if self.image_index == 3  else self.image_index + 1

        collidedWithEnemy = pygame.sprite.spritecollide(self, enemiesGroup, False)
        if len(collidedWithEnemy) > 0:
            self.kill()
            scene.updateables.remove(self)
            self.body.position = (-10.0, -10.0)
            self.rect.center = -100 * b2p, height - -100 * b2p
            collidedWithEnemy[0].set_dead()
            # TODO update the score

        if self.lifetime == 0:
            self.kill()
            scene.updateables.remove(self)
            self.body.position = (-10.0, -10.0)
            self.rect.center = -100 * b2p, height - -100 * b2p

        self.lifetime -= 1
        self.rect.center = self.body.position[0] * b2p , height - self.body.position[1] * b2p

class FireFlower(egs.Game_objects.drawupdateable):
    def __init__(self, pos):
        super().__init__()

        if os.name == 'nt':
            filename = "image\\fireFlower.png"
        else:
            filename = "image/fireFlower.png"

        piece_ss = SpriteSheet(filename)

        self.dirty = 2

        fireFlower_rect = (0, 0, 68, 68)
        ground_image = piece_ss.image_at(fireFlower_rect)
        self.image = ground_image.convert_alpha()
        self.body = world.CreateStaticBody(position = pos, shapes = b2PolygonShape(box = (p2b*32, p2b*32)))
        self.rect = self.image.get_rect()

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    def update(self):
        global mario
        collidedWithMario = pygame.sprite.spritecollide(self, marioGroup, False)

        
        
        if collidedWithMario:
            self.kill()
            scene.updateables.remove(self)
            self.body.position = (-10.0, -10.0)
            self.rect.center = -100 * b2p, height - -100 * b2p
            mario.fire = True
            # TODO update the score

        self.rect.center = self.body.position[0] * b2p , height - self.body.position[1] * b2p

class FireMario(egs.Game_objects.drawupdateable):
    # Sets the initial state of the Square class
    mario_running = []
    flipped = False
    counter = 0
    current_mario = 0
    previous_center = ()
    previous_bottom = ()
    collision = [False] * 9
    dead = False
    fire = False

    def __init__(self, pos):
        super().__init__()

        if os.name == 'nt':
            filename = "image\\fireMario.png"
        else:
            filename = 'image/fireMario.png'

        piece_ss = SpriteSheet(filename)
        for i in range(3):
            mario_rect = (i*68, 0, 68, 132)
            mario_image = piece_ss.image_at(mario_rect)
            self.mario_running.append(mario_image)

        mario_rect = (204, 0, 68, 132)
        mario_image = piece_ss.image_at(mario_rect)
        self.mario_running.append(mario_image)

        mario_rect = (0, 0, 68, 132)
        self.mario_still = piece_ss.image_at(mario_rect)

        mario_rect = (272, 0, 68, 132)
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
        elif self.body.linearVelocity == (0,0):
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
        for e in enemiesGroup:
            if self.rect.colliderect(e.rect):
                if not self.rect.bottom  - 10 > e.rect.top and not type(e) == "<class '__main__.KoopaShell'>":
                    self.die()
                    return
                elif not self.rect.bottom  - 10 > e.rect.top and type(e) == "<class '__main__.KoopaShell'>" and e.stationary:
                    self.die()
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
                if event.key == pygame.K_SPACE:
                    fireball = FireBall((self.body.position.x + .55, self.body.position.y + .46))
                    fireGroup.add(fireball)
                    scene.drawables.add(fireball)
                    scene.updateables.append(fireball)
        
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    def die(self):
        global mario

        self.dead = True
        mario = Mario(self.body.position, 500)
        scene.drawables.add(mario)
        scene.updateables.append(mario)
        marioGroup.add(mario)
        self.kill()
        scene.updateables.remove(self)
        self.body.position = (-10.0, -10.0)

class Flag(egs.Game_objects.drawupdateable):
    flag_sprites = []
    index = 0
    counter = 0
    # Sets the initial state of the Square class
    def __init__(self, pos):
        super().__init__()

        # self.reached = True
        if os.name == 'nt':
            filename = "image\\flag.png"
        else:
            filename = 'image/flag.png'

        piece_ss = SpriteSheet(filename)
        for i in range(9):
            flag_rect = (i*128, 0, 128, 706)
            flag_image = piece_ss.image_at(flag_rect)
            self.flag_sprites.append(flag_image)
        self.body = world.CreateStaticBody(position = pos, shapes = b2PolygonShape(box = (p2b* 32, p2b*352)))
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
        if os.name == 'nt':
            filename = "image\\enemies.png"
        else:
            filename = 'image/enemies.png'

        piece_ss = SpriteSheet(filename)
        for i in range (2):
            goomba_rect = (i*68, 0, 68, 68)
            goomba_image = piece_ss.image_at(goomba_rect)
            self.goomba_sprites.append(goomba_image)

        goomba_rect = (136, 0, 68, 68)
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
        if not self.body:
            return

        if self.dead and self.counter < 30:
            bigger_img = pygame.transform.scale(self.goomba_dying, (64, 64))
            self.image = bigger_img.convert_alpha()
            self.rect = self.image.get_rect()
            self.counter += 1
            self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p
            enemiesGroup.remove(self)
            return
        if self.dead and self.counter == 30:
            self.body.position = (-10.0, -10.0)
            self.kill()
            scene.updateables.remove(self)
            return
        
        if self.dead:
            self.rect.center = -100 * b2p, height - -100 * b2p
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
                if collidedWithEnemy:
                    for m in marioGroup:
                        if self.rect.colliderect(m.rect):
                            if self.rect.top + 10 >= m.rect.bottom:                            
                                self.set_dead()
                                return
                            
            else:
                self.last_center = self.rect.center
                self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p
                self.counter = self.counter + 1 
        else:
            self.kill()
            scene.updateables.remove(self)    
            self.body.position = (-10.0, -10.0)
      
    def set_dead(self):
        self.dead = True
        self.counter = 0
        enemiesGroup.remove(self)


    def collided_with_top(self, rect):
        return rect.collidepoint(self.rect.topleft) or rect.collidepoint(self.rect.topright) or rect.collidepoint(self.rect.midtop)

class Ground(egs.Game_objects.drawable):

    # Sets the initial state of the Square class
    def __init__(self, x, w, y=.64, h= 1.28):
        super().__init__()

        if os.name == 'nt':
            filename = "image\\ground.png"
        else:
            filename = 'image/ground.png'

        piece_ss = SpriteSheet(filename)

        self.dirty = 2

        width_in_pixels = w * b2p 
        height_in_pixels = h * b2p + 4
        
        # Pixels may be off due to scaling issues.  Everything is currently multiplied by 4 other places
        ground_rect = (0, 0, width_in_pixels, height_in_pixels)
        ground_image = piece_ss.image_at(ground_rect)

        self.dirty = 2

        self.body = world.CreateStaticBody(position=(x, y), shapes=b2PolygonShape(box=(w/2, h/2)))

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
        
        if os.name == 'nt':
            filename = "image\\enemies.png"
        else:
            filename = 'image/enemies.png'

        piece_ss = SpriteSheet(filename)
        
        koopa_rect = (0, 68, 68, 100)
        koopa_image = piece_ss.image_at(koopa_rect)
        self.koopa_walking.append(koopa_image)

        self.body = world.CreateDynamicBody(position=pos, fixedRotation = True)
        shape=b2PolygonShape(box=(p2b*32, p2b*48))
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=0, density=1)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2

        koopa_rect = (68, 68, 68, 100)
        koopa_image = piece_ss.image_at(koopa_rect)
        self.koopa_walking.append(koopa_image)

        self.image = self.koopa_walking[self.current_koopa].convert_alpha()
        self.current_koopa = (self.current_koopa + 1) % 2

        self.rect = self.image.get_rect()
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    # This function switches whether the square is black or colored
    def update(self):
        if self.dead:
            self.rect.center = -100 * b2p, height - -100 * b2p
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

        
        collidedWithEnemy = pygame.sprite.spritecollide(self, marioGroup, False)
        if(collidedWithEnemy):
            for e in enemiesGroup:
                if self.rect.colliderect(e.rect):
                    if e.rect.bottom > self.rect.top:
                        self.set_dead()
                        return

        self.rect = self.image.get_rect()
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    def set_dead(self):
        self.dead = True
        koopa = KoopaShell(self.body.position)
        scene.drawables.add(koopa)
        scene.updateables.append(koopa)
        enemiesGroup.add(koopa)
        enemiesGroup.remove(self)
        self.kill()
        scene.updateables.remove(self) 
        self.body.position = (-10.0, -10.0)

    def collided_with_top(self, rect):
        return rect.collidepoint(self.rect.topleft) or rect.collidepoint(self.rect.topright) or rect.collidepoint(self.rect.midtop)

class KoopaShell(egs.Game_objects.drawupdateable):
    counter = 0
    dead = False
    stationary = False

    # Sets the initial state of the Square class
    def __init__(self, pos):
        super().__init__()
        
        if os.name == 'nt':
            filename = "image\\enemies.png"
        else:
            filename = 'image/enemies.png'
        piece_ss = SpriteSheet(filename)
        
        koopa_rect = (136, 100, 68, 68)
        self.koopa_shell = piece_ss.image_at(koopa_rect)

        koopa_rect = (204, 100, 68, 68)
        self.koopa_shell_legs = piece_ss.image_at(koopa_rect)

        self.body = world.CreateDynamicBody(position=pos, fixedRotation = True)
        shape=b2PolygonShape(box=(p2b*32, p2b*32))
        fixDef = b2FixtureDef(shape=shape, friction=0.05, restitution=0, density=1)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2

        self.image = self.koopa_shell.convert_alpha()
        self.rect = self.image.get_rect()

        self.previous_pos = self.rect.center

    # This function switches whether the square is black or colored
    def update(self):
        if self.dead:
            self.rect.center = -100 * b2p, height - -100 * b2p
            return
        
        if self.previous_pos == self.rect.center:
            self.stationary = True
        
        self.previous_pos = self.rect.center

        if self.counter == 560:
            koopa = Koopa(self.body.position)
            enemiesGroup.add(koopa)
            scene.drawables.add(koopa)
            scene.updateables.append(koopa)
            self.dead = True
            self.kill()
            scene.updateables.remove(self) 
            self.body.position = (-10.0, -10.0)
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

    def set_dead(self):
        pass
class Mario(egs.Game_objects.drawupdateable):
     # Sets the initial state of the Square class
    mario_running = []
    flipped = False
    counter = 0
    current_mario = 0
    previous_center = ()
    previous_bottom = ()
    dead = False
    mushroom = False
    star = False
    fire = False

    def __init__(self, pos, immunity = 0):
        super().__init__()

        self.immune = immunity

        if os.name == 'nt':
            filename = "image\\marioSprites.png"
        else:
            filename = 'image/marioSprites.png'

        piece_ss = SpriteSheet(filename)
        for i in range(3):
            mario_rect = (i*68, 0, 68, 68)
            mario_image = piece_ss.image_at(mario_rect)
            self.mario_running.append(mario_image)

        mario_rect = (204, 0, 68, 68)
        mario_image = piece_ss.image_at(mario_rect)
        self.mario_running.append(mario_image)

        mario_rect = (0, 0, 68, 68)
        self.mario_still = piece_ss.image_at(mario_rect)

        mario_rect = (272, 0, 68, 68)
        self.mario_jump = piece_ss.image_at(mario_rect)

        mario_rect = (340, 0, 68, 68)
        self.mario_dying = piece_ss.image_at(mario_rect)


        self.body = world.CreateDynamicBody(position=pos, fixedRotation=True)
        shape=b2PolygonShape(box=(p2b*32, p2b*32))
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=0, density=1)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        self.image = self.mario_running[self.current_mario].convert_alpha()
        if(self.flipped):
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()

    def update(self):
        global mario

        if self.dead and self.counter < 30:
            self.image = self.mario_dying.convert_alpha()
            self.rect = self.image.get_rect()
            self.counter += 1
            self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p
            return
        if self.dead and self.counter == 30:
            self.kill()
            scene.updateables.remove(self)
            self.body.position = (-10.0, -10.0)
            return
        
        if self.dead:
            return
        
        if not self.previous_bottom == self.rect.bottom:
            bigger_img = self.mario_jump
        elif self.body.linearVelocity == (0,0):
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

        if self.immune < 0:
            # Deal with Collisions with Enemies
            for e in enemiesGroup:
                if self.rect.colliderect(e.rect):
                    if self.rect.bottom - 10 >= e.rect.top:
                        self.dead = True
                        self.counter = 0
                        return
                    
        if self.mushroom:
            self.dead = True
            mario = SuperMario(self.body.position)
            scene.drawables.add(mario)
            scene.updateables.append(mario)
            marioGroup.add(mario)
            self.kill()
            scene.updateables.remove(self)
            self.body.position = (-10.0, -10.0)
            

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
        
        self.immune -= 1
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

class Mushroom(egs.Game_objects.drawupdateable):
    def __init__(self, pos):
        super().__init__()

        filename = "image/tileset.png"

        piece_ss = SpriteSheet(filename)

        self.dirty = 2

        mushroom_rect = (134, 68, 68, 68)
        ground_image = piece_ss.image_at(mushroom_rect)
        self.image = ground_image.convert_alpha()
        self.body = world.CreateStaticBody(position = pos, shapes = b2PolygonShape(box = (p2b*32, p2b*32)))
        self.rect = self.image.get_rect()

        self.rect.center = self.body.position[0] * b2p , height - self.body.position[1] * b2p

    def update(self):
        global mario
        collidedWithMario = pygame.sprite.spritecollide(self, marioGroup, False)

        if collidedWithMario:
            self.kill()
            scene.updateables.remove(self)
            self.body.position = (-10.0, -10.0)
            self.rect.center = -100 * b2p, height - -100 * b2p
            mario.mushroom = True
            # TODO update the score

        self.rect.center = self.body.position[0] * b2p , height - self.body.position[1] * b2p

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
    fire = False

    def __init__(self, pos, immunity = 0):
        super().__init__()

        self.immune = immunity

        if os.name == 'nt':
            filename = "image\\superMarioSprites.png"
        else:
            filename = 'image/superMarioSprites.png'

        piece_ss = SpriteSheet(filename)
        for i in range(3):
            mario_rect = (i*68, 0, 68, 132)
            mario_image = piece_ss.image_at(mario_rect)
            self.mario_running.append(mario_image)

        mario_rect = (204, 0, 68, 132)
        mario_image = piece_ss.image_at(mario_rect)
        self.mario_running.append(mario_image)

        mario_rect = (0, 0, 68, 132)
        self.mario_still = piece_ss.image_at(mario_rect)

        mario_rect = (272, 0, 68, 132)
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
        global mario
        if(self.dead):
            return

        if not self.previous_bottom == self.rect.bottom:
            bigger_img =self.mario_jump
        elif self.body.linearVelocity == (0,0):
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
        
        if self.immune < 0:
        # Deal with Collisions with Enemies
            for e in enemiesGroup:
                if self.rect.colliderect(e.rect):
                    if not self.rect.bottom  - 10 > e.rect.top and not type(e) == "<class '__main__.KoopaShell'>":
                        self.die()
                        return
                    elif not self.rect.bottom  - 10 > e.rect.top and type(e) == "<class '__main__.KoopaShell'>" and e.stationary:
                        self.die()
                        return
                
        if self.fire:
            self.dead = True
            mario = FireMario(self.body.position)
            scene.drawables.add(mario)
            scene.updateables.append(mario)
            marioGroup.add(mario)
            self.kill()
            scene.updateables.remove(self)
            self.body.position = (-10.0, -10.0)

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
        
        self.immune -= 1
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    def die(self):
        global mario

        self.dead = True
        mario = Mario(self.body.position, 500)
        scene.drawables.add(mario)
        scene.updateables.append(mario)
        marioGroup.add(mario)
        self.kill()
        scene.updateables.remove(self)
        self.body.position = (-10.0, -10.0)

class QuestionBlock(egs.Game_objects.drawupdateable):
    destroyed = False
     # Sets the initial state of the Square class
    def __init__(self, pos, powerup = False):
        super().__init__()

        filename = "image/tileset.png"

        piece_ss = SpriteSheet(filename)
        self.powerup = powerup

        self.dirty = 2

        brick_rect = (68, 0, 68, 68)
        ground_image = piece_ss.image_at(brick_rect)
        self.image = ground_image.convert_alpha()
        self.body = world.CreateStaticBody(position = pos, shapes = b2PolygonShape(box = (p2b*32, p2b*32)))
        self.rect = self.image.get_rect()

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    # This function switches whether the square is black or colored
    def update(self):
        if self.destroyed:
            return

        collidedWithMario = pygame.sprite.spritecollide(self, groundGroup, False)

        if collidedWithMario:
            for m in marioGroup:
                if m.rect.collidepoint(self.rect.midbottom):
                    self.kill()
                    scene.updateables.remove(self)
                    stone = SolidStone(self.body.position, True)
                    if self.powerup:
                        if type(m) == SuperMario or type(m) == FireMario: 
                            powerup = FireFlower((self.body.position.x, self.body.position.y + .64))
                        else:
                            powerup = Mushroom((self.body.position.x, self.body.position.y + .64))
                    else:
                        powerup = Coin((self.body.position.x, self.body.position.y+.64))
                    self.body.position = (-10.0, -10.0)
                    groundGroup.add(stone)
                    scene.drawables.add(stone)
                    scene.drawables.add(powerup)
                    scene.updateables.append(stone)
                    scene.updateables.append(powerup)
                    self.destroyed = True
                    return


        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

class Pipe(egs.Game_objects.drawable):

    def __init__(self, xpos, h):
        super().__init__()

        if os.name == 'nt':
            filename = "image\\pipes.png"
        else:
            filename = 'image/pipes.png'
        
        piece_ss = SpriteSheet(filename)

        self.dirty = 2
        width_in_pixels = 128
        height_in_pixels = h * 64

        ypos = 1.28 + (height_in_pixels * p2b / 2)

        pipe_rect = ((h-2)*132, 0, width_in_pixels + 4, height_in_pixels + 4)
        pipe_image = piece_ss.image_at(pipe_rect)

        self.body = world.CreateStaticBody(position = (xpos, ypos) , shapes = b2PolygonShape(box = (.64, (h*.64)/2)))

        self.image = pipe_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2p, height - self.body.position.y * b2p
                                        

class SolidStone(egs.Game_objects.drawable):
     # Sets the initial state of the Square class
    def __init__(self, pos, isUsed = False):
        super().__init__()

        filename = "image/tileset.png"

        piece_ss = SpriteSheet(filename)

        self.dirty = 2
        if isUsed:
            brick_rect = (68, 68, 68, 68)
        else:
            brick_rect = (0, 0, 68, 68)
        ground_image = piece_ss.image_at(brick_rect)
        self.image = ground_image.convert_alpha()
        self.body = world.CreateStaticBody(position = pos, shapes = b2PolygonShape(box = (p2b*32, p2b*32)))
        self.rect = self.image.get_rect()

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

class Updater(egs.Game_objects.updateable):
    def __init__(self):
        super().__init__()

    def update(self):
        try:
            world.Step(timeStep, vec_iters, pos_iters)
            world.ClearForces()
        except:
            print("Oh no")


def createGround():
    grounds = []
    grounds.append(Ground(22.08,44.16))
    grounds.append(Ground(50.24,9.6))
    grounds.append(Ground(77.44, 40.96))
    grounds.append(Ground(117.12, 35.84))

    for e in grounds:
        groundGroup.add(e)
        scene.drawables.add(e)

def createQuestions():
    questions = []

    questions.append(QuestionBlock((10.56, 3.52)))
    questions.append(QuestionBlock((13.76,3.52), True))
    questions.append(QuestionBlock((15.04,3.52)))
    questions.append(QuestionBlock((14.40,6.08)))
    questions.append(QuestionBlock((50.24,3.52), True))
    questions.append(QuestionBlock((60.48,6.08)))
    questions.append(QuestionBlock((68.16,3.52)))
    questions.append(QuestionBlock((70.08,6.08), True))
    questions.append(QuestionBlock((70.08,3.52)))
    questions.append(QuestionBlock((72,3.52)))
    questions.append(QuestionBlock((82.88,6.08)))
    questions.append(QuestionBlock((83.52,6.08)))
    questions.append(QuestionBlock((109.12,3.52)))

    for item in questions:
        groundGroup.add(item)
        scene.drawables.add(item)
        scene.updateables.append(item)

def createBricks():
    bricks = []
    bricks.append(Brick((13.12, 3.52)))    
    bricks.append(Brick((14.40, 3.52)))
    bricks.append(Brick((15.68, 3.52)))
    bricks.append(Brick((49.60, 3.52)))
    bricks.append(Brick((50.88, 3.52)))
    bricks.append(Brick((51.52, 6.08)))
    bricks.append(Brick((52.16, 6.08)))
    bricks.append(Brick((52.80, 6.08)))
    bricks.append(Brick((53.44, 6.08)))
    bricks.append(Brick((54.08, 6.08)))
    bricks.append(Brick((54.72, 6.08)))
    bricks.append(Brick((55.36, 6.08)))
    bricks.append(Brick((56, 6.08)))
    bricks.append(Brick((58.56, 6.08)))
    bricks.append(Brick((59.20, 6.08)))
    bricks.append(Brick((59.84, 6.08)))
    bricks.append(Brick((60.48, 3.52), "coin"))
    bricks.append(Brick((64.32, 3.52)))
    bricks.append(Brick((64.96, 3.52), "star"))
    bricks.append(Brick((75.84, 3.52)))
    bricks.append(Brick((77.76, 6.08)))
    bricks.append(Brick((78.4, 6.08)))
    bricks.append(Brick((79.04, 6.08)))
    bricks.append(Brick((82.24, 6.08)))
    bricks.append(Brick((82.88, 3.52)))
    bricks.append(Brick((83.52, 3.52)))
    bricks.append(Brick((84.16, 6.08)))
    bricks.append(Brick((107.84, 3.52)))
    bricks.append(Brick((108.48, 3.52)))
    bricks.append(Brick((109.76, 3.52)))

    for e in bricks:
        groundGroup.add(e)
        scene.drawables.add(e)
        scene.updateables.append(e)

def createPipes():
    pipes = []
    pipes.append(Pipe(18.56, 2))
    pipes.append(Pipe(24.96, 3))
    pipes.append(Pipe(30.08, 4))
    pipes.append(Pipe(37.12, 4))
    pipes.append(Pipe(104.96, 2))
    pipes.append(Pipe(115.20, 2))
    for item in pipes:
        groundGroup.add(item)
        scene.drawables.add(item)

width = 1024
height = 832
coin_count = 0
engine = egs.Engine("Mario 1-1", width = width, height = height)

scene = egs.Scene("Scene 1")
egs.Engine.current_scene = scene

view = Camera()

background = Background()

mario = FireMario((2.24, 3.52))
# goomba = Goomba((4,3.52))
# flag = Flag((90.92,4.8))
koopa = Koopa((10.24,1.76))

groundGroup = pygame.sprite.Group()

fireGroup = pygame.sprite.Group()
# fireGroup.add(fireball)

enemiesGroup = pygame.sprite.Group()
# enemiesGroup.add(goomba)
enemiesGroup.add(koopa)

marioGroup = pygame.sprite.Group()
marioGroup.add(mario)

scene.drawables.add(background)
scene.drawables.add(mario)
# scene.drawables.add(fireball)
# scene.drawables.add(goomba)
scene.drawables.add(koopa)
# scene.drawables.add(flag)

scene.updateables.append(Updater())

scene.updateables.append(mario)

# scene.updateables.append(fireball)
# scene.updateables.append(goomba)
scene.updateables.append(koopa)
# scene.updateables.append(flag)

createGround()
createQuestions()
createBricks()
createPipes()

scene.updateables.append(view)

engine.start_game()
