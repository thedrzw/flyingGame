import pygame

#wildcard imports my beloved
from H_constants import *
from H_imports import *
from H_UI import *
from H_save_data import *

#TODO: put all resource-intensive functions calls and stuff that can be done asynchronously outside of the main function
#actually on second thought i can just put everything but the game loop outside
def main(screen: pygame.Surface):
    save_data = load_save_data()

    fade_in = Fade(20, 'in')
    fade_out = Fade(20, 'out')
    fading_in = True
    fading_out = False

    #clock
    clock = pygame.time.Clock()
    

    background, background_rect = import_sprite(r'level select background.png', 10, True, (0, 0))
    
    level_title, level_title_rect = import_sprite(r'level title.png', 5, True)
    #print(level_title.get_size())
    level_selected_glow = import_sprite(r'level selected glow.png', 5)

    empty_star = import_sprite(r'empty star.png', 5)
    filled_star, star_rect = import_sprite(r'filled star.png', 5, True)

    text_box, text_box_rect = import_sprite('text box.png', 5, True, (constants['SCREEN_WIDTH'] - 750, 150))

    chapter_title, chapter_title_rect = import_sprite('chapter 1.png', 10, True, (150, 120))
    #print(chapter_title.get_size())
    font = import_font_sizes(None, (25, 50, 75, 100, 125, 150, 175, 200))


    class LevelIcon(InteractableUIObject):

        all = []
        switch_screen = ''

        def __init__(self, section = 0, number = 0, description = 'placeholder'):

            super().__init__(pygame.Rect(150, 300 + ((number % 5) * 120), level_title_rect.width, level_title_rect.height), level_title)

            self.section = section
            self.number = number
            self.name = f'{section + 1}-{number + 1}'
            self.description = description

            if self.number > 4:
                self.rect.x += 480 + 30
                self.update_coordinates()

            self.description_text, self.description_text_rect = render_text(font[50], description, text_box_rect, padding = (20, 10))

            self.selected = False

            
            self.background_rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
            #TODO: refactor all this to make it use the render_text() function from the imports module

            self.text, self.text_rect = render_text(font[50], self.name, self.rect, padding = (30, 5))

            self.star_rect = pygame.Rect(self.x_pos + 300, self.y_pos + 10, star_rect.width, star_rect.height)

            if self.name in save_data['levels_completed']:
                self.star_sprite = filled_star
            else:
                self.star_sprite = empty_star

        def glow_and_text(self):
            screen.blit(level_selected_glow, self.rect)

            screen.blit(self.description_text, self.description_text_rect)

        def update(self):
            self.update_hovering_and_clicked(mouse_position, mouse_clicked)

            if self.clicked:
                LevelIcon.switch_screen = self.name

        def draw(self):
            #background to each level icon
            screen.blit(self.sprite, self.rect)

            #text on each level icon
            screen.blit(self.text, self.text_rect)

            #star on each level icon
            screen.blit(self.star_sprite, self.star_rect)

            #"level selected" display
            if self.hovering:
                self.glow_and_text()

    LevelIcon(0, 0, 'only in ohio epic test please please work i really hope that this works')
    LevelIcon(0, 1)
    LevelIcon(0, 2)
    LevelIcon(0, 3)
    LevelIcon(0, 4)

    LevelIcon(0, 5)
    LevelIcon(0, 6)
    LevelIcon(0, 7)
    LevelIcon(0, 8)
    LevelIcon(0, 9)

    index_selected = 0

    running = True
    return_value = None

    holding_up = False
    holding_down = False

    mouse_clicked = False


    while running or fading_out:
        #event handler ----
        mouse_clicked = False
        holding_down = False
        holding_up = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                elif event.key == pygame.K_1:
                    running = False
                    return_value = 'skill_tree'
                    fading_out = True
                
                elif event.key == pygame.K_DOWN:
                    holding_down = True

                elif event.key == pygame.K_UP:
                    holding_up = True
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
        
        mouse_position = pygame.mouse.get_pos()
        

        #calculations and stuff ----
        LevelIcon.update_all()

        if LevelIcon.switch_screen:
            running = False
            return_value = LevelIcon.switch_screen
            fading_out = True
        
        #draw to the screen ----
        screen.blit(background, background_rect)
        screen.blit(chapter_title, chapter_title_rect)

        screen.blit(text_box, text_box_rect)

        LevelIcon.draw_all()

        if fading_in:
            fade_in.update_and_draw(screen)
            if fade_in.completed:
                fading_in = False

        elif fading_out:
            fade_out.update_and_draw(screen)
            if fade_out.completed:
                fading_out = False

        # pygame.draw.rect(screen, WHITE, pygame.Rect(150, 300, 450, 80))
        # pygame.draw.rect(screen, WHITE, pygame.Rect(150 + 480 + 30, 300, 450, 80))
        # pygame.draw.rect(screen, YELLOW, chapter_title_rect)

        pygame.display.flip()
        clock.tick(60)


    
    save_game(save_data)
    return return_value