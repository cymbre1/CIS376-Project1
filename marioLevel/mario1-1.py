# Kit Bazner and Cymbre Spoehr

#!/usr/bin/env python
import pygame
from pygame.locals import *
from pygame import mixer

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

# A class to hold the background.  Inherits from a drawable game object
class Background(egs.Game_objects.drawable):
    # Creates the background
    def __init__(self):
        super().__init__()
        
        if os.name == 'nt':
            filename = "image\\background.png"
        else:
            filename = "image/background.png"

        self.dirty = 2
        self.body = world.CreateStaticBody(position = (165.76/2, height*p2b/2), active = False, shapes = b2PolygonShape(box = (165.76/2, height*p2b/2))) # body should be 121.92 meters.  Use active = false
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2p, height - self.body.position.y * b2p

# This is a helper class that all marios will inheirit from
class BaseMario(egs.Game_objects.drawable):
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
    star_count = -1

    # Initializes a mario, sets up the images, and sets the position
    # Params
    # int tuple pos, the position where Mario will start
    # int immunity controls how long mario will be invincible after his creation
    # int tuple size communicates the size mario is, it is defaulted to the size of small mario
    # string image_file is the file that mario's sprites will be pulled from. It is defaulted to small mario's sprites
    def __init__(self, pos, immunity = 0, size=(68, 68), image_file='marioSprites.png'):
        super().__init__()  

        self.immune = immunity

        self.load_images(size, image_file)


        self.body = world.CreateDynamicBody(position=pos, fixedRotation=True)
        shape=b2PolygonShape(box=(p2b*((size[0]/2) - 2), p2b*((size[1]/2) - 2)))
        if size[1] == 68:
            fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=0, density=1)
        else:
            fixDef = b2FixtureDef(shape=shape, friction=0.4, restitution=0, density=.6)

        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        self.image = self.mario_running[self.current_mario].convert_alpha()
        if(self.flipped):
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    # Updates mario
    def update(self):
        global mario

        self.check_star()

        if self.body.position[1] < 0:
            self.die()

        self.update_animation()

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

        self.check_enemy_collision()
                    
        self.handle_powerup()          

        self.handle_keyboard_events()
        
        if self.rect.left <= 0:
            self.body.linearVelocity =(.1, self.body.linearVelocity[1])
        
        self.star_count -= 1
        self.immune -= 1
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    # This function loads the images for the star mario as well as changes the music
    # Params
    # int tuple size, the size of the current mario, defaults to the size of small mario
    def convert_star(self, size=(68, 68)):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join('sound', 'invincible.mp3'))
        pygame.mixer.music.play()

        self.load_images(size, 'starMario.png' if size[1] == 68 else 'starSuperMario.png')

    # This function converts the sprites into the regular sprites (Not star mario) and changes the music back to the theme
    # Params
    # int tuple size, the size of the current mario, defaults to the size of small mario
    # boolean fire, which just holds whether or not the current mario is fire mario, defaulted to false 
    def convert_fromStar(self, size=(68,68), fire=False):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join('sound', 'theme.mp3'))
        pygame.mixer.music.play()

        if size[1] == 68:
            filename = 'marioSprites.png'
        elif fire: 
            filename = 'fireMario.png'
        else:
            filename = 'superMarioSprites.png'

        self.load_images(size, filename)

    # This function handles collision with enemies, whether or not mario dies, and whether or not the enemy itself dies.
    def check_enemy_collision(self):
        if self.star_count < 0:                
            for e in enemiesGroup:
                if self.rect.colliderect(e.rect):
                    if type(e) != KoopaShell:
                        if self.rect.bottom > e.rect.centery:
                            if self.immune <= 0:
                                self.die()
                        elif self.rect.centerx + 10 > e.rect.left or self.rect.centerx - 10 < e.rect.right:
                            pygame.mixer.Sound.play(music.stomp_sound)
                            e.set_dead()
                            self.body.ApplyLinearImpulse(b2Vec2(0, 4), self.body.position, True)
                    else:
                        koopa_force = 1.75
                        if e.stationary:
                            if self.rect.centerx < e.rect.centerx:
                                e.body.ApplyLinearImpulse(b2Vec2(koopa_force,0), e.body.position, True)
                            else:
                                e.body.ApplyLinearImpulse(b2Vec2(0 - koopa_force, 0), e.body.position, True)
                            if self.rect.bottom < e.rect.centery:
                                self.body.ApplyLinearImpulse(b2Vec2(0, 4), self.body.position, True)
                        else:
                            if self.rect.bottom > e.rect.centery:
                                if self.immune <= 0:
                                    self.die()
                            else:
                                if self.rect.centerx < e.rect.centerx:
                                    e.body.linearVelocity = (0,0)
                                    e.body.ApplyLinearImpulse(b2Vec2(koopa_force,0), e.body.position, True)
                                else:
                                    e.body.linearVelocity = (0,0)
                                    e.body.ApplyLinearImpulse(b2Vec2(0 - koopa_force, 0), e.body.position, True)
        else:
            collidedEnemies = pygame.sprite.spritecollide(self, enemiesGroup, False)
            for e in collidedEnemies:
                pygame.mixer.Sound.play(music.kick_sound)
                e.set_dead()

    # This function checks to see if the player has a star or if the star effect has expired
    def check_star(self):
        if self.star:
            self.star_count = 636
            self.convert_star()
            self.star = False
        if self.star_count == 0:
            self.convert_fromStar()

    # This function makes a new mario because mario has changed state and destroys the current mario
    # Params
    # BaseMario mario, the Mario that is going to be the new mario
    def replace_mario(self, mario):
        self.dead = True
        scene.drawables.add(mario)
        scene.updateables.append(mario)
        marioGroup.add(mario)
        self.kill()
        scene.updateables.remove(self)
        self.body.position = (-10.0, -10.0)

    # This function loads a given image into the different poses for mario
    # Params
    # int tuple size, the size of the sprite for the images to be loaded into
    # string image_file is the file in the images folder that contains the desired sprites
    def load_images(self, size, image_file):
        s = 'image'

        filename = os.path.join(s, image_file)

        self.mario_running.clear()

        piece_ss = SpriteSheet(filename)
        for i in range(3):
            mario_rect = (i*68, 0, size[0], size[1])
            mario_image = piece_ss.image_at(mario_rect)
            self.mario_running.append(mario_image)

        mario_rect = (204, 0, size[0], size[1])
        mario_image = piece_ss.image_at(mario_rect)
        self.mario_running.append(mario_image)

        mario_rect = (0, 0, size[0], size[1])
        self.mario_still = piece_ss.image_at(mario_rect)

        mario_rect = (272, 0, size[0], size[1])
        self.mario_jump = piece_ss.image_at(mario_rect)

        mario_rect = (340, 0, size[0], size[1])
        self.mario_dying = piece_ss.image_at(mario_rect)

    # This function will animate Mario's movements based on how he is moving
    def update_animation(self):
        if not self.previous_bottom == self.rect.bottom:
            image = self.mario_jump
        elif self.body.linearVelocity == (0,0):
            image = self.mario_still
        else:
            image = self.mario_running[self.current_mario]
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

        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()    

        if(self.flipped):
            self.image = pygame.transform.flip(self.image, True, False)

    # This function will change Mario's state given a powerup that he has acquired.
    def handle_powerup(self):
        global mario

        if self.mushroom or self.fire:
            self.dead = True
            if self.rect.height == 68:
                mario = SuperMario(self.body.position)
            elif self.fire:
                mario = FireMario(self.body.position)
            mario.star_count = self.star_count
            if self.star_count > 0:
                mario.convert_star() 
            self.replace_mario(mario) 

    # This function will handle Mario's movements based on keyboard input.
    def handle_keyboard_events(self):
        collided = pygame.sprite.spritecollide(self, groundGroup, False)

        for event in egs.Engine.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if collided:
                        self.body.ApplyForce(b2Vec2(-75,0), self.body.position, True)
                    else:
                        self.body.ApplyForce(b2Vec2(-35, 0), self.body.position, True)                    
                    self.flipped = True
                if event.key == pygame.K_d:
                    if collided:
                        for c in collided:
                            if type(c) == Pipe:
                                if c.underground:
                                    view.loaded = False
                                    view.offset = c.teleport_point[0] - view.total_offset
                                    self.body.linearVelocity = (0,0)
                                    self.body.position = (c.teleport_point[0] + .32- view.total_offset, c.teleport_point[1])
                        self.body.ApplyForce(b2Vec2(75,0), self.body.position, True)
                    else:
                        self.body.ApplyForce(b2Vec2(35, 0), self.body.position, True)
                    self.flipped = False
                if event.key == pygame.K_w:
                    if collided:
                        for c in collided:
                            if c.rect.collidepoint(self.rect.midbottom):
                                pygame.mixer.Sound.play(music.jump_small if self.rect.height == 68 else music.jump_big)
                                if self.rect.height == 68:
                                    self.body.ApplyLinearImpulse(b2Vec2(0,3.25), self.body.position, True)
                                else:
                                    self.body.ApplyLinearImpulse(b2Vec2(0,3.75), self.body.position, True)
                if event.key == pygame.K_s:
                    if collided:
                        for c in collided:
                            if type(c) == Pipe:
                                if c.active and self.rect.bottom + 2 > c.rect.top - 2:
                                    view.pipe = True
                                    view.loaded = False
                                    self.body.linearVelocity = (0,0)
                                    self.body.position = (135.68 - view.total_offset, c.teleport_point[1])
                                    view.offset = c.teleport_point[0] - view.total_offset

                if event.key == pygame.K_SPACE:
                    self.shoot_fire()
 
