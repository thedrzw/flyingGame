import pygame
import time

from H_constants import *
from H_imports import *
from H_UI import *
from H_save_data import *
from H_colors import *

def main(screen: pygame.Surface):
    save_data = load_save_data()

    fade_in = Fade(20, 'in')
    fade_out = Fade(20, 'out')
    fading_in = True
    fading_out = False


    #clock
    clock = pygame.time.Clock()

    #font
    font = import_font_sizes(None, (25, 50, 75, 100, 125, 150, 175, 200))

    #import sprites
    background, background_rect = import_sprite('skill tree background.png', 10, True, (0, 0))

    title, title_rect = import_sprite('the tree.png', 10, True, (150, 120))

    skill_tree_circle, skill_tree_circle_rect = import_sprite('skill tree circle.png', 10, True)
    bought_skill_tree_circle = import_sprite('gold skill tree circle.png', 10)
    skill_tree_circle_glow = import_sprite('skill tree circle selected glow.png', 10)

    among_us, among_us_rect = import_sprite('amogus.png', 5, True)

    text_box, text_box_rect = import_sprite('text box.png', 5, True, (constants['SCREEN_WIDTH'] - 750, 150))

    money_background, money_background_rect = import_sprite('money display.png', 5, True, (constants['SCREEN_WIDTH'] - 500, constants['SCREEN_HEIGHT'] - 125))


    class MoneyDisplay(UIObject):
        
        def __init__(self):

            self.money_amount = None

            self.rect = pygame.Rect(100, 100, 500, 100)

        
        def update(self):
            if self.money_amount != save_data['money']:
                self.money_amount = save_data['money']

                self.sprite, _ = render_text(font[50], f'money: {self.money_amount}', self.rect)

        def draw(self):
            screen.blit(self.sprite, self.rect)
                

    class TreeElement(InteractableUIObject):

        all = []

        def __init__(self, position: tuple[int, int], requirements, cost, name, description = 'placeholder'):
            
            super().__init__(pygame.Rect(position[0], position[1], skill_tree_circle_rect.width, skill_tree_circle_rect.height), skill_tree_circle)
 
            self.requirements = requirements
            self.name = name
            self.description = description
            self.cost = cost

            self.middle_x_pos, self.middle_y_pos = self.x_pos + self.width / 2, self.y_pos + self.height / 2

            self.name_text, self.name_text_rect = render_text(font[100], self.name, text_box_rect, padding = (20, 10))


            self.description_text, self.description_text_rect = render_text(font[50], self.description, text_box_rect, (20, 200), line_spacing = 50)

            self.bought = False

            self.image_rect = pygame.Rect(self.x_pos + skill_tree_circle_rect.width / 12, self.y_pos + skill_tree_circle_rect.height / 12, among_us_rect.width, among_us_rect.height)


        def check_and_buy(self):
            if self.clicked and not self.bought:
                if save_data['money'] >= self.cost:
                    save_data['money'] -= self.cost
                    self.bought = True

        def glow_and_text(self):
            screen.blit(skill_tree_circle_glow, self.rect) #glow around the circle
                
            screen.blit(self.name_text, self.name_text_rect) #text on the right
            screen.blit(self.description_text, self.description_text_rect)


        def update(self):
            self.update_hovering_and_clicked(mouse_position, mouse_clicked)

            self.check_and_buy()

        def draw_lines(self):
            for requirement in self.requirements:
                pygame.draw.line(screen, BLACK, (self.middle_x_pos, self.middle_y_pos), (requirement.middle_x_pos, requirement.middle_y_pos), 5)


        def draw(self):
            if self.bought:
                self.sprite = bought_skill_tree_circle
            else:
                self.sprite = skill_tree_circle
            
            screen.blit(self.sprite, self.rect)

            screen.blit(among_us, self.image_rect)

            if self.hovering:
                self.glow_and_text()


        @classmethod
        def draw_all(cls):
            for instance in cls.all:
                instance.draw_lines()
            
            super().draw_all()


    node1 = TreeElement((250, 250), [], 300, 'Sus 1', 'be 25% more sussy and get a 50% lower chance of being voted out of the ship the quick brown fox jumped over the lazy river ahhhhhhhhh please add line breaks')
    node2 = TreeElement((500, 500), [node1], 300, 'Sus 2', r'doubles the effect of Sus 1')

    money_display = MoneyDisplay()

    running = True
    return_value = None
    mouse_clicked = False

    #game loop
    while running or fading_out:
        #event handler ----
        mouse_clicked = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
                elif event.key == pygame.K_1:
                    running = False
                    return_value = 'level_select'
                    fading_out = True
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
            else:
                mouse_clicked = False
        
        mouse_position = pygame.mouse.get_pos()


        #calculations and stuff ----
        TreeElement.update_all()
        money_display.update()

        
        #draw stuff ----
        screen.blit(background, background_rect)
        screen.blit(title, title_rect)
        screen.blit(text_box, text_box_rect)
        screen.blit(money_background, money_background_rect) #lmao this looks like shit rn
        #pygame.draw.rect(screen, YELLOW, pygame.Rect(constants['SCREEN_WIDTH'] - 500, constants['SCREEN_HEIGHT'] - 125, 500, 125))

        money_display.draw()

        TreeElement.draw_all()

        if fading_in:
            fade_in.update_and_draw(screen)
            if fade_in.completed == True:
                fading_in = False

        elif fading_out:
            fade_out.update_and_draw(screen)
            if fade_out.completed == True:
                fading_out = False

        pygame.display.flip()
        clock.tick(60)

    
    save_game(save_data)
    return return_value