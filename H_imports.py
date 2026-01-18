import pygame
from H_constants import *
from H_colors import *


def placeholder_sprite(width, height, color = (0, 0, 0)) -> pygame.Surface:
    sprite = pygame.Surface([width, height])
    sprite.fill(color)
    return sprite


# sprite importing:
# file_path: specify a file path to the desired image
# scale_factor: a scale factor for how much the image should be enlargened or shrunk when it is displayed
# return_rect: whether you want a rect to be returned along with the image or not
# position: the rect's position on the screen
def import_sprite(file_path: str,
                  scale_factor: int | float = 1,
                  return_rect: bool = False,
                  position: tuple[int | str, int | str] = (0, 0)
                  ) -> tuple[pygame.Surface, pygame.Rect] | pygame.Surface:
    try:
        sprite = pygame.image.load('C:\\Users\\zianr\\OneDrive\\Desktop\\coding things\\python\\games\\fly_game\\assets\\' + file_path).convert_alpha()
    except FileNotFoundError:
        sprite = pygame.image.load(file_path).convert_alpha()

    sprite_width = sprite.get_width() * scale_factor
    sprite_height = sprite.get_height() * scale_factor

    sprite = pygame.transform.scale(sprite, (sprite_width, sprite_height))

    if return_rect:
        x_pos, y_pos = position
        if position[0] == 'center':
            x_pos = (constants['SCREEN_WIDTH'] - sprite_width) / 2
        if position[1] == 'center':
            y_pos = (constants['SCREEN_HEIGHT'] - sprite_height) / 2
        
        sprite_rect = pygame.Rect(x_pos, y_pos, sprite_width, sprite_height)

        return sprite, sprite_rect
    
    else:
        return sprite


#wrapper function because i aint remembering all that
def list_fonts() -> None:
    print(pygame.font.get_fonts())


#also a wrapper function because that shit is way too confusing
def import_font(font_name: str, font_size: int) -> pygame.font.Font:
    return pygame.font.Font(pygame.font.match_font(font_name), font_size)



#font file paths:
# - C:\Users\zianr\OneDrive\Desktop\coding things\python\games\fly_game\assets\fonts\Pixelify_Sans\PixelifySans-Regular.ttf
# - C:\Users\zianr\OneDrive\Desktop\coding things\python\games\fly_game\assets\fonts\Raleway\Raleway-Regular.ttf

def import_font_sizes(font_name: str | None, font_sizes: tuple[int, ...]) -> dict[int, pygame.font.Font]:
    '''
    imports multiple font sizes of a single font

    putting None for font_name defaults to Raleway
    
    returns a dictionary which is pretty cool because you can just be like font[23] and then that will be that font at size 23
    '''
    fonts = {}
    for font_size in font_sizes:
        if font_name == None:
            font = pygame.font.Font(r'C:\Users\zianr\OneDrive\Desktop\coding things\python\games\fly_game\assets\fonts\Raleway\Raleway-Regular.ttf', font_size)
        else:
            font = import_font(font_name, font_size)

        fonts[font_size] = font
    
    return fonts

import datetime
datetime.time
class AutoFont():
    '''automatically imports fonts in given sizes

    example:

    font = AutoFont('font.ttf')

    font[50] # returns the font in size 50
    '''

    def __init__(self, file_path: str = r'C:\Users\zianr\OneDrive\Desktop\coding things\python\games\fly_game\assets\fonts\Raleway\Raleway-Regular.ttf'):
        self.file_path = file_path
        self.fonts = {}

    def __getitem__(self, font_size: int):
        if font_size in self.fonts:
            return self.fonts[font_size]
        
        self.fonts[font_size] = pygame.font.Font(self.file_path, font_size)
        print(self.fonts)
        return self.fonts[font_size]


#split text into words
#for each word, check if the width of it + the width of all previous words is longer than the inputted width
#if so, put a line break there
#repeat
def auto_add_line_breaks(font: pygame.font.Font, text: str, width: int):
    output = []

    for section in text.split('\n'):
        test_string = ''
        for word in section.split(' '):
            
            test_string += word + ' '

            #print(f'test_string is "{test_string}" with a width of {font.size(test_string)[0]} (max width = {width})')
            
            if font.size(test_string)[0] >= width:
                output.append('\n')
                test_string = word + ' '
            
            output.append(word + ' ')
        
        output.append('\n')
    
    output = output[:-1]
    return ''.join(output)


#this is a lot of yap but it makes rendering text wayyyy easier
#the parameters are pretty self-explainatory imo so im not gonna explain them

#ok update this function has become so complicated wtf is happening
def render_text(font: pygame.font.Font,
                text: str,
                rect: pygame.Rect = pygame.Rect(0, 0, 9999, 0),
                
                padding: int = (0, 0),
                line_spacing: float | int = 50,
                antialias: bool = True,
                color: pygame.Color | tuple[int, int, int] = (255, 255, 255),
                scale_factor: float | int = 1
                ) -> tuple[pygame.Surface, pygame.Rect]:
    
    width = rect.width
    position = list(rect.topleft)

    position[0] += padding[0]
    position[1] += padding[1]
    width -= padding[0] * 2
    
    text = auto_add_line_breaks(font, text, width)

    rendered_lines = []
    longest_line = 0
    total_height = 0

    #splits the text by line breaks and renders each line individually
    lines = text.split('\n')
    for i, line in enumerate(lines):
        #render the line, scale it, and store it in 'rendered_lines'
        rendered_line = font.render(line, antialias, color)
        rendered_line = pygame.transform.scale_by(rendered_line, scale_factor)
        rendered_lines.append(rendered_line)
        
        #add the line's height to 'total_height'
        total_height += (line_spacing + font.get_height()) * scale_factor

        #update longest line if it is no longer the longest line
        if rendered_line.get_size()[0] > longest_line:
            longest_line = rendered_line.get_size()[0]

    width = longest_line

    #create a tranparent surface for the text with its dimensions based on the inputted width and the height value in 'total_height'
    rendered_text = pygame.Surface([width, total_height]).convert_alpha()
    rendered_text.fill((0, 0, 0, 0))

    #blit all lines to the surface 
    for i, line in enumerate(rendered_lines):
        rendered_text.blit(line, (0, i * line_spacing * scale_factor))

    #create a rect for the surface
    rendered_text_rect = pygame.rect.Rect(position[0], position[1], width, total_height)


    return rendered_text, rendered_text_rect


if __name__ == '__main__':
    pygame.font.init()

    list_fonts()

    # test_font = import_font_sizes(None, (50,))

    # please_have_line_breaks = auto_add_line_breaks(test_font[50], 'the quick brown fox jumped over the lazy river \nahhhhhhhhh please add line breaks only in ohio', 400)
    # print(please_have_line_breaks)