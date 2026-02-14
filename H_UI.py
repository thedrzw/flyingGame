import pygame
from H_constants import constants



class UIObject:

    def __init__(self, rect: pygame.Rect, sprite: pygame.Surface):

        try:
            self.add_to_all(self)
        except AttributeError:
            pass
        
        self.rect = rect
        self.sprite = sprite

        self.x_pos, self.y_pos = self.rect.topleft
        self.width, self.height = self.rect.size

    def update_coordinates(self):
        self.x_pos, self.y_pos = self.rect.topleft
        self.width, self.height = self.rect.size

    @classmethod
    def add_to_all(cls, self):
        cls.all.append(self)

    def update(self):
        raise NotImplementedError('the original "update" method of UIObject is being called (which does nothing)\nyou need to redefine this method or not call it')
        #🤓☝️ erm actually you're supposed to use the abstract base class module to create a method like this 🤓🤓🤓 like shut yo skibidi ass up
        #srsly though i don't know what the point of abstract methods are if you can just do this
        #also this class still could work by itself so idk whats going on

    def draw(self):
        raise NotImplementedError('the original "draw" method of UIObject is being called (which does nothing)\nyou need to redefine this method or not call it')
    

    @classmethod
    def update_all(cls):
        if not hasattr(cls, 'all'): #raise an error if there's no class variable named "all"
            raise NotImplementedError('you need to define a class variable named "all" in the class that inherits from UIObject\neg "all = []"')
        
        for instance in cls.all:
            instance.update()

    @classmethod
    def draw_all(cls):
        if not hasattr(cls, 'all'):
            raise NotImplementedError('you need to define a class variable named "all" in the class that inherits from UIObject\neg "all = []"')
        
        for instance in cls.all:
            instance.draw()



class InteractableUIObject(UIObject):

    def __init__(self, rect: pygame.Rect, sprite: pygame.Surface):
        super().__init__(rect, sprite)

        self.hovering = False
        self.clicked = False
    
    def update_hovering_and_clicked(self, mouse_position: tuple[int, int], mouse_clicked: bool):
        if not self.rect.collidepoint(mouse_position):
            self.hovering = False
            return
        
        self.hovering = True

        if not mouse_clicked:
            self.clicked = False
            return
        
        self.clicked = True



class Fade():
    "setting 'fade_direction' to 'in' makes it start at fully black and become more transparent over time\n\nsetting it to 'out' does the opposite"

    def __init__(self, fade_speed: float | int = 1, fade_direction: str = 'out') -> None:

        self.fade_speed = fade_speed

        if self.fade_speed <= 0:
            raise TypeError("'fade_speed' needs to be above 0")

        self.fade_direction = fade_direction

        if fade_direction == 'in':
            self.alpha_value = 255
            self.fade_speed = - self.fade_speed
        elif fade_direction == 'out':
            self.alpha_value = 0
        else:
            raise TypeError("'fade_direction' needs to be either 'in' or 'out'")
        
        self.fade_overlay = pygame.Surface([constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT']], flags=pygame.SRCALPHA)

        self.completed = False
        
    def update_and_draw(self, screen: pygame.Surface):
        #update
        if not self.completed:
            self.alpha_value += self.fade_speed

            if self.alpha_value >= 255:
                self.completed = True
                self.alpha_value = 255

            elif self.alpha_value <= 0:
                self.completed = True
                self.alpha_value = 0

            self.fade_overlay.fill((0, 0, 0, self.alpha_value))

        #draw
        screen.blit(self.fade_overlay, [0, 0])



#this would have been cool but it just doesn't work lmao
# class FadeScreen():
#     "like the class 'Fade', except that it is a fully-functioning screen"

#     @staticmethod
#     def fade(screen: pygame.Surface, fade_speed: float | int = 1, fade_direction: str = 'out') -> None:
#         clock = pygame.time.Clock()

#         fade_effect = Fade(fade_speed, fade_direction)

#         while fade_effect.completed is False:
#             pygame.event.get() #TODO: check if the player presses QUIT and exit the game within this loop
 
#             fade_effect.update_and_draw(screen)

#             pygame.display.flip()

#             clock.tick(60)