# A class that defines the interactable bricks.  Inherits from a drawable and updateable game object     
class Brick(egs.Game_objects.drawupdateable):
    # Sets the initial state of the Brick class
    # Parameters:
    # Tuple pos is the starting position of the brick of the level in meters
    # String contents is the name of what the brick contains
    def __init__(self, pos, contents = "", underground = False):
        super().__init__()

        if underground:
            filename = os.path.join("image", "underTileset.png")
        else:
            filename = os.path.join("image", "tileset.png")

        piece_ss = SpriteSheet(filename)

        self.dirty = 2
        
        self.contents = contents
        self.coinCounter = 288
        self.active = False
        self.underground = underground
        if self.underground:
            brick_rect =(0, 0, 68, 68) 
        else:
            brick_rect = (0, 68, 68, 68)
        ground_image = piece_ss.image_at(brick_rect)
        self.image = ground_image.convert_alpha()
        self.body = world.CreateStaticBody(position = pos, shapes = b2PolygonShape(box = (p2b*32, p2b*32)))
        self.rect = self.image.get_rect()

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    # Updates the brick
    def update(self):
        collidedWithMario = pygame.sprite.spritecollide(self, groundGroup, False)

        # handles collisions with mario.  Behavior depends on mario type and contents
        if collidedWithMario:
            for m in marioGroup:
                if m.rect.collidepoint(self.rect.midbottom):
                    if self.coinCounter < 0 and not self.active:
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
                            groundGroup.add(stone)
                    elif self.contents == "star":
                        pygame.mixer.Sound.play(music.powerup_appears_sound)
                        star = Star((self.body.position.x, self.body.position.y + .64))
                        scene.drawables.add(star)
                        scene.updateables.append(star)
                        stone = SolidStone(self.body.position, True)
                        scene.drawables.add(stone)
                        scene.updateables.append(stone)
                        groundGroup.add(stone)
                        self.body.position = (-10, -10)
                        self.kill()
                        scene.updateables.remove(self)
                    elif type(m) != Mario:
                        pygame.mixer.Sound.play(music.brick_break_sound)
                        self.kill()
                        scene.updateables.remove(self)
                        self.body.position = (-10.0, -10.0)
        # only decrements the coin counter if it's a coin brick
        if self.contents == "coin":
            self.coinCounter -= 1  
        # sets the position of self.rect to reflect the changes from box2d
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p   

