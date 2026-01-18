import time
start_time = time.time()

import pygame
import gc

from typing import Callable

#screens
import S_level_select, S_skill_tree
import S_won

#levels
import L_1_1, L_1_2, L_1_3
import L_test, L_test2, L_template

#random helper files
from H_constants import constants
from H_log import log


#create screen
screen = pygame.display.set_mode((constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT']), flags = pygame.SCALED | pygame.FULLSCREEN, vsync = 1)

#set the name of the window
pygame.display.set_caption('💀\U0001f480')

#initialize pygame
pygame.init()

#log load time
log(f'took {round(time.time() - start_time, 2)} seconds to load')

#screen switcher
files: dict[str, Callable[[pygame.Surface], str]] = { #honestly i think the type annotations make this more confusing lmfao
    'level_select': S_level_select.main,
    'skill_tree': S_skill_tree.main,
    
    '1-1': L_1_1.main,
    '1-2': L_1_2.main,
    '1-3': L_1_3.main,

    '1-8': L_template.main,
    '1-9': L_test.main,
    '1-10': L_test2.main,

    'won': S_won.main,
}

next_screen = 'level_select'

while True:
    
    if next_screen in files:    
        next_screen = files[next_screen](screen)

    elif next_screen == None:
        break

    else:
        raise Exception(f"you probably shouldn't be getting to this part of the code... (the value of 'next_screen' was '{next_screen}')")

    gc.collect()


pygame.quit()

