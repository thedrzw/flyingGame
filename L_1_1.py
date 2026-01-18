import pygame

from H_levels import *
from H_imports import *

from H_UI import Fade
from H_save_data import load_save_data, save_game
from H_event_handler import event_handler

LEVEL_ID = '1-1'


def main(screen: pygame.Surface) -> str:

    save_data = load_save_data()

    clock = pygame.time.Clock()

    player = Player(80 * 60)
    hud = Hud(player.health, player.time_remaining)

    events: dict = None

    level_background, level_background_rect = import_sprite(r'level background dimmed.png', 5, True)
    font = AutoFont()

    fade_in, fade_out = Fade(20, 'in'), Fade(10, 'out')

    destination = '' #set this to a level id to fade the screen out and transition to the level corresponding to the id
    running = True #set this to False to instantly quit the game

    frames_elapsed = 0 #self-explanatory imo

    #level-specific code should probablyyyy go in between these two comments vvv
    frames_since_last_wall = 0
    wall_frequency = 3 * 60
    wall_gap = 400
    #level-specific code should probablyyyy go in between these two comments ^^^

    #game loop
    while running:
        
        frames_elapsed += 1
        seconds_elapsed = frames_elapsed / 60
        events = event_handler(pygame.event.get(), events)
        
        #level-specific code should probablyyyy go in between these two comments vvv
        frames_since_last_wall += 1
        if wall_frequency > 70:
            wall_frequency -= 0.03
        if wall_gap > 220:
            wall_gap -= 0.05

        if frames_since_last_wall >= wall_frequency and player.time_remaining > 3 * 60:
            Wall(-10, wall_gap)
            frames_since_last_wall = 0
        #level-specific code should probablyyyy go in between these two comments ^^^

        #update objects
        Everything.update(events)

        #check if the player has won/lost
        if player.time_remaining <= 0:
            destination = 'won'
        elif player.health <= 0:
            destination = 'lost'

        #draw to the screen
        screen.blit(level_background, level_background_rect)
        Everything.draw(screen)
        
        if events['quit']:
            running = False

        elif events['esc'][0]:
            destination = 'level_select'

        #do fade effects and check if the game should be running
        if not fade_in.completed:
            fade_in.update_and_draw(screen)
                
        elif destination != '':
            fade_out.update_and_draw(screen)
            if fade_out.completed is True:
                running = False
        
        #erm what the flip
        pygame.display.flip()

        #tick tock im the clock
        clock.tick(60)

    
    Everything.delete()

    if destination == 'won' and LEVEL_ID not in save_data['levels_completed']:
        save_data['levels_completed'].append(LEVEL_ID)

    save_game(save_data)

    return destination if destination != '' else None