# A class that helps move the screen based player movement.  Inherits from an updateable game object
class Camera(egs.Game_objects.updateable):
    
    # initializes the Camera class
    def __init__(self):
        super().__init__()

        self.levelFinished = False
        self.marioDead = False
        self.pipe = False
        self.loaded = False
        self.total_offset = 0.0
        self.offset = 0.0
    
    # updates the camera object based on mario's position
    def update(self):
        if not self.marioDead:
            if not self.pipe:
                if self.total_offset < 124.80 and mario.rect.right > 384:
                    self.offset= (mario.rect.right - 384) * p2b
                elif not self.levelFinished:
                    self.offset = 0.0
            elif self.loaded:
                self.offset = 0.0
            else:
                self.loaded = True
                if self.offset < 0:
                    self.pipe = False
        else:
            view.offset = 145.28 - view.total_offset
            self.marioDead = False
        self.total_offset += self.offset

        # loops through all visible objects and updates b2 body position based on offset 
        for e in scene.drawables:
            e.body.position = (e.body.position[0] - self.offset, e.body.position[1])
            e.rect.center = e.body.position[0] * b2p, height - e.body.position[1] * b2p
            if type(e) == Castle:
                e.door_rect.center = e.body.position.x * b2p, height - e.body.position.y * b2p + 97

# A class that creates the castle
class Castle(egs.Game_objects.drawupdateable):
    # This function creates the castle
    # Parameters:
    # Tuple pos is the position of the middle of the castle in meters
    def __init__(self, pos):
        super().__init__()
        if os.name == 'nt':
            filename = "image\\castle.png"
        else:
            filename = "image/castle.png"
        
        piece_ss = SpriteSheet(filename)

        castle_rect = (0,0,328,328)
        castle_image = piece_ss.image_at(castle_rect)

        self.door_rect = pygame.Rect(0,0,64,129)

        self.levelFinished = False
        
        self.body = world.CreateStaticBody(position = pos, active = False, shapes = b2PolygonShape(box = (3.24/2, 3.24/2)))
        self.image = castle_image
        self.rect = self.image.get_rect()
        self.door_rect.center = self.body.position.x * b2p, height - self.body.position.y * b2p + 97
        self.rect.center = self.body.position.x * b2p, height - self.body.position.y * b2p

    # This function checks if mario has reached the castle door, and jumps to a completed screen
    def update(self):
        if not self.levelFinished and self.door_rect.colliderect(mario.rect):
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(music.level_finished_sound)
            view.levelFinished = True
            self.levelFinished = True
            view.offset = 155.52 - view.total_offset
        elif self.levelFinished:
            view.offset = 0.0

# A class that creates a coin in the world   
class Coin(egs.Game_objects.drawupdateable):
    
    # Creates the coin in the world
    # Parameters:
    # Tuple pos is the position of the center of the coin in meters
    def __init__(self, pos, underground = False):
        super().__init__()

        if underground:
            filename = os.path.join("image", "underTileset.png")
        else:
            filename = os.path.join("image", "tileset.png")

        piece_ss = SpriteSheet(filename)
        pygame.mixer.Sound.play(music.coin_sound)


        self.dirty = 2
        self.time_counter = 15
        self.underground = underground
        if self.underground:
            coin_rect(68, 0, 68, 68)
        else:
            coin_rect = (134, 0, 68, 68)
        ground_image = piece_ss.image_at(coin_rect)
        self.image = ground_image.convert_alpha()
        self.body = world.CreateStaticBody(position = pos, shapes = b2PolygonShape(box = (p2b*32, p2b*32)))
        self.rect = self.image.get_rect()


        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    # This function adds to the coin count and makes the coin dissapear after the time counter is finished
    def update(self):
        global coin_count
        if self.underground:
            coin_count += 1
        else:
            if self.time_counter == 15:
                coin_count += 1
            elif self.time_counter == 0:
                self.kill()
                scene.updateables.remove(self)
                self.body.position = (-10,-10)
            self.time_counter -= 1

        self.rect.center = self.body.position[0] * b2p , height - self.body.position[1] * b2p

