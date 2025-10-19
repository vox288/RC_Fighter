
import pygame
import pygwidgets
from abc import ABC, abstractmethod
from pygame.locals import *
from .Constants import *


class ProjectileMgr():
    def __init__(self, window:pygame.surface):

        self.window = window

    
    def create_projectile(self, projectile_type:str, location:tuple[int,int],
                          side_movement:int=0):
        if projectile_type == "player":
            player_projectile = PlayerProjectile(self.window, location,
                                                 side_movement)
            player_projectile_list.append(player_projectile)

        elif projectile_type == "bee":
            bee_projectile = BeeProjectile(self.window, location,
                                           side_movement)
            enemy_projectile_list.append(bee_projectile)

        elif projectile_type == "dragonfly":
            dragonfly_projectile = DragonflyProjectile(self.window, location,
                                                       side_movement)
            enemy_projectile_list.append(dragonfly_projectile)

        elif projectile_type == "bat":
            dragonfly_projectile = BatProjectile(self.window, location,
                                                 side_movement)
            enemy_projectile_list.append(dragonfly_projectile)


    def draw(self):
        for enemy_projectile in enemy_projectile_list:
            enemy_projectile.draw()
        for player_projectile in player_projectile_list:
            player_projectile.draw()


    def update(self):
        for enemy_projectile in enemy_projectile_list:
            if enemy_projectile.update():
                enemy_projectile_list.remove(enemy_projectile)
        for player_projectile in player_projectile_list:
            if player_projectile.update():
                player_projectile_list.remove(player_projectile)


class Projectile(ABC):
    def __init__(self, window:pygame.surface, location:tuple[int,int],
                 animation_dict:dict, side_movement:int=0):
        
        self.window = window
        self.x, self.y = location
        self.animation_dict = animation_dict
        self.side_movement = side_movement

        self.animation = pygwidgets.SpriteSheetAnimationCollection(self.window,
                                    (self.x, self.y), self.animation_dict,
                                    "projectile", True, True)

    def draw(self):
        self.animation.draw()
     
        
    def getRect(self):
        return self.animation.getRect() 
    

    @abstractmethod
    def update(self):
        raise NotImplementedError
    


class PlayerProjectile(Projectile):
    def __init__(self, window:pygame.surface, location:tuple[int,int],
                 side_movement:int=0):

        self.animation_dict = {"projectile": 
                        ("resource/images/projectile/Projectile_fly3.png",
                         3, 9, 20, 0.1)}
        self.speed = 17

        super().__init__(window, location, self.animation_dict, side_movement)
    

    def update(self):
        self.y -= self.speed
        self.x += self.side_movement
        self.animation.setLoc((self.x, self.y))
        self.animation.update()
        self.rect = self.animation.getRect()
        if self.rect[1] < 0:
            return True
        


class BeeProjectile(Projectile):
    def __init__(self, window:pygame.surface, location:tuple[int,int],
                 side_movement:int=0):

        self.animation_dict = {"projectile":
                ("resource/images/enemy_projectiles/Bee_projectile.png",
                3, 9, 20, 0.1)}
        self.speed = 6

        super().__init__(window, location, self.animation_dict, side_movement)
    

    def update(self):
        self.y += self.speed
        self.x += self.side_movement
        self.animation.setLoc((self.x, self.y))
        self.animation.update()
        self.rect = self.animation.getRect()
        if self.rect[1] > WINDOW_HEIGHT:
            return True
        
    
class DragonflyProjectile(Projectile):
    def __init__(self, window:pygame.surface, location:tuple[int,int],
                 side_movement:int=0):

        self.animation_dict = {"projectile":
                ("resource/images/enemy_projectiles/Dragonfly_projectile.png",
                 3, 15, 30, 0.1)}
        self.speed = 12

        super().__init__(window, location, self.animation_dict, side_movement)


    def update(self):
        self.y += self.speed
        self.x += self.side_movement
        self.animation.setLoc((self.x, self.y))
        self.animation.update()
        self.rect = self.animation.getRect()
        if self.rect[1] > WINDOW_HEIGHT:
            return True
        

class BatProjectile(Projectile):
    def __init__(self, window:pygame.surface, location:tuple[int,int],
                 side_movement:int=0):

        self.animation_dict = {"projectile" : 
                ("resource/images/enemy_projectiles/Bat_projectile.png",
                 3, 50, 50, 0.1)}
        self.speed = 10

        super().__init__(window, location, self.animation_dict, side_movement)

    def update(self):
        self.y += self.speed
        self.x += self.side_movement
        self.animation.setLoc((self.x, self.y))
        self.animation.update()
        self.rect = self.animation.getRect()
        if self.rect[1] > WINDOW_HEIGHT:
            return True