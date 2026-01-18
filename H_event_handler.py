#for keys like 'W' or '2':
#the first boolean is True ONLY on the FIRST frame it is pressed
#the second boolean is True the ENTIRE time is is pressed
import pygame

key_names = {
    'esc': pygame.K_ESCAPE,

    'w': pygame.K_w,
    'a': pygame.K_a,
    'd': pygame.K_d,

    '1': pygame.K_1,
    '2': pygame.K_2,
    '3': pygame.K_3,

    's': pygame.K_s,
    'k': pygame.K_k,
    'i': pygame.K_i,
    'b': pygame.K_b,
    'd': pygame.K_d,
}

key_ids = {v: k for k, v in key_names.items()} #same as key_names but the key value pairs are swapped

mouse_button_names = {
    'mouse1': pygame.BUTTON_LEFT,
    'mouse2': pygame.BUTTON_RIGHT,
}

mouse_button_ids = {v: k for k, v in mouse_button_names.items()}

def event_handler(events: list[pygame.event.Event], events_dict: dict | None) -> dict:
    #if there is no events dictionary yet, create one!
    #puts [False, False] for the value of every key
    if events_dict == None:
        events_dict = {'quit': False}

        for key in key_names:
            events_dict[key] = [False, False]

        for button in mouse_button_names:
            events_dict[button] = [False, False]

        events_dict['mouse_pos'] = (0, 0)


    #set the first boolean in each key/mouse button to False
    for key in key_names:
        events_dict[key][0] = False
    for button in mouse_button_names:
        events_dict[button][0] = False


    #go through every event and update the event dict accordingly
    for event in events:
        clicked_quit = (event.type == pygame.QUIT)
        keydown = (event.type == pygame.KEYDOWN)
        keyup = (event.type == pygame.KEYUP)
        mousedown = (event.type == pygame.MOUSEBUTTONDOWN)
        mouseup = (event.type == pygame.MOUSEBUTTONUP)
        mouse_moved = (event.type == pygame.MOUSEMOTION)
        

        if clicked_quit:
            events_dict['quit'] = True
        
        elif keydown or keyup:
            #check if the event matches any of the ids in keys and update events_dict if so
            if event.key in key_ids:
                if keydown:
                    events_dict[key_ids[event.key]] = [True, True]
                
                elif keyup:
                    events_dict[key_ids[event.key]] = [False, False]

        elif mousedown or mouseup:
            if event.button in mouse_button_ids:
                if mousedown:
                    events_dict[mouse_button_ids[event.button]] = [True, True]
                
                elif mouseup:
                    events_dict[mouse_button_ids[event.button]] = [False, False]

        elif mouse_moved:
            events_dict['mouse_pos'] = event.pos
            
    
    return events_dict


# def check_if_running(events_dict: dict):
#     return (events_dict['quit'] and not events_dict['esc'][0])