# A class that creates a fireball
class FireBall(egs.Game_objects.drawupdateable):
    lifetime = 100
    images = []
    image_index = 0
    
    # Creates the fireball
    # Parameters:
    # Tuple pos is the position of the middle of the fireball
    # int direction is the position the fireball will shoot in.  Should be -1 or 1
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

        fire_rect = (36, 0, 34, 34)
        fire_image = piece_ss.image_at(fire_rect)
        self.images.append(fire_image)

        fire_rect = (72, 0, 34, 34)
        fire_image = piece_ss.image_at(fire_rect)
        self.images.append(fire_image)

        fire_rect = (108, 0, 34, 34)
        fire_image = piece_ss.image_at(fire_rect)
        self.images.append(fire_image)

        self.body = world.CreateDynamicBody(position=pos, fixedRotation = True)
        shape=b2PolygonShape(box=(p2b*16, p2b*16))
        fixDef = b2FixtureDef(shape=shape, friction=0.1, restitution=1, density=.8)
        box = self.body.CreateFixture(fixDef)
        self.rect = self.image.get_rect()
        self.body.ApplyForce(b2Vec2(self.direction * 50, 0), self.body.position, True)

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    #  Updates,checks to see if it collided with an enemy, and cycles the animation
    def update(self):
        global mario
        

        if self.lifetime % 10 == 0:
            self.image = self.images[self.image_index].convert_alpha()
            self.image_index = 0 if self.image_index == 3  else self.image_index + 1

        collidedWithEnemy = pygame.sprite.spritecollide(self, enemiesGroup, False)
        if len(collidedWithEnemy) > 0:
            self.kill()
            scene.updateables.remove(self)
            self.body.position = (-10.0, -10.0)
            self.rect.center = -100 * b2p, height - -100 * b2p
            pygame.mixer.Sound.play(music.kick_sound)
            collidedWithEnemy[0].set_dead()
            # TODO update the score

        if self.lifetime == 0:
            self.kill()
            if scene.updateables.__contains__(self):
                scene.updateables.remove(self)
            self.body.position = (-10.0, -10.0)
            self.rect.center = -100 * b2p, height - -100 * b2p

        self.lifetime -= 1
        self.rect.center = self.body.position[0] * b2p , height - self.body.position[1] * b2p

# A class that creates a fire flower
class FireFlower(egs.Game_objects.drawupdateable):
    # Creates the fire flower
    # Parameters:
    # Tuple pos is the position of the middle of the flower in meters
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

    # updates and checks if mario has collided
    def update(self):
        global mario
        collidedWithMario = pygame.sprite.spritecollide(self, marioGroup, False)
        
        if collidedWithMario:
            pygame.mixer.Sound.play(music.powerup_sound)
            self.kill()
            scene.updateables.remove(self)
            self.body.position = (-10.0, -10.0)
            self.rect.center = -100 * b2p, height - -100 * b2p
            mario.fire = True
            # TODO update the score

        self.rect.center = self.body.position[0] * b2p , height - self.body.position[1] * b2p

# A class that creates a mario that can throw fireballs
class FireMario(BaseMario):
    # Sets the initial state of the fire mario by specifying the size and the spritesheet
    def __init__(self, pos, immunity = 0):
        super().__init__(pos, immunity, size=(68,132),image_file='fireMario.png')

    # Updates FireMario by calling the super class
    def update(self):
        if(self.dead):
            return
        
        super().update()
        
    # Creates a new Mario object and replaces self with it when Fire Mario dies
    def die(self):
        global mario

        self.dead = True
        mario = Mario(self.body.position, 500)
        self.replace_mario(mario)

    # Shoots fire by creating fire objects
    def shoot_fire(self):
        pygame.mixer.Sound.play(music.fire_sound)
        if self.flipped:
            fireball = FireBall((self.body.position.x - .55, self.body.position.y + .46), -1)
        else:
            fireball = FireBall((self.body.position.x + .55, self.body.position.y + .46))
        fireGroup.add(fireball)
        scene.drawables.add(fireball)
        scene.updateables.append(fireball)

    # Converts FireMario to be invincible
    def convert_star(self):
        super().convert_star((self.rect.width, self.rect.height))

    # Converts FireMario from being invincible
    def convert_fromStar(self):
        super().convert_fromStar((self.rect.width, self.rect.height), True)

# A class for creating the end of level flag
class Flag(egs.Game_objects.drawupdateable):
    flag_sprites = []
    index = 0
    counter = 0
    sound_played = False
   
    # Creates a flag
    def __init__(self, pos):
        super().__init__()

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

    # Checks if mario has collided and animates the flag lowering
    def update(self):
        self.image = self.flag_sprites[self.index].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position[0] * b2p , height - self.body.position[1] * b2p


        collidedWithMario = pygame.sprite.spritecollide(self, marioGroup, False)
        
        if collidedWithMario and not self.sound_played:
            pygame.mixer.Sound.play(music.flagpole)
            self.sound_played = True

        if collidedWithMario:
            if self.counter == 5:
                self.counter = 0
                if self.index < 8:
                    self.index += 1
                elif self.index == 8:
                    mario.body.position = (self.body.position[0] + 1.28, mario.body.position[1])
                    mario.body.linearVelocity = (0,0)
            else:
                self.counter += 1
 
        self.rect.center = self.body.position[0] * b2p , height - self.body.position[1] * b2p

# A class that creates a goomba                 
class Goomba(egs.Game_objects.drawupdateable):
    goomba_sprites = []
    counter = 0
    current_index = 0
    force = -20
    last_center = None
    dead = False
    # Creates a goomba
    # Parameters:
    # Tuple pos is the starting position of the middle of the goomba in meters
    def __init__(self, pos):
        super().__init__()
        if os.name == 'nt':
            filename = "image\\enemies.png"
        else:
            filename = 'image/enemies.png'

        piece_ss = SpriteSheet(filename)
        for i in range (2):
            goomba_rect = (i*68, 0, 70, 70)
            goomba_image = piece_ss.image_at(goomba_rect)
            self.goomba_sprites.append(goomba_image)

        goomba_rect = (136, 0, 68, 68)
        self.goomba_dying = piece_ss.image_at(goomba_rect)

        self.body = world.CreateDynamicBody(position= pos, fixedRotation = True)
        shape = b2PolygonShape(box = (p2b* 32,p2b*32))
        fixDef = b2FixtureDef(shape=shape, friction = 0.3, restitution=0, density = 1)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        self.image = self.goomba_sprites[self.current_index % 2].convert_alpha()
        self.rect = self.image.get_rect()

    # Updates the goomba.  Checks if the goomba is dead, and moves if it's touching the ground
    def update(self):
        global mario
        if self.body.position.x - 16 > mario.body.position.x:
            self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p
            return
        if not self.body:
            return

        if self.dead and self.counter < 30:
            image = pygame.transform.scale(self.goomba_dying, (64, 64))
            self.image = image.convert_alpha()
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

        if self.body.position[0] <= 11.52:
            if self.rect.right > -2432:
                if self.counter == 15:
                    self.current_index = self.current_index + 1
                    self.counter = 0
                    self.image = self.goomba_sprites[self.current_index % 2].convert_alpha()
                    self.rect = self.image.get_rect()

                    self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

                    groundCollided = pygame.sprite.spritecollide(self, groundGroup, False)
                    if groundCollided:
                        for e in groundCollided:
                            if (e.rect.left + 2 > self.rect.right -2 or e.rect.right -2 < self.rect.left+2):
                                self.linearVelocity = (0,0)
                                self.force *= -1
                        self.body.ApplyForce(b2Vec2(self.force, 0), self.body.position, True)                
                else:
                    self.counter = self.counter + 1 
            else:
                self.kill()
                scene.updateables.remove(self)    
                self.body.position = (-10.0, -10.0)

        self.last_center = self.rect.center
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p
    
    # starts the process of the goomba dying
    def set_dead(self):
        self.body.active = False
        self.dead = True
        self.counter = 0
        enemiesGroup.remove(self)

