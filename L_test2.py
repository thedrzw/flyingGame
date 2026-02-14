'jeremy is the best i love him so so much 😘😘😘😘'

import pygame

from H_levels import *
from H_event_handler import *
from H_imports import *
from H_UI import Fade
from H_save_data import *

LEVEL_ID = 'test level 2'

def main(screen: pygame.Surface) -> str:

    save_data = load_save_data()

    fade_in, fade_out = Fade(20, 'in'), Fade(20, 'out')
    destination = '' #assigning this variable will cause the level to fade, quit and go to the screen with the id in the variable

    font = AutoFont()
    clock = pygame.time.Clock()

    player = Player(60 * 60)
    hud = Hud(player.health, player.time_remaining)

    events: dict = None

    frames_elapsed = 0
    
    skibidi_text, skibidi_text_rect = render_text(font[25], '')
    debug_text, debug_text_rect = render_text(font[25], '')

    skibidi_letters = 'skibd'
    skibidi_queue = ''

    level_background, level_background_rect = import_sprite(r'level background dimmed.png', 5, True)

    running = True

    #Shooter(500, 500, 10, Shooter.SP_normal)

    #game loop
    while running:
        frames_elapsed += 1

        events = event_handler(pygame.event.get(), events)

        
        for letter in skibidi_letters:
            if events[letter][0] == True:
                skibidi_queue += letter
            
                if len(skibidi_queue) > 7:
                    skibidi_queue = skibidi_queue[(len(skibidi_queue) - 7):]

                skibidi_text, skibidi_text_rect = render_text(font[25], skibidi_queue)
        
        debug_info = f'fps: {round(clock.get_fps())}\n'
        # debug_info += f'{player.rect = }\n{player.x, player.y, player.width, player.height = }\n{player.health = }\n'
        # debug_info += f'{len(Wall.all) = }\n'
        # debug_info += f'{len(Projectile.all) = }\n'
        # debug_info += f'{len(Shooter.all) = }\n'
        # debug_info += f'{len(Enemy.all) = }\n'

        if frames_elapsed % 5 == 0:
            debug_text, debug_text_rect = render_text(font[25], debug_info)
        
        if player.health <= 0 or player.time_remaining <= 0 or events['esc'][0]:
            destination = 'won'

        if frames_elapsed % (1.5 * 60) == 0:
            #Projectile(500, 500, player.x, player.y, 10)
            Wall(random.randrange(1, 15))#, Shooter())
            # Enemy(20, Shooter.SP_normal, random.randrange(1000, 1500), random.randrange(100, 500), Enemy.chase_settings)
            # Enemy(20, Shooter.SP_normal, random.randrange(1000, 1500), random.randrange(100, 500), Enemy.run_settings)

        if events['k'][0] == True:
            Enemy(20, Shooter.SP_normal, random.randrange(1000, 1500), random.randrange(100, 500), Enemy.run_settings)

        

        #update ----
        Everything.update(events)

        #draw ----
        screen.fill(BLACK)
        screen.blit(level_background, level_background_rect)

        Everything.draw(screen)

        screen.blit(debug_text, debug_text_rect)

        if not fade_in.completed:
            fade_in.update_and_draw(screen)
                
        elif destination != '':
            fade_out.update_and_draw(screen)
            if fade_out.completed is True:
                running = False
        
        if events['quit']:
            running = False

        pygame.display.flip()

        #tick tock im the clock
        clock.tick(60)

    
    Everything.delete()


    if destination == 'won' and LEVEL_ID not in save_data['levels_completed']:
        save_data['levels_completed'].append(LEVEL_ID)

    save_game(save_data)

    return destination if destination != '' else None
