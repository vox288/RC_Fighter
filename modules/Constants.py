
import sys
import os
from pathlib import Path

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
    relative_path = Path(relative_path)
    try:
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(__file__).parent.parent

    return os.path.join(base_path, relative_path)


# pyinstaller build : pyinstaller RC_Fighter.py --onefile --clean --windowed --add-data="./resource:resource"