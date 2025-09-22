
# 1 - Import packages
import sys
import pygame
from pygame.locals import *

# 2 - Define constants
BLACK = (0,0,0)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# 4 - Load assets: Images, sounds, etc

# 5 - Initialize variables

# 6 - Infinite loop
while True:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        # Clicked the close button?
        if event.type == pygame.QUIT:
            sys.exit()

    # 8 - Do any per frame actions

    # 9 - Clear the window
    window.fill(BLACK)

    # 10 - Draw all window elements

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit Framerate
    clock.tick(FRAMES_PER_SECOND)