

import pygame
import pygwidgets
import pyghelpers
from .Player import Player
from .Enemys import *
from .Projectile import *
from .Constants import *



class PlayScene(pyghelpers.Scene):

    animation_dict = {"normal":("resource/images/play_background.png",
                                40, 1024, 680, 0.1),
                      "dark":("resource/images/play_background_dark.png",
                                40, 1024, 680, 0.1),
                      "transition" : ("resource/images/transition.png",
                                40, 1024, 680, 0.03)}

    def __init__(self, window:pygame.surface):
        self.window = window
        self.background_animation = pygwidgets.SpriteSheetAnimationCollection(
                                self.window, (0, 0), PlayScene.animation_dict,
                                "normal")
        self.frame_image = pygwidgets.Image(self.window, (0,0), 
                                    "resource/images/Frame.png")
        self.player = Player(self.window, (450, 570))
        self.enemy_manager = EnemyMgr(self.window)
        self.projectile_manager = ProjectileMgr(self.window)
        self.lifes_title = pygwidgets.DisplayText(self.window, (10, 300),
                                                  "Lifes Left :",
                                                  textColor=WHITE)
        self.lifes_display = pygwidgets.DisplayText(self.window,
                                                    (10, WINDOW_HEIGHT/2),
                                                    self.player.get_lifes(),
                                                    fontSize=46,
                                                    textColor=WHITE)
        self.gameover_display = pygwidgets.DisplayText(self.window,
                                                       (90, 200), "GAME OVER",
                                                       fontSize=200, 
                                                       textColor=WHITE)
        self.gameover_hint = pygwidgets.DisplayText(self.window, (350, 350),
                                        "Press Mousebutton to return to the Menu",
                                        fontSize=22, textColor=WHITE)
        self.enemy_row = 0
    

        self.timer = pyghelpers.Timer(1.5)
        self.timer.start()
        self.endgame_timer = pyghelpers.Timer(0.5)


    def reset(self):
        self.gameover_display.hide()
        self.gameover_hint.hide()
        self.enemy_row = 0
        enemy_projectile_list.clear()
        player_projectile_list.clear()
        enemy_list.clear()
        self.background_animation.replace("normal")
        self.timer.start()
        self.player = Player(self.window, (450, 570))


    def handleInputs(self, events, keyPressedList):
        for event in events:
           if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.handleEvent(event)
                if self.player.get_lifes() <= 0:
                    self.endgame_timer.start()


    def check_enemy_list(self):
        if len(enemy_list) <= 0:
            self.enemy_row += 1
            self.timer.start()
        return


    def draw(self):
        self.background_animation.draw()
        self.frame_image.draw()
        self.lifes_display.draw()
        self.lifes_title.draw()
        self.player.draw()
        self.enemy_manager.draw()
        self.projectile_manager.draw()
        if self.player.get_lifes() <= 0:
            self.gameover_display.show()
            self.gameover_display.draw()
            self.gameover_hint.show()
            self.gameover_hint.draw()


    def update(self):
        self.background_animation.update()
        self.background_animation.start()
        self.player.update()
        self.enemy_manager.update()
        self.projectile_manager.update()
        self.lifes_display.setValue(self.player.get_lifes())
        if self.endgame_timer.update():
            self.goToScene(MENU_SCENE)
            self.reset()

        if self.enemy_row == 0:
            if self.timer.update():
                self.first_row()

        if self.enemy_row == 1:
            self.check_enemy_list()
               
        if self.enemy_row == 2:
            if self.timer.update():
                self.second_row()

        if self.enemy_row == 3:
            self.check_enemy_list()

        if self.enemy_row == 4:
            if self.timer.update():
                self.third_row()
        
        if self.enemy_row == 5:
            self.check_enemy_list()

        if self.enemy_row == 6:
            if self.timer.update():
                self.fourth_row()

        if self.enemy_row == 7:
            self.check_enemy_list()

        if self.enemy_row == 8:
            self.background_animation.replace("transition")
            self.timer.start(1.2)
            self.enemy_row += 1
        
        if self.enemy_row == 9:
            if self.timer.update():
                self.background_animation.replace("dark")
                self.timer.start(3)
                self.enemy_row += 1
        
        if self.enemy_row == 10:
            if self.timer.update():
                self.boss_row()

                       
    def getSceneKey(self):
        return PLAY_SCENE
    
    
    def first_row(self):
        for _ in range(3):
            self.enemy_manager.create_enemy("bee", (random.randrange(50,800),
                      random.randrange(50,300)))
        self.enemy_row += 1
            

    def second_row(self):
        for _ in range(5):
            self.enemy_manager.create_enemy("bee", (random.randrange(50,800),
                      random.randrange(50,300)))
        for _ in range(1):
            self.enemy_manager.create_enemy("dragonfly", 
                      (random.randrange(50, 800), random.randrange(50, 300)))
        self.enemy_row += 1


    def third_row(self):
        for _ in range(3):
            self.enemy_manager.create_enemy("bee", (random.randrange(50,800),
                      random.randrange(50,300)))
        for _ in range(5):
            self.enemy_manager.create_enemy("dragonfly", 
                      (random.randrange(50, 800), random.randrange(50, 300)))
        self.enemy_row += 1


    def fourth_row(self):
        for _ in range(10):
            self.enemy_manager.create_enemy("dragonfly", 
                      (random.randrange(50, 800), random.randrange(50, 300)))
        self.enemy_row += 1


    def boss_row(self):
        self.enemy_manager.create_enemy("bat", (350, 150))
        
