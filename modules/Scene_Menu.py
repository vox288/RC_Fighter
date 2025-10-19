
import sys
import pygame
import pygwidgets
import pyghelpers
from .Constants import *



class MenuScene(pyghelpers.Scene):
    def __init__(self, window:pygame.surface):
        self.window = window
        self.background_animation = pygwidgets.SpriteSheetAnimation(
                                    self.window, (0, 0),
                                    "resource/images/waves.png",
                                    30, 1024, 680, 0.05, True, True)
        self.frame_image = pygwidgets.Image(self.window, (0,0), 
                                    "resource/images/Frame.png")
        self.title_image = pygwidgets.Image(self.window, (170, 80),
                                    "resource/images/Title.png")
        self.quit_button = pygwidgets.TextButton(self.window, (350, 500),
                                                 "Quit", 100,)
        self.start_button = pygwidgets.TextButton(self.window, (550, 500),
                                                  "Start Game", 100)
        
        pygame.mixer.music.load("resource/sounds/background.mp3")
        pygame.mixer.music.play(-1)


    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.start_button.handleEvent(event):
                self.goToScene(PLAY_SCENE)
                
            if self.quit_button.handleEvent(event):
                sys.exit()
                pygame.quit()


    def draw(self):
        self.background_animation.draw()
        self.frame_image.draw()
        self.title_image.draw()
        self.quit_button.draw()
        self.start_button.draw()
    

    def update(self):
        self.background_animation.update()

        
    def getSceneKey(self):
        return MENU_SCENE