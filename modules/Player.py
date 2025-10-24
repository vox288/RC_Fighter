
import pygame
import pygwidgets
import pyghelpers
import random
from pygame.locals import *
from .Projectile import ProjectileMgr
from .Constants import *



class Player():
    animation_dict:dict = {"north":(resolve_path("resource/images/Fighter/Fighter_straight_sheet.png"),
                                 2, 100, 100, 0.1),
                      "west":(resolve_path("resource/images/Fighter/Fighter_left-sheet.png"),
                              2, 100, 100, 0.1),
                      "east":(resolve_path("resource/images/Fighter/Fighter_right-sheet.png"),
                               2, 100, 100, 0.1),
                      "north_attack":(resolve_path("resource/images/Fighter/Fighter_straight_fire-sheet.png"),
                                        3, 100, 100, 0.1),
                      "west_attack":(resolve_path("resource/images/Fighter/Fighter_left_fire-sheet.png"),
                                     3, 100, 100, 0.1),
                      "east_attack":(resolve_path("resource/images/Fighter/Fighter_right_fire-sheet.png"),
                                      3, 100, 100, 0.1),
                      "explode":(resolve_path("resource/images/Fighter/Fighter_straight_explode1-sheet.png"),
                                 5, 100, 100, 0.1)}

    sound_dict:dict = {"north":resolve_path("resource/sounds/Fighter/fly_streight.wav"),
                      "west":resolve_path("resource/sounds/Fighter/fly_left.wav"),
                      "east":resolve_path("resource/sounds/Fighter/fly_right.wav"),
                      "attack":resolve_path("resource/sounds/Fighter/gun_sound.mp3"),
                      "explode":resolve_path("resource/sounds/Fighter/fighter_explosion.mp3")}
    
    got_hit_sounds = (resolve_path("resource/sounds/impact/fighter_got_hit1.wav"),
                      resolve_path("resource/sounds/impact/fighter_got_hit2.wav"),
                      resolve_path("resource/sounds/impact/fighter_got_hit3.wav"))

    def __init__(self, window:pygame.surface, location:tuple[int,int]):
        self.window = window
        self.x, self.y = location
        self.lifes_left = 5
        self.speed = 15
        self.shots_fired = 0

        self.animation = pygwidgets.SpriteSheetAnimationCollection(
            self.window, (self.x, self.y), Player.animation_dict, "north",
            False, False, False)
        
        self.player_fly_sound = pygame.mixer.Sound(Player.sound_dict["north"])
        self.player_shoot_sound = pygame.mixer.Sound(Player.sound_dict["attack"])
        self.player_explode_sound = pygame.mixer.Sound(Player.sound_dict["explode"])
        self.player_channel_fly = pygame.mixer.Channel(0)
        self.player_channel_shoot = pygame.mixer.Channel(1)
        self.player_channel_explode = pygame.mixer.Channel(1)
        self.player_channel_got_hit = pygame.mixer.Channel(2)

        self.rect = pygame.Rect(self.x, self.y, 100, 100)
        self.attack_button_pressed = False
        self.flying_state = "north"
        self.timer = pyghelpers.Timer(0.5)


    def get_lifes(self):
        return self.lifes_left
    
    
    def get_shots_fired(self):
        return self.shots_fired
    

    def explode(self): 
        self.player_channel_explode.play(self.player_explode_sound)
        self.player_channel_fly.stop()
        self.animation.replace("explode")
        

    def got_hit(self, projectile):
        collide_with_player = self.animation.getRect().colliderect(projectile)
        if collide_with_player:
            enemy_projectile_list.remove(projectile)
            self.player_got_hit_sound = pygame.mixer.Sound(random.choice(Player.got_hit_sounds))
            self.player_channel_got_hit.play(self.player_got_hit_sound)
            self.lifes_left -= 1 
            if self.lifes_left == 0:
                self.explode()
                self.flying_state = "explode"
                self.timer.start()
            return True


    def shoot(self):
        self.shots_fired += 1
        self.player_channel_shoot.play(self.player_shoot_sound)
        self.projectile_manager = ProjectileMgr(self.window)
        if self.flying_state == "east":
            self.projectile_manager.create_projectile("player",
                                                      (self.x + 43, self.y),
                                                      5)
        elif self.flying_state == "west":
            self.projectile_manager.create_projectile("player",
                                                      (self.x + 43, self.y),
                                                      -5)
        else:
            self.projectile_manager.create_projectile("player",
                                                      (self.x + 43, self.y))



    def handleEvent(self, event):
        if self.flying_state == "explode":
            return
        elif event.type == pygame.MOUSEBUTTONDOWN\
            or self.key_pressed[K_RETURN]:
            self.attack_button_pressed = True
            self.shoot()
    

    def draw(self):
        self.animation.draw()

        
    def update(self):
        self.key_pressed = pygame.key.get_pressed()

        if self.flying_state != "explode":
            if self.attack_button_pressed and self.key_pressed[K_a]:
                self.animation.replace("west_attack")
                if self.x < 0:
                    return
                self.x -= self.speed
                self.flying_state_switch("west")

            elif self.attack_button_pressed and self.key_pressed[K_d]:
                self.animation.replace("east_attack")
                if self.x > WINDOW_WIDTH - 100:
                    return
                self.x += self.speed
                self.flying_state_switch("east")

            elif self.key_pressed[pygame.K_a]:
                if self.x < 0:
                    return
                self.x -= self.speed
                self.animation.replace("west")
                self.flying_state_switch("west")

            elif self.key_pressed[pygame.K_d]:
                if self.x > WINDOW_WIDTH - 100:
                    return
                self.x += self.speed
                self.animation.replace("east")
                self.flying_state_switch("east")

            elif self.attack_button_pressed:
                self.animation.replace("north_attack")

            else:
                self.animation.replace("north")
                self.flying_state_switch("north")

            for projectile in enemy_projectile_list:
                self.got_hit(projectile.getRect())

            self.attack_button_pressed = False
            self.animation.setLoc((self.x, self.y))
            self.animation.update()
            self.animation.start()
      
           
        
        elif self.flying_state == "explode":
            self.animation.update()
            if self.timer.update():
                self.animation.stop()
                self.animation.hide()
                pygame.mixer.music.stop()

        
    def flying_state_switch(self, state:str):
        if self.flying_state == state:
            return
        self.player_fly_sound = pygame.mixer.Sound(Player.sound_dict[state])
        self.player_channel_fly.play(self.player_fly_sound, -1)
        self.flying_state = state