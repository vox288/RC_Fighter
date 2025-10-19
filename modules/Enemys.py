import pygame
import pygwidgets
import pyghelpers
import random
from abc import ABC, abstractmethod
from pygame.locals import *
from .Projectile import ProjectileMgr
from .Constants import *



class EnemyMgr():
    def __init__(self, window:pygame.surface):
        self.window = window
        self.timer = pyghelpers.Timer(0.1)

    
    def create_enemy(self, enemy_type:str, location:tuple[int,int]):
        if enemy_type == "bee":
            enemy = Bee(self.window, location)
            enemy_list.append(enemy)
        if enemy_type == "dragonfly":
            enemy = Dragonfly(self.window, location)
            enemy_list.append(enemy)
        if enemy_type == "bat":
            enemy = Bat(self.window, location)
            enemy_list.append(enemy)


    def update(self):
        for enemy in enemy_list:
            enemy.update()
            enemy.shoot()
            enemy.special_shoot()
        self.check_hits()


    def check_hits(self):
        for enemy in enemy_list:
            for projectile in player_projectile_list:
                if enemy.got_hit(projectile.getRect()):
                    player_projectile_list.remove(projectile)


    def draw(self):
        for enemy in enemy_list:
            enemy.draw()



class Enemy(ABC):
    
    def __init__(self, window:pygame.surface, location:tuple[int,int],
                 enemy_type:str, animation_dict:dict, sound_dict:dict,
                 width:int, height:int, lifes:int):
        self.window = window
        self.x, self.y = location
        self.width, self.height = width, height
        self.enemy_type = enemy_type
        self.animation_dict = animation_dict
        self.sound_dict = sound_dict
        self.lifes_left = lifes


        self.animation = pygwidgets.SpriteSheetAnimationCollection(
            self.window, (self.x, self.y), self.animation_dict, "north",
            False, False)

        self.explode_sound = pygame.mixer.Sound(self.sound_dict["explode"])
        self.shoot_sound = pygame.mixer.Sound(self.sound_dict["attack"])
        self.timer = pyghelpers.Timer(0.4)
        self.projectile_manager = ProjectileMgr(self.window)


    def get_type(self):
        return self.enemy_type
    

    def play_fly_sound(self, channel):
        self.fly_sound = pygame.mixer.Sound(self.sound_dict["north"])
        self.channel = pygame.mixer.Channel(channel)
        self.channel.play(self.fly_sound, -1)


    def get_lifes_left(self):
        return self.lifes_left
    

    def update(self):
        self.animation.update()
        self.animation.play()
        self.move()
        self.animation.setLoc((self.x, self.y))
        if self.timer.update():
            enemy_list.remove(self)


    def draw(self):
        self.animation.draw()


    def explode(self):
        self.timer.start()
        self.animation.replace("explode")
        self.explode_sound.play()
        

    def got_hit(self, projectile):
        collide_with_target = self.animation.getRect().colliderect(projectile)
        if collide_with_target:
            self.lifes_left -= 1 
            if self.lifes_left <= 0:
                self.explode()
            return True
        

    def special_shoot(self):
        return
    

    @abstractmethod
    def move(self):
        raise NotImplementedError


    @abstractmethod
    def shoot(self):
        raise NotImplementedError



class Bee(Enemy):
    def __init__(self, window:pygame.surface, location:tuple[int,int]):
        enemy_type = "bee"
        animation_dict = {"north":("resource/images/Bee/Bee_fly1.png",
                                   4, 100, 100, 0.1),
                          "explode":("resource/images/Bee/Bee_explode.png",
                                     4, 100, 100, 0.1),}
        sound_dict = {"north":"resource/sounds/Bee/Bee_north.wav",
                      "attack":"resource/sounds/Bee/splat2.wav",
                      "explode":"resource/sounds/Bee/slime.mp3"}
        width = 100
        height = 100
        lifes_left = 1

        super().__init__(window, location, enemy_type, animation_dict,
                        sound_dict, width, height, lifes_left)
        
        self.movement_frame_counter = random.randrange(5, 30)
        self.speed_y = random.randrange(-8, 8)
        self.speed_x = random.randrange(-15, 15)
        self.shoot_timer = pyghelpers.Timer(random.randrange(2, 20) / 10)
        self.shoot_timer.start()


    def shoot(self): 
        if self.shoot_timer.update():
            self.shoot_sound.play()
            self.projectile_manager.create_projectile(self.enemy_type,
                                        (self.x + (self.width/2),
                                         self.y + self.height),
                                         random.randrange(-2,2))
            self.shoot_timer = pyghelpers.Timer(random.randrange(2, 20) / 10)
            self.shoot_timer.start()
        

    def move(self):
        self.movement_frame_counter -= 1
        self.x += self.speed_x
        self.y += self.speed_y
        if self.movement_frame_counter <= 0:
            self.movement_frame_counter = random.randrange(5, 30)
            self.speed_y = random.randrange(-5, 5)
            self.speed_x = random.randrange(-10, 10)
        if self.x < 0 or self.x > WINDOW_WIDTH - self.width:
            self.speed_x = -self.speed_x
        if self.y < 0 or self.y > WINDOW_HEIGHT - (self.height*3):
            self.speed_y = - self.speed_y
        


