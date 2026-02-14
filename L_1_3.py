import pygame

from H_levels import *
from H_imports import *

from H_UI import Fade
from H_save_data import load_save_data, save_game
from H_event_handler import event_handler

LEVEL_ID = '1-3'


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
    Enemy(20, Shooter.SP_normal, 0, 0, {'run_distance': 300, 'follow_distance': 600})

    previous_wall_center_y = constants['PLAYABLE_HEIGHT'] / 2
    frames_since_last_wall = 0
    last_wall_came_from = 'left'
    wall_speed = 10
    wall_frequency = 1.5 * 60
    #level-specific code should probablyyyy go in between these two comments ^^^

    #game loop
    while running:
        
        frames_elapsed += 1
        seconds_elapsed = frames_elapsed / 60
        events = event_handler(pygame.event.get(), events)
        
        #level-specific code should probablyyyy go in between these two comments vvv
        # wall_speed = 10
        # wall_frequency = 20
        # player.health = 100
        # last_wall_came_from = 'left'

        frames_since_last_wall += 1
        if wall_frequency > 40:
            wall_frequency -= 0.01

        if wall_speed < 13:
            wall_speed += 0.003

        if frames_since_last_wall >= wall_frequency and player.time_remaining > 3 * 60:
            #i have no idea if this is the best way to do this but whatever tbh
            if last_wall_came_from == 'left':
                previous_wall_center_y = Wall.wall_based_on_previous(previous_wall_center_y, 70, 200, - wall_speed, 300).center_y

                last_wall_came_from = 'right'

            elif last_wall_came_from == 'right':
                previous_wall_center_y = Wall.wall_based_on_previous(previous_wall_center_y, 70, 200, wall_speed, 300).center_y

                last_wall_came_from = 'left'

            frames_since_last_wall = 0

        if player.time_remaining < 2 * 60:
            for enemy in Enemy.all:
                enemy.delete = True
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