# Creates the ground that mario walks on
class Ground(egs.Game_objects.drawable):

    # Creates the ground
    # Parameters:
    # float x is the position of the horizontal center of the ground in meters
    # float w is the width of the ground in meters
    # float y is the positition of the vertical center of the ground in meters
    # float h is the height of the ground in meters
    def __init__(self, x, w, y=.64, h= 1.28, underground = False):
        super().__init__()

        if underground:
            filename = os.path.join("image", "underGround.png")
        else:
            filename = os.path.join("image", "ground.png")

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

# Creates a kooopa
class Koopa(egs.Game_objects.drawupdateable):
    flipped = False
    koopa_walking = []
    current_koopa = 0
    counter = 0
    step_counter = 0
    dead = False

    # Creates a koopa
    # Parameters:
    # Tuple pos is the center of the koopa in meters
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

    # updates the koopa and moves when touching the ground
    def update(self):
        if self.dead:
            self.rect.center = -100 * b2p, height - -100 * b2p
            return
        if self.body.position[0] < 11.52:
            if self.counter == 30:
                self.image = self.koopa_walking[self.current_koopa].convert_alpha()
                self.current_koopa = (self.current_koopa + 1) % 2
                self.counter = 0
                if self.flipped:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.body.ApplyForce(b2Vec2(45, 0), self.body.position, True)
                    if self.step_counter == 15:
                        self.flipped = False
                        self.step_counter = 0
                    else:
                        self.step_counter = self.step_counter + 1
                else:
                    self.body.ApplyForce(b2Vec2(-45, 0), self.body.position, True)
                    if self.step_counter == 15:
                        self.flipped = True
                        self.step_counter = 0
                    else:
                        self.step_counter = self.step_counter + 1
            else:
                self.counter = self.counter + 1

        self.rect = self.image.get_rect()
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    # turns a koopa into a koopa shell
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

# Creates a Koopa Shell
class KoopaShell(egs.Game_objects.drawupdateable):
    counter = 0
    dead = False
    stationary = False

    # Creates a koopa shell
    # Parameters:
    # Tuple pos is the center of the koopa shell's starting position in meters
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
        fixDef = b2FixtureDef(shape=shape, friction=0.03, restitution= 0, density=1)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2

        self.image = self.koopa_shell.convert_alpha()
        self.rect = self.image.get_rect()

        self.previous_pos = self.rect.center

    # Updates the koopa shell and checks if it kills a goomba, or bounces off a block
    def update(self):
        if self.dead:
            self.rect.center = -100 * b2p, height - -100 * b2p
            return
        
        if self.previous_pos == self.rect.center:
            self.stationary = True
        else:
            self.stationary = False
        
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

        collidedWithGoomba = pygame.sprite.spritecollide(self, enemiesGroup, False)
        if collidedWithGoomba:
            for e in collidedWithGoomba:
                if type(e) == Goomba:
                    e.set_dead()
        
        collidedWithGround = pygame.sprite.spritecollide(self, groundGroup, False)
        if collidedWithGround:
            for e in collidedWithGround:
                if e.rect.right - 2 < self.rect.left + 2:
                    self.body.ApplyLinearImpulse(b2Vec2(1.75, 0), self.body.position, True)
                elif e.rect.left + 2 > self.rect.right - 2:
                    self.body.ApplyLinearImpulse(b2Vec2(-1.75, 0), self.body.position, True)

        self.counter += 1
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    # Function placed in order to call this on any enemy
    def set_dead(self):
        pass

# This class creates a small mario
class Mario(BaseMario):
    # Updates Mario, sets his dying animation if he's dying, then calls the superclass update
    def update(self):
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
            view.marioDead = True
            return
        
        if self.dead:
            return

        super().update()

    # This function will set the correct variables so that Mario's death animation will be run
    def die(self):
        pygame.mixer.Sound.play(music.mariodie_sound)
        pygame.mixer.music.stop()
        self.dead = True
        self.counter = 0
    
    # This is just a stub function so that the baseclass can call shoot fire on any mario, but has no functionality
    def shoot_fire(self):
        return

