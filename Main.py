

import pygame
from pyghelpers import SceneMgr
from pygame.locals import *
from modules.Scene_Menu import MenuScene
from modules.Scene_Play import PlayScene
from modules.Constants import *


if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("RC Fighter")


    scene_dict:dict = {"menu":MenuScene(window),
                       "play":PlayScene(window)}

    scene_manager:SceneMgr = SceneMgr(scene_dict, FRAMES_PER_SECOND)

    scene_manager.run()