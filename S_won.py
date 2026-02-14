import pygame

from H_levels import *
from H_event_handler import *
from H_imports import *
from H_UI import Fade

def main(screen: pygame.Surface) -> str:

    clock = pygame.time.Clock()

    events: dict = None

    background, background_rect = import_sprite(r'win background.png', 10, True)
    title, title_rect = import_sprite('win title.png', 10, True, ('center', 120))

    font = import_font_sizes(None, (25, 50, 75, 100))

    press_key_text, press_key_text_rect = render_text(font[75], 'Click to return to the level select screen!', pygame.Rect(0, 850, 9999, 0 ))
    press_key_text_rect.x = (constants['SCREEN_WIDTH'] / 2) - (press_key_text_rect.width / 2)

    rewards_text_box, rewards_text_box_rect = import_sprite('level complete text box.png', 5, True, ((constants['SCREEN_WIDTH'] / 2) - (1200 / 2), 300))

    fade_in, fade_out = Fade(20, 'in'), Fade(20, 'out')

    destination = '' #set this to a level id to fade the screen out and transition to the level corresponding to the id
    running = True #set this to False to instantly quit the game

    frames_elapsed = 0 #self-explanatory imo

    #game loop
    while running:
        frames_elapsed += 1
        events = event_handler(pygame.event.get(), events)


        #update objects
        if events['esc'][0]:
            destination = 'level_select'

        #draw to the screen
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        screen.blit(title, title_rect)
        screen.blit(press_key_text, press_key_text_rect)
        screen.blit(rewards_text_box, rewards_text_box_rect)

        #do fade effects and check if the game should be running
        if not fade_in.completed:
            fade_in.update_and_draw(screen)
                
        elif destination != '':
            fade_out.update_and_draw(screen)
            if fade_out.completed is True:
                running = False
        
        if events['quit']:
            running = False

        #erm what the flip
        pygame.display.flip()

        #tick tock im the clock
        clock.tick(60)

    
    return destination if destination != '' else None