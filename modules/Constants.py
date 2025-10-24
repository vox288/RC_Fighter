
import sys
import os

MENU_SCENE = "menu"
PLAY_SCENE = "play"

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 80, 0)
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 680
FRAMES_PER_SECOND = 30

enemy_projectile_list = []
player_projectile_list = []
enemy_list = []


def resolve_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)