
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
                                    resolve_path("resource/images/waves.png"),
                                    30, 1024, 680, 0.05, True, True)
        self.frame_image = pygwidgets.Image(self.window, (0,0), 
                                    resolve_path("resource/images/Frame.png"))
        self.title_image = pygwidgets.Image(self.window, (170, 80),
                                    resolve_path("resource/images/Title.png"))
        self.controls_hint = pygwidgets.DisplayText(self.window, (270, 320),
                                    """[ Press A and D to fly left and right ]\n
                                        [ Press Return or Mousebutton to fire !]""", 
                                      textColor=WHITE, fontSize=25)
        self.quit_button = pygwidgets.TextButton(self.window, (350, 500),
                                                 "Quit", 100,)
        self.start_button = pygwidgets.TextButton(self.window, (550, 500),
                                                  "Start Game", 100)
        
        pygame.mixer.music.load(resolve_path("resource/sounds/background.wav"))


    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.start_button.handleEvent(event):
                pygame.mixer.Sound(resolve_path("resource/sounds/button.wav")).play()
                pygame.mouse.set_visible(False)
                self.goToScene(PLAY_SCENE)
                
                
            if self.quit_button.handleEvent(event):
                sys.exit()
                pygame.quit()


    def draw(self):
        self.background_animation.draw()
        self.frame_image.draw()
        self.title_image.draw()
        self.controls_hint.draw()
        self.quit_button.draw()
        self.start_button.draw()
    

    def update(self):
        self.background_animation.update()
        if pygame.mixer.music.get_busy():
            return
        pygame.mixer.music.play(-1)

        
    def getSceneKey(self):
        return MENU_SCENE