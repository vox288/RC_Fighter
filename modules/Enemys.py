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
        self.deletion_timer = pyghelpers.Timer(0.1)
        self.fly_sound_dict = {
                        "bee":"resource/sounds/Bee/Bee_north.wav",
                        "dragonfly":"resource/sounds/Dragonfly/Bee_north.wav",
                        "bat":"resource/sounds/Bat/bat_fly.wav"}
        self.bee_counter = 0
        self.dragonfly_counter = 0
        self.bat_counter = 0

    
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
            if enemy.get_type() == "bee":
                self.bee_counter += 1
            if enemy.get_type() == "dragonfly":
                    self.dragonfly_counter += 1
            if enemy.get_type() == "bat":
                self.bat_counter += 1
        self.check_hits()
        self.play_fly_sound()
        self.bee_counter = 0
        self.dragonfly_counter = 0
        self.bat_counter = 0


    def check_hits(self):
        for enemy in enemy_list:
            for projectile in player_projectile_list:
                if enemy.got_hit(projectile.getRect()):
                    player_projectile_list.remove(projectile)


    def play_fly_sound(self):
            self.enemy_fly_sound("bee", 3, self.bee_counter)
            self.enemy_fly_sound("dragonfly", 4, self.dragonfly_counter)
            self.enemy_fly_sound("bat", 5, self.bat_counter)


    def enemy_fly_sound(self, type:str, channel:int, counter:int):
            fly_sound_channel = pygame.mixer.Channel(channel)
            if counter == 0 or not enemy_list:
                fly_sound_channel.fadeout(1000)
                return
            if fly_sound_channel.get_busy():
                return
            fly_sound = pygame.mixer.Sound(self.fly_sound_dict[type])
            fly_sound_channel.play(fly_sound, 1)


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
        self.explode_channel = pygame.mixer.Channel(6)
        self.shoot_sound = pygame.mixer.Sound(self.sound_dict["attack"])
        self.shoot_channel = pygame.mixer.Channel(7)
        self.deletion_timer = pyghelpers.Timer(0.4)
        self.projectile_manager = ProjectileMgr(self.window)


    def get_type(self):
        return self.enemy_type


    def get_lifes_left(self):
        return self.lifes_left
    

    def update(self):
        self.animation.update()
        self.animation.play()
        self.move()
        self.animation.setLoc((self.x, self.y))
        if self.deletion_timer.update():
            enemy_list.remove(self)


    def draw(self):
        self.animation.draw()


    def explode(self):
        self.deletion_timer.start()
        self.animation.replace("explode")
        self.explode_channel.play(self.explode_sound)


    def got_hit(self, projectile):
        collide_with_target = self.animation.getRect().colliderect(projectile)
        if collide_with_target:
            self.lifes_left -= 1 
            if self.lifes_left == 0:
                self.explode()
            return True
        

    @abstractmethod
    def special_shoot(self):
        raise NotImplementedError
    

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
        sound_dict = {"attack":"resource/sounds/Bee/splat2.wav",
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
            self.shoot_channel.play(self.shoot_sound)
            self.projectile_manager.create_projectile(self.enemy_type,
                                        (self.x + (self.width/2),
                                         self.y + self.height),
                                         random.randrange(-2,2))
            self.shoot_timer = pyghelpers.Timer(random.randrange(2, 20) / 10)
            self.shoot_timer.start()


    def special_shoot(self):
        return
    

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
        
        sound_dict = {"explode" : "resource/sounds/Dragonfly/space_insect.mp3",
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
            self.shoot_channel.play(self.shoot_sound)
            self.projectile_manager.create_projectile(self.enemy_type,
                                        (self.x + (self.width/2),
                                         self.y + self.height))
            self.shoot_timer = pyghelpers.Timer(random.randrange(2, 20) / 10)
            self.shoot_timer.start()


    def special_shoot(self):
        return
    

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
        animation_dict = {"north":("resource/images/Bat/bat_sprite.png",
                                   4, 350, 200, 0.1),
                          "explode":("resource/images/Bat/bat_explode.png",
                                     8, 350, 200, 0.1),}
        sound_dict = {"attack":"resource/sounds/Bat/bat_attack2.wav",
                      "attack_2":"resource/sounds/Bat/bat_attack1.wav",
                      "explode":"resource/sounds/Bat/bat_explode.wav",
                      "spawn":"resource/sounds/Bat/bat_spawn.wav"}
        width = 350
        height = 200
        lifes_left = 30

        super().__init__(window, location, enemy_type, animation_dict,
                        sound_dict, width, height, lifes_left)
        
        self.movement_frame_counter = random.randrange(5, 30)
        self.speed_y = random.randrange(-5, 5)
        self.speed_x = random.randrange(-15, 15)
        self.shoot_timer = pyghelpers.Timer(random.randrange(2, 20) / 10)
        self.shoot_timer.start()
        self.special_shoot_timer = pyghelpers.Timer(random.randrange(20,60) / 10)
        self.special_shoot_timer.start()
        self.special_shoot_sound = pygame.mixer.Sound(self.sound_dict["attack_2"])
        self.spawn_sound = pygame.mixer.Sound(self.sound_dict["spawn"])
        self.shoot_channel.play(self.spawn_sound)

    def shoot(self): 
        if self.shoot_timer.update():
            self.shoot_channel.play(self.shoot_sound)
            self.projectile_manager.create_projectile(self.enemy_type,
                                        (self.x + (self.width/2),
                                         self.y + self.height))
            self.shoot_timer = pyghelpers.Timer(random.randrange(2, 20) / 10)
            self.shoot_timer.start()
        
        
    def special_shoot(self):
        if self.special_shoot_timer.update():
            self.shoot_channel.play(self.special_shoot_sound)
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