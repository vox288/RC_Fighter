
import pygame
import pygwidgets
import pyghelpers
from pygame.locals import *
from .Projectile import ProjectileMgr
from .Constants import *



class Player():
    animation_dict:dict = {"north":("resource/images/fighter/Fighter_straight_sheet.png",
                                 2, 100, 100, 0.1),
                      "west":("resource/images/fighter/Fighter_left-sheet.png",
                              2, 100, 100, 0.1),
                      "east":("resource/images/fighter/Fighter_right-sheet.png",
                               2, 100, 100, 0.1),
                      "north_attack":("resource/images/fighter/Fighter_straight_fire-sheet.png",
                                        3, 100, 100, 0.1),
                      "west_attack":("resource/images/fighter/Fighter_left_fire-sheet.png",
                                     3, 100, 100, 0.1),
                      "east_attack":("resource/images/fighter/Fighter_right_fire-sheet.png",
                                      3, 100, 100, 0.1),
                      "explode":("resource/images/fighter/Fighter_straight_explode1-sheet.png",
                                 5, 100, 100, 0.1),
                      "projectile":("resource/images/projectile/Projectile_fly3.png",
                                  3, 9, 20, 0.1 )}

    sound_dict:dict = {"north":"resource/sounds/fighter/fly_streight.wav",
                      "west":"resource/sounds/fighter/fly_left.wav",
                      "east":"resource/sounds/fighter/fly_right.wav",
                      "attack":"resource/sounds/fighter/gun_sound.mp3",
                      "got_hit":"resource/sounds/fighter/fighter_got_hit.wav",
                      "explode":"resource/sounds/fighter/fighter_explosion.mp3"}

    def __init__(self, window:pygame.surface, location:tuple[int,int]):
        self.window = window
        self.x, self.y = location
        self.lifes_left = 5
        self.speed = 15

        self.animation = pygwidgets.SpriteSheetAnimationCollection(
            self.window, (self.x, self.y), Player.animation_dict, "north",
            False, False, False)
        
        self.shoot_sound = pygame.mixer.Sound(Player.sound_dict["attack"])
        self.explode_sound = pygame.mixer.Sound(Player.sound_dict["explode"])
        self.got_hit_sound = pygame.mixer.Sound(Player.sound_dict["got_hit"])
        self.fly_sound = pygame.mixer.Sound(Player.sound_dict["north"])
        self.channel_2 = pygame.mixer.Channel(2)

        self.rect = pygame.Rect(self.x, self.y, 100, 100)
        self.mouse_button_pressed = False
        self.flying_state = "north"
        self.timer = pyghelpers.Timer(0.5)


    def get_lifes(self):
        return self.lifes_left
    

    def explode(self): 
        self.explode_sound.play()
        self.channel_2.stop()
        self.animation.replace("explode")
        

    def got_hit(self, projectile):
        collide_with_player = self.animation.getRect().colliderect(projectile)
        if collide_with_player:
            enemy_projectile_list.remove(projectile)
            self.got_hit_sound.play()
            self.lifes_left -= 1 
            if self.lifes_left == 0:
                self.explode()
                self.flying_state = "explode"
                self.timer.start()
            return True


    def shoot(self):
        self.shoot_sound.play()
        self.projectile_manager = ProjectileMgr(self.window)
        if self.flying_state == "east":
            self.projectile_manager.create_projectile("player",
                                                      (self.x + 43, self.y),
                                                      4)
        elif self.flying_state == "west":
            self.projectile_manager.create_projectile("player",
                                                      (self.x + 43, self.y),
                                                      -4)
        else:
            self.projectile_manager.create_projectile("player",
                                                      (self.x + 43, self.y))
        self.shot_fired = True


    def handleEvent(self, event):
        if self.flying_state == "explode":
            return
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_button_pressed = True
            self.shoot()


    def draw(self):
        self.animation.draw()

        
    def update(self):
        self.key_pressed = pygame.key.get_pressed()

        if self.flying_state != "explode":
            if self.mouse_button_pressed and self.key_pressed[K_a]:
                self.animation.replace("west_attack")
                if self.x < 0:
                    return
                self.x -= self.speed
                self.flying_state_switch("west")

            elif self.mouse_button_pressed and self.key_pressed[K_d]:
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

            elif self.mouse_button_pressed:
                self.animation.replace("north_attack")

            else:
                self.animation.replace("north")
                self.flying_state_switch("north")

            for projectile in enemy_projectile_list:
                self.got_hit(projectile.getRect())

            self.mouse_button_pressed = False
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
        self.fly_sound = pygame.mixer.Sound(Player.sound_dict[state])
        self.channel_2.play(self.fly_sound, -1)
        self.flying_state = state
        print(self.flying_state)