class Dragonfly(Enemy):
    def __init__(self, window:pygame.surface, location:tuple[int,int]):
        enemy_type = "dragonfly"
        animation_dict = {"north" : ("resource/images/Dragonfly/Dragonfly_fly.png",
                                   4, 200, 150, 0.1),
                          "explode" : ("resource/images/Dragonfly/Dragonfly_explode.png",
                                   4, 200, 150, 0.1)}
        
        sound_dict = {"north" : "resource/sounds/Dragonfly/Bee_north.wav",
                      "explode" : "resource/sounds/Dragonfly/space_insect.mp3",
                      "attack" : "resource/sounds/Dragonfly/splat.wav"}
        width = 200
        height = 150
        lifes_left = 3

        super().__init__(window, location, enemy_type, animation_dict, sound_dict,
                         width, height, lifes_left)
        
        self.movement_frame_counter = random.randrange(5, 15)
        self.speed_y = random.randrange(-3, 3)
        self.speed_x = random.randrange(-35, 35)
        self.shoot_timer = pyghelpers.Timer(random.randrange(10, 30) / 10)
        self.shoot_timer.start()

        
    def shoot(self):
        if self.shoot_timer.update():
            self.shoot_sound.play()
            self.projectile_manager.create_projectile(self.enemy_type,
                                        (self.x + (self.width/2),
                                         self.y + self.height))
            self.shoot_timer = pyghelpers.Timer(random.randrange(2, 20) / 10)
            self.shoot_timer.start()
    
    def move(self):
        self.movement_frame_counter -= 1
        self.x += self.speed_x
        self.y += self.speed_y
        if self.movement_frame_counter <= 0:
            self.movement_frame_counter = random.randrange(5, 30)
            self.speed_y = random.randrange(-5, 5)
            self.speed_x = random.randrange(-10, 10)
        if self.x < 0 or self.x > WINDOW_WIDTH - self.width:
            self.speed_x = -self.speed_x
        if self.y < 0 or self.y > WINDOW_HEIGHT - (self.height*3):
            self.speed_y = - self.speed_y



class Bat(Enemy):
    def __init__(self, window:pygame.surface, location:tuple[int,int]):

        enemy_type = "bat"
        animation_dict = {"north":("resource/images/bat/bat_sprite.png",
                                   4, 350, 200, 0.1),
                          "explode":("resource/images/bat/bat_explode.png",
                                     8, 350, 200, 0.1),}
        sound_dict = {"north":"resource/sounds/bat/bat_fly.wav",
                      "attack":"resource/sounds/bat/bat_attack2.wav",
                      "attack_2":"resource/sounds/bat/bat_attack1.wav",
                      "explode":"resource/sounds/bat/bat_explode.wav"}
        width = 350
        height = 200
        lifes_left = 30

        super().__init__(window, location, enemy_type, animation_dict,
                        sound_dict, width, height, lifes_left)
        
        self.movement_frame_counter = random.randrange(5, 30)
        self.speed_y = 1
        self.speed_x = random.randrange(-10, 10)
        self.shoot_timer = pyghelpers.Timer(random.randrange(2, 20) / 10)
        self.shoot_timer.start()
        self.special_shoot_timer = pyghelpers.Timer(random.randrange(20,60) / 10)
        self.special_shoot_timer.start()
        self.special_shoot_sound = pygame.mixer.Sound(self.sound_dict["attack_2"])


    def shoot(self): 
        if self.shoot_timer.update():
            self.shoot_sound.play()
            self.projectile_manager.create_projectile(self.enemy_type,
                                        (self.x + (self.width/2),
                                         self.y + self.height))
            self.shoot_timer = pyghelpers.Timer(random.randrange(2, 20) / 10)
            self.shoot_timer.start()
        
        
    def special_shoot(self):
        if self.special_shoot_timer.update():
            self.special_shoot_sound.play()
            for pixel in range(-20, 21, 10):  # Range used to create 5 spreading projectiles
                self.projectile_manager.create_projectile("dragonfly",
                                        (self.x + (self.width/2),
                                        self.y + self.height),
                                        side_movement=pixel)
            self.special_shoot_timer = pyghelpers.Timer(random.randrange(20,60) / 10)
            self.special_shoot_timer.start()


    def move(self):
        self.movement_frame_counter -= 1
        self.x += self.speed_x
        self.y += self.speed_y
        if self.movement_frame_counter <= 0:
            self.movement_frame_counter = random.randrange(5, 30)
            self.speed_y = random.randrange(-5, 5)
            self.speed_x = random.randrange(-10, 10)
        if self.x < 0 or self.x > WINDOW_WIDTH - self.width:
            self.speed_x = -self.speed_x
        if self.y < 0 or self.y > WINDOW_HEIGHT - (self.height*3):
            self.speed_y = - self.speed_y