# This class creates a mushroom powerup
class Mushroom(egs.Game_objects.drawupdateable):
    # This class creates a new mushroom
    # Params
    # int tuple pos, the position at which the mushroom will appear
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

    # This function will check to see if a Mario has collided with the mushroom and update Mario accordingly.
    def update(self):
        global mario
        collidedWithMario = pygame.sprite.spritecollide(self, marioGroup, False)

        if collidedWithMario:
            pygame.mixer.Sound.play(music.powerup_sound)
            self.kill()
            scene.updateables.remove(self)
            self.body.position = (-10.0, -10.0)
            self.rect.center = -100 * b2p, height - -100 * b2p
            mario.mushroom = True
            # TODO update the score

        self.rect.center = self.body.position[0] * b2p , height - self.body.position[1] * b2p

# The class defines all of the sounds that will be used in the game
class Music():
    # Creates all of the sounds
    def __init__(self):
        mixer.init()

        s = 'sound'

        self.jump_small = pygame.mixer.Sound(os.path.join(s, 'smb_jump-small.wav'))
        self.jump_big = pygame.mixer.Sound(os.path.join(s, 'smb_jump-super.wav'))
        self.flagpole = pygame.mixer.Sound(os.path.join(s, 'smb_flagpole.wav'))
        self.fire_sound = pygame.mixer.Sound(os.path.join(s, 'smb_fireball.wav'))
        self.mariodie_sound = pygame.mixer.Sound(os.path.join(s, 'smb_mariodie.wav'))
        self.coin_sound = pygame.mixer.Sound(os.path.join(s,'smb_coin.wav'))
        self.brick_break_sound = pygame.mixer.Sound(os.path.join(s, 'smb_breakblock.wav'))
        self.powerup_sound = pygame.mixer.Sound(os.path.join(s, 'smb_powerup.wav'))
        self.powerup_appears_sound = pygame.mixer.Sound(os.path.join(s, 'smb_powerup_appears.wav'))
        self.stomp_sound = pygame.mixer.Sound(os.path.join(s, 'smb_stomp.wav'))
        self.kick_sound = pygame.mixer.Sound(os.path.join(s, 'smb_kick.wav'))
        self.level_finished_sound = pygame.mixer.Sound(os.path.join(s, 'smb_stage_clear.wav'))

        if os.name == 'nt':
            filename = "sound\\theme.mp3"
        else:
            filename = "sound/theme.mp3"
        mixer.music.load(filename)
        mixer.music.play()

# This class creates a new Star
class Star(egs.Game_objects.drawupdateable):
    # Initializes the star
    # Params
    # int tuple pos, the position at which the star will appear
    def __init__(self, pos):
        super().__init__()
        if os.name == 'nt':
            filename = "image\\star.png"
        else:
            filename = "image/star.png"

        piece_ss = SpriteSheet(filename)

        self.dirty = 2

        star_rect = (68, 0, 68, 68)
        ground_image = piece_ss.image_at(star_rect)
        self.image = ground_image.convert_alpha()
        self.body = world.CreateStaticBody(position = pos, shapes = b2PolygonShape(box = (p2b*32, p2b*32)))
        self.rect = self.image.get_rect()

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    # This class checks to see if the star has been collided with by Mario and then updates Mario accordingly
    def update(self):
        global mario
        collidedWithMario = pygame.sprite.spritecollide(self, marioGroup, False)
        
        if collidedWithMario:
            self.kill()
            scene.updateables.remove(self)
            self.body.position = (-10.0, -10.0)
            self.rect.center = -100 * b2p, height - -100 * b2p
            mario.star = True
            # TODO update the score

        self.rect.center = self.body.position[0] * b2p , height - self.body.position[1] * b2p

# This class creates a solid stone block, the ones that are in the stairs or a QuestionBlock after it is used
class SolidStone(egs.Game_objects.drawable):
    # This function will set the image for the SolidStone block based on whether it is a used QuestionBlock or a stairs block
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

# This class creates a super mario
class SuperMario(BaseMario):
    # Sets up a new mario with the correct size and sprite sheet
    def __init__(self, pos, immunity = 0):
        super().__init__(pos, immunity, size=(68,132), image_file='superMarioSprites.png')

    # Updates Mario
    def update(self):
        if(self.dead):
            return

        super().update()

    # Creates a new small Mario when SuperMario dies and replaces SuperMario with the small Mario
    def die(self):
        global mario

        self.dead = True
        mario = Mario(self.body.position, 500)
        self.replace_mario(mario)

    # Converts SuperMario to be invincible
    def convert_star(self):
        super().convert_star((self.rect.width, self.rect.height))

    # Converts SuperMario from being invincible
    def convert_fromStar(self):
        super().convert_fromStar((self.rect.width, self.rect.height))

    # This is just a stub function so that the baseclass can call shoot fire on any mario, but has no functionality
    def shoot_fire(self):
        return

# This class updates the QuestionBlock
class QuestionBlock(egs.Game_objects.drawupdateable):
    destroyed = False
    
    # Sets up the question block physics and image
    # Params
    # int tuple pos, the position of the block
    # boolean powerup, whether or not there is a powerup in the QuestionBlock
    # boolean invisible, whether or not the block is invisible
    def __init__(self, pos, powerup = False, invisible = False):
        super().__init__()

        filename = "image/tileset.png"

        piece_ss = SpriteSheet(filename)
        self.powerup = powerup

        self.dirty = 2

        if not invisible:
            brick_rect = (68, 0, 68, 68)
            ground_image = piece_ss.image_at(brick_rect)
            self.image = ground_image.convert_alpha()
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
            self.rect = pygame.Rect(pos[0], pos[1], 64, 64)

        self.body = world.CreateStaticBody(position = pos, shapes = b2PolygonShape(box = (p2b*32, p2b*32)))

        self.rect.center = self.body.position[0] * b2p, height - self.body.position[1] * b2p

    # This function checks to see if Mario has destroyed it, or releases a powerup or coin if it contains one
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
                        pygame.mixer.Sound.play(music.powerup_appears_sound)
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

# This class creates a new pipe
class Pipe(egs.Game_objects.drawable):
    # This class initializes the pipe
    # Params
    # int xpos is the horizontal position of the pipe, every pipe is on the ground 
    # int h is how tall the pipe will be
    def __init__(self, xpos, h, active = False, underground = False, teleport = (0.0, 0.0)):
        super().__init__()

        filename = os.path.join('image', 'pipes.png')
        piece_ss = SpriteSheet(filename)

        self.dirty = 2
        width_in_pixels = 128
        height_in_pixels = h * 64

        self.active = active
        self.underground = underground
        self.teleport_point = teleport
        
        if self.underground:
            pipe_rect = (396, 0, width_in_pixels + 4, height_in_pixels + 4)
        else:
            pipe_rect = ((h-2)*132, 0, width_in_pixels + 4, height_in_pixels + 4)

        ypos = 1.28 + (height_in_pixels * p2b / 2)

        pipe_image = piece_ss.image_at(pipe_rect)

        self.body = world.CreateStaticBody(position = (xpos, ypos) , shapes = b2PolygonShape(box = (.64, (h*.64)/2)))

        self.image = pipe_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2p, height - self.body.position.y * b2p

    # def update(self):
    #     if self.active:
    #         collided = pygame.sprite.spritecollide(self, marioGroup, False)

    #         if collided:
    #             for e in collided:
    #                 if self.underground and 
    #                 elif :


# This class updates Box2d
class Updater(egs.Game_objects.updateable):
    def __init__(self):
        super().__init__()

    def update(self):
        try:
            world.Step(timeStep, vec_iters, pos_iters)
            world.ClearForces()
        except:
            print("Oh no")

class WallPipe(egs.Game_objects.drawable):
    def __init__(self, pos):
        super().__init__()

        filename = os.path.join('image', 'underPipe.png')
        piece_ss = SpriteSheet(filename)

        self.dirty = 2
        
        pipe_rect = (0, 0, 68, 708)
        pipe_image = piece_ss.image_at(pipe_rect)

        self.body = world.CreateStaticBody(position = pos, shapes = b2PolygonShape(box = (.32,3.52)))

        self.image = pipe_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2p, height - self.body.position.y * b2p

# Creates all the ground that appears in the level
def createGround():
    grounds = []
    grounds.append(Ground(22.08,44.16))
    grounds.append(Ground(50.24,9.6))
    grounds.append(Ground(77.44, 40.96))
    grounds.append(Ground(117.12, 35.84))
    grounds.append(Ground(140.16, 10.24, underground = True))

    for e in grounds:
        groundGroup.add(e)
        scene.drawables.add(e)

# creates all the question blocks that appear in the level.  Includes the invisible block
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
    questions.append(QuestionBlock((41.28, 3.52), True, True))

    for item in questions:
        groundGroup.add(item)
        scene.drawables.add(item)
        scene.updateables.append(item)

# Creates all the bricks in level
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

    # Underground Bricks
    for i in range(3,14):
        bricks.append(Brick((135.36, (i * .64) - .32), underground = True))

    for e in bricks:
        groundGroup.add(e)
        scene.drawables.add(e)
        scene.updateables.append(e)

# creates all the pipes in the level
def createPipes():
    pipes = []
    pipes.append(Pipe(18.56, 2))
    pipes.append(Pipe(24.96, 3))
    pipes.append(Pipe(30.08, 4))
    pipes.append(Pipe(37.12, 4, True, teleport = (135.04, 7.68)))
    pipes.append(Pipe(104.96, 2))
    pipes.append(Pipe(115.20, 2))
    pipes.append(WallPipe((144.96, 4.8)))
    pipes.append(Pipe(144, 2, True, True, (104.32, 3.2)))
    for item in pipes:
        groundGroup.add(item)
        scene.drawables.add(item)

# creates all the solid stones in the level
def createSolids():
    solids = []

    # First Stairs
    solids.append(SolidStone((86.08, 1.60)))

    solids.append(SolidStone((86.72, 1.60)))
    solids.append(SolidStone((86.72, 2.24)))

    solids.append(SolidStone((87.36, 1.60)))
    solids.append(SolidStone((87.36, 2.24)))
    solids.append(SolidStone((87.36, 2.88)))

    solids.append(SolidStone((88.00, 1.60)))
    solids.append(SolidStone((88.00, 2.24)))
    solids.append(SolidStone((88.00, 2.88)))
    solids.append(SolidStone((88.00, 3.52)))

    solids.append(SolidStone((89.92, 1.60)))
    solids.append(SolidStone((89.92, 2.24)))
    solids.append(SolidStone((89.92, 2.88)))
    solids.append(SolidStone((89.92, 3.52)))

    # Second Stairs
    solids.append(SolidStone((90.56, 1.60)))
    solids.append(SolidStone((90.56, 2.24)))
    solids.append(SolidStone((90.56, 2.88)))

    solids.append(SolidStone((91.20, 1.60)))
    solids.append(SolidStone((91.20, 2.24)))

    solids.append(SolidStone((91.84, 1.60)))

    # Third Stairs
    solids.append(SolidStone((95.04, 1.60)))

    solids.append(SolidStone((95.68, 1.60)))
    solids.append(SolidStone((95.68, 2.24)))

    solids.append(SolidStone((96.32, 1.60)))
    solids.append(SolidStone((96.32, 2.24)))
    solids.append(SolidStone((96.32, 2.88)))

    solids.append(SolidStone((96.96, 1.60)))
    solids.append(SolidStone((96.96, 2.24)))
    solids.append(SolidStone((96.96, 2.88)))
    solids.append(SolidStone((96.96, 3.52)))

    solids.append(SolidStone((97.60, 1.60)))
    solids.append(SolidStone((97.60, 2.24)))
    solids.append(SolidStone((97.60, 2.88)))
    solids.append(SolidStone((97.60, 3.52)))

    # Fourth Stairs
    solids.append(SolidStone((99.52, 1.60)))
    solids.append(SolidStone((99.52, 2.24)))
    solids.append(SolidStone((99.52, 2.88)))
    solids.append(SolidStone((99.52, 3.52)))

    solids.append(SolidStone((100.16, 1.60)))
    solids.append(SolidStone((100.16, 2.24)))
    solids.append(SolidStone((100.16, 2.88)))

    solids.append(SolidStone((100.80, 1.60)))
    solids.append(SolidStone((100.80, 2.24)))

    solids.append(SolidStone((101.44, 1.60)))

    # Final Stairs
    solids.append(SolidStone((116.16, 1.60)))

    solids.append(SolidStone((116.80, 1.60)))
    solids.append(SolidStone((116.80, 2.24)))

    solids.append(SolidStone((117.44, 1.60)))
    solids.append(SolidStone((117.44, 2.24)))
    solids.append(SolidStone((117.44, 2.88)))

    solids.append(SolidStone((118.08, 1.60)))
    solids.append(SolidStone((118.08, 2.24)))
    solids.append(SolidStone((118.08, 2.88)))
    solids.append(SolidStone((118.08, 3.52)))

    solids.append(SolidStone((118.72, 1.60)))
    solids.append(SolidStone((118.72, 2.24)))
    solids.append(SolidStone((118.72, 2.88)))
    solids.append(SolidStone((118.72, 3.52)))
    solids.append(SolidStone((118.72, 4.16)))

    solids.append(SolidStone((119.36, 1.60)))
    solids.append(SolidStone((119.36, 2.24)))
    solids.append(SolidStone((119.36, 2.88)))
    solids.append(SolidStone((119.36, 3.52)))
    solids.append(SolidStone((119.36, 4.16)))
    solids.append(SolidStone((119.36, 4.80)))

    solids.append(SolidStone((120.00, 1.60)))
    solids.append(SolidStone((120.00, 2.24)))
    solids.append(SolidStone((120.00, 2.88)))
    solids.append(SolidStone((120.00, 3.52)))
    solids.append(SolidStone((120.00, 4.16)))
    solids.append(SolidStone((120.00, 4.80)))
    solids.append(SolidStone((120.00, 5.44)))

    solids.append(SolidStone((120.64, 1.60)))
    solids.append(SolidStone((120.64, 2.24)))
    solids.append(SolidStone((120.64, 2.88)))
    solids.append(SolidStone((120.64, 3.52)))
    solids.append(SolidStone((120.64, 4.16)))
    solids.append(SolidStone((120.64, 4.80)))
    solids.append(SolidStone((120.64, 5.44)))
    solids.append(SolidStone((120.64, 6.08)))

    solids.append(SolidStone((121.28, 1.60)))
    solids.append(SolidStone((121.28, 2.24)))
    solids.append(SolidStone((121.28, 2.88)))
    solids.append(SolidStone((121.28, 3.52)))
    solids.append(SolidStone((121.28, 4.16)))
    solids.append(SolidStone((121.28, 4.80)))
    solids.append(SolidStone((121.28, 5.44)))
    solids.append(SolidStone((121.28, 6.08)))

    for item in solids:
        groundGroup.add(item)
        scene.drawables.add(item)

# Creates all the enemies in the level
def createEnemies():
    enemies = []
    enemies.append(Goomba((14.4, 1.76)))
    enemies.append(Goomba((25.92, 1.76)))
    enemies.append(Goomba((32.96, 1.76)))
    enemies.append(Goomba((34.24, 1.76)))
    enemies.append(Goomba((51.52, 6.72)))
    enemies.append(Goomba((52.8, 6.72))) 
    enemies.append(Goomba((61.76, 1.76)))
    enemies.append(Goomba((63.04, 1.76)))
    enemies.append(Koopa((68.16, 1.76)))
    enemies.append(Goomba((72.0, 1.76)))
    enemies.append(Goomba((73.28, 1.76)))
    enemies.append(Goomba((78.4, 1.76)))
    enemies.append(Goomba((79.69, 1.76)))
    enemies.append(Goomba((80.96, 1.76)))
    enemies.append(Goomba((82.24, 1.76)))
    enemies.append(Goomba((111.04, 1.76)))
    enemies.append(Goomba((112.32, 1.76)))

    for enemy in enemies:
        enemiesGroup.add(enemy)
        scene.drawables.add(enemy)
        scene.updateables.append(enemy)

# Creates all the items in the level except for mario and camera
def create_level():
    background = Background()

    flag = Flag((126.72,4.8))
    castle = Castle((130.88, 2.88))

    scene.drawables.add(background)
    scene.drawables.add(castle)
    scene.drawables.add(flag)


    scene.updateables.append(Updater())
    scene.updateables.append(flag)
    scene.updateables.append(castle)

    createGround()
    createQuestions()
    createBricks()
    createPipes()
    createSolids()
    createEnemies()

width = 1024
height = 832
coin_count = 0
engine = egs.Engine("Mario 1-1", width = width, height = height)

scene = egs.Scene("Scene 1")
egs.Engine.current_scene = scene

music = Music()
view = Camera()

groundGroup = pygame.sprite.Group()
fireGroup = pygame.sprite.Group()
enemiesGroup = pygame.sprite.Group()
marioGroup = pygame.sprite.Group()

mario = Mario((1.92, 1.6))
create_level()

marioGroup.add(mario)
scene.drawables.add(mario)
scene.updateables.append(mario)

scene.updateables.append(view)

engine.start_game()
