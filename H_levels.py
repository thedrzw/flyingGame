from H_constants import *
from H_colors import *

import pygame
import random
import math

from H_imports import *

from typing import Any


# def rect_matches_coordinates(rect: pygame.Rect, x: float | int, y: float | int, width: float | int, height: float | int) -> bool:
#     return rect.topleft == (x, y) and rect.size == (width, height)

#write a repr for your classes or draw 32
#me:

def in_between(value: int | float, lower_bound: int | float, upper_bound: int | float) -> bool:
    """returns True if 'value' is between 'lower_bound' and 'upper_bound' (inclusive for lower bound, exclusive for upper bound)
    
    equivalent to: 'value >= lower_bound and value < upper_bound'
    """
    return value >= lower_bound and value < upper_bound

class PhysicsHelper:
    @staticmethod
    def check_offscreen(x, y, x_speed, y_speed, width, height):
        '''updates an object's x/y position and x/y speed if the object is out of bounds (OOB)\n\nsidenote i love the acroynm oob it sounds so funny'''
        if x > constants['SCREEN_WIDTH'] - width:# and x_speed > 0:
            x_speed = 0
            x = constants['SCREEN_WIDTH'] - width
        
        elif x < 0:# and x_speed < 0:
            x_speed = 0
            x = 0
        
        if y > constants['PLAYABLE_HEIGHT'] - height:# and y_speed < 0:
            y_speed = 0
            y = constants['PLAYABLE_HEIGHT'] - height
        
        elif y < 0:# and y_speed > 0:
            y_speed = 0
            y = 0
        
        return x, y, x_speed, y_speed
    
    @staticmethod
    def normalize_vectors(x_vector, y_vector):
        '''the function's name is pretty self-explanitory tbh'''
        scale_factor = ((x_vector ** 2) + (y_vector ** 2)) ** 0.5
        normalized_x = x_vector / scale_factor
        normalized_y = y_vector / scale_factor
        return normalized_x, normalized_y
    
    @staticmethod
    def find_vector(x1: int | float, y1: int | float, x2: int | float, y2: int | float) -> tuple[int | float, int | float]:
        '''finds the normalized vector that points from (x1, y1) to (x2, y2)'''
        x_vector = x2 - x1
        y_vector = y2 - y1

        x_vector, y_vector = PhysicsHelper.normalize_vectors(x_vector, y_vector)

        return (x_vector, y_vector)
    
    @staticmethod
    def slow_down(value: int | float, slow_percentage: int | float = 1, slow_constant: int | float = 0) -> int:
        '''
        value is the value to be "slowed" (reduced)\n
        slow_percentage is the percent that the value will be reduced to (eg. 0.8 means the value is mulitplied by 0.8)\n
        slow_constant is a constant that is subtracted from the value (applied after the percentage)
        '''

        value *= slow_percentage

        if value == 0:
            return value
        
        elif value > 0:
            value -= slow_constant
            if value < 0:
                return 0
            else:
                return value
        
        elif value < 0:
            value += slow_constant
            if value > 0:
                return 0
            else:
                return value


class GameObject:
    
    def __init__(self, sprite_and_rect: tuple[pygame.Surface, pygame.Rect]) -> None:
        try:
            self.add_to_all(self)
        except AttributeError:
            raise NotImplementedError('you need to define a class variable named "all" in the class that inherits from UIObject\neg "all = []"')
        
        self.rect = sprite_and_rect[1]
        self.sprite = sprite_and_rect[0]

        self.x, self.y = self.rect.topleft
        self.width, self.height = self.rect.size
        self.middle_x, self.middle_y = self.x + (self.width / 2), self.y + (self.height / 2)

        self.delete = False
    
    @classmethod
    def add_to_all(cls, self):
        cls.all.append(self)

    def update(self):
        raise NotImplementedError('you need to define a update method in order to call it ._.')

    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprite, self.rect)

    @classmethod
    def update_all(cls, *args):
        if not hasattr(cls, 'all'): #raise an error if there's no class variable named "all"
            raise NotImplementedError('you need to define a class variable named "all" in the class that inherits from UIObject\neg "all = []"')
        
        #>> and this is v3, thanks to chatgpt (clean and actually makes sense)
        for instance in cls.all:
            instance.update(*args)
        
        if len(cls.all) > 0:
            if hasattr(cls.all[0], 'delete'):
                cls.all = [instance for instance in cls.all if (not instance.delete)]


        #>> this was v2 (works but is messy af)
        #please god forgive me for this sinful code
        # starting_length = len(cls.all)
        # i = 0

        # while i < starting_length:
        #     cls.all[i].update(*args)

        #     if starting_length == len(cls.all):
        #         i += 1
        #     elif starting_length - 1 == len(cls.all):
        #         starting_length = len(cls.all)
        #     else:
        #         raise Exception(f'lmao something went wrong\n{starting_length = }\n{len(cls.all) = }')
                

        #>> ok so this was v1 (doesn't work)
        # all_instances = cls.all.copy() #this might cause errors because of shallow copying - hopefully it doesn't!
        # for instance in all_instances:
        #     instance.update(*args)
    
    @classmethod
    def draw_all(cls, *args):
        if not hasattr(cls, 'all'): #raise an error if there's no class variable named "all"
            raise NotImplementedError('you need to define a class variable named "all" in the class that inherits from UIObject\neg "all = []"')

        for instance in cls.all:
            instance.draw(*args)


class MovingGameObject(GameObject):
    #you can tell this class caused me kind of a headache because of all the commented-out code

    def __init__(self, sprite_and_rect: tuple[pygame.Surface, pygame.Rect]) -> None:
        #no super().__init__() because of getter and setter stuff
        #idk man just go with it
        try:
            self.add_to_all(self)
        except AttributeError:
            raise NotImplementedError('you need to define a class variable named "all" in the class that inherits from MovingGameObject\neg "all = []"')
        
        self.rect = sprite_and_rect[1] # calls the rect setter, which sets self.x, self.y, self.width, and self.height
        self.sprite = sprite_and_rect[0]

        self.delete = False
        
        self.x_speed = 0
        self.y_speed = 0
    
    #all these getter and setter methods basically just update self.x, self.y, self.width, and self.height whenever they're call
    
    @property #getter method (is this a reference)
    def middle_x(self):
        return self.x + (self.width / 2)
    
    @middle_x.setter #setter method (this IS a reference)
    def middle_x(self, middle_x):
        self.x = middle_x - (self.width / 2)
    
    @property
    def middle_y(self):
        return self.y + (self.width / 2)
    
    @middle_y.setter
    def middle_y(self, middle_y):
        self.y = middle_y - (self.height / 2)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    @rect.setter
    def rect(self, rect: pygame.Rect):
        self.x, self.y = rect.topleft
        self.width, self.height = rect.size


    def update_position(self) -> None:
        self.x += self.x_speed
        self.y += self.y_speed
    
    def update(self):
        self.update_position()

    #haha don't worry about all this commented-out code just scoll on by

    # #honestly not sure wtf is happening in this function but don't worry about it lmao
    # def update_coordinates(self) -> None:
    #     #if the x, y, width, and height values match the normal rect
    #     if rect_matches_coordinates(self.rect, self.x, self.y, self.width, self.height):
    #         #set the private rect to the same value as the normal rect
    #         if not (self._rect == self.rect):
    #             self._rect = self.rect
        
    #     #if any one of the x, y, width, or height values doesn't match the normal rect
    #     else: #use the private rect as the tiebreaker

    #         #if the private rect and the normal rect match
    #         if self._rect == self.rect:
    #             #set both the private and normal rect to the values in x, y, width, and height
    #             self.rect.topleft = (self.x, self.y)
    #             self.rect.size == (self.width, self.height)

    #             self._rect = self.rect
            
    #         # - commented out because you should only use the rect for displaying sprites
    #         # - if you need to edit position, change the object's x/y values because those use floats instead of ints
    #         # elif rect_matches_coordinates(self._rect, self.x, self.y, self.width, self.height):
    #         #     #set the x, y, width, height, and private rect values to the value in the normal rect
    #         #     (self.x, self.y) = self.rect.topleft
    #         #     (self.width, self.height) = self.rect.size
                
    #         #     self._rect = self.rect

    #         else:
    #             raise Exception(
    #             "don't change the values of _rect or rect of this object you bozo\n"
    #             "instead you should only change the x/y/width/height values and they'll be auto updated\n"
    #             f"_rect = {self._rect}\n"
    #             f"rect = {self.rect}\n"
    #             f"x, y, width, height = {self.x, self.y, self.width, self.height}\n"
    #             "good luck debugging!"
    #             )
        
    #     self.middle_x, self.middle_y = self.x + (self.width / 2), self.y + (self.height / 2)


#for player data, drawing player
class Player(MovingGameObject):
    all = []
    
    def __init__(self, level_duration):
        sprite = placeholder_sprite(25, 25)
        rect = pygame.Rect((constants['SCREEN_WIDTH'] - 25) / 2, (constants['PLAYABLE_HEIGHT'] - 25) / 2, 25, 25)
        super().__init__((sprite, rect))

        #mmmmmmm yes numbesr i love numbers yes yes
        self.x_move_strength = 1.2
        self.y_move_strength = 2.4
        self.gravity = 0.9
        self.slow_percentage = 0.96
        self.slow_constant = 0.2
        self.speed_multiplier = 0.8
        self.boost_strength = 50

        self.gun_cooldown = 1 #amount of time before you can shoot another shot (including the frame of the shot) (eg. 2 would mean that you shoot every other frame)
        self.time_since_last_shot = self.gun_cooldown

        self.health = 100

        self.invincibility = 0

        self.time_remaining = level_duration #time remaining in the level

    def take_damage(self, damage, i_frames, kb_vector = [0, 0], kb_strength = 2): #called when the player is hit
        if self.invincibility == 0:
            self.health -= damage
            self.invincibility += i_frames

            self.x_speed += kb_vector[0] * kb_strength
            self.y_speed -= kb_vector[1] * kb_strength
    
    def update(self, events): #called every frame
        self.time_remaining -= 1
        self.time_since_last_shot += 1

        if events['mouse1'][1]:
            if self.time_since_last_shot >= self.gun_cooldown:
                Projectile(self.middle_x, self.middle_y, events['mouse_pos'][0], events['mouse_pos'][1], 5, (Enemy, ))
                self.time_since_last_shot = 0

        if events['mouse2'][0]:
            x_boost, y_boost = PhysicsHelper.find_vector(self.middle_x, self.middle_y, events['mouse_pos'][0], events['mouse_pos'][1])
            x_boost *= self.boost_strength
            y_boost *= self.boost_strength

            self.x_speed += x_boost
            self.y_speed -= y_boost

        if events['w'][1]:
            self.y_speed += self.y_move_strength

        if events['a'][1]:
            self.x_speed -= self.x_move_strength
        
        if events['d'][1]:
            self.x_speed += self.x_move_strength
        

        #speed slowing (air resistance i guess??)
        if self.x_speed != 0 or self.y_speed != 0:
            self.x_speed = PhysicsHelper.slow_down(self.x_speed, self.slow_percentage, self.slow_constant)
            self.y_speed = PhysicsHelper.slow_down(self.y_speed, self.slow_percentage, self.slow_constant)

        #gravity calculation
        self.y_speed -= self.gravity
        
        #update player position based on speed
        self.x += self.x_speed * self.speed_multiplier
        self.y -= self.y_speed * self.speed_multiplier

        #keeps the player on the screen
        self.x, self.y, self.x_speed, self.y_speed = PhysicsHelper.check_offscreen(self.x, self.y, self.x_speed, self.y_speed, self.width, self.height)

        #update rect position
        #self.update_coordinates()

        #decrement player invincibility and update sprite model
        if self.invincibility > 0:
            self.invincibility -= 1
        
        if self.invincibility > 0:
            self.sprite = placeholder_sprite(25, 25, PURPLE)
        else:
            self.sprite = placeholder_sprite(25, 25, RED)
    

#for handling bullet movement/collision
class Projectile(MovingGameObject):
    all = []

    def __init__(self, x, y, target_x, target_y, speed, targets = (Player,)):
        self.width = 10
        self.height = 10
        sprite = placeholder_sprite(self.width, self.height, PURPLE)
        rect = pygame.Rect(x - (self.width / 2), y - (self.height / 2), self.width, self.height)
        super().__init__((sprite, rect))

        self.target_x = target_x - (self.width / 2)
        self.target_y = target_y - (self.height / 2)
        self.speed = speed

        #math mmmm yes
        self.x_vector, self.y_vector = PhysicsHelper.find_vector(self.x, self.y, self.target_x, self.target_y)

        self.x_speed = self.x_vector * self.speed
        self.y_speed = self.y_vector * self.speed

        self.targets = targets

    def update(self, player: Player):
        super().update()
        
        if Player in self.targets:
            if pygame.Rect.colliderect(self.rect, player.rect):
                player.take_damage(2, 0)
                # player.take_damage(2, 0, [self.x_vector, self.y_vector], 10)
                self.delete = True

        else:
            for thing in self.targets:
                thing_hit = self.rect.collidelist(thing.all)
                if thing_hit != -1:
                    thing.all[thing_hit].delete = True
                    self.delete = True
                    break

        if self.x > constants['SCREEN_WIDTH'] + 100 or self.x < -100 or self.y > constants['PLAYABLE_HEIGHT'] + 100 or self.y < -100:
            self.delete = True
    
    @classmethod
    def update_all(cls, player: Player):
        super().update_all(player)


#for enemies that shoot projectiles
class Shooter(MovingGameObject):
    all = []

    #shooting patterns
    SP_minigun = [120, 15, 14, 12, 9, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    SP_burst = [20, 3, 3]
    SP_normal = [30]

    #shooting pattern is the number of frames in between each shot (eg. SP = [10, 20] means shoot, wait 10 frames, shoot, wait 20 frames, repeat)
    def __init__(self, projectile_speed = 20, shooting_pattern: list[int] = SP_normal, x = -100, y = -100):
        sprite = placeholder_sprite(50, 50, PURPLE)
        rect = pygame.Rect(x, y, 50, 50)
        super().__init__((sprite, rect))

        self.projectile_speed = projectile_speed
        self.SP = shooting_pattern
        #self.lead_shots = lead_shots #commented out because trying to lead shots makes the shooters aim really weird :/

        self.frames_since_last_shot = 0
        self.SP_index = 0
    
    #shoots a new projectile towards the player
    def update(self, player: Player):
        super().update()

        self.frames_since_last_shot += 1
        if self.frames_since_last_shot >= self.SP[self.SP_index]:
            
            
            #distance_from_player = math.dist((player.middle_x, player.middle_y), (self.middle_x, self.middle_y))
            aiming_x = player.x + (player.width / 2)# + (player.x_speed * (distance_from_player / 100) * self.lead_shots)
            aiming_y = player.y + (player.height / 2)# + (player.y_speed * (distance_from_player / 100) * self.lead_shots)

            Projectile(self.x + (self.width / 2), self.y + (self.height / 2), aiming_x, aiming_y, self.projectile_speed)
            
            self.frames_since_last_shot = 0
            self.SP_index += 1
            self.SP_index = self.SP_index % len(self.SP)
    
    @classmethod
    def update_all(cls, player: Player):
        super().update_all(player)


class Enemy(Shooter):
    """
    like a shooter, but with an AI!

    set the 'enemy_settings' parameter to Enemy.chase for the enemy to follow the player, or Enemy.run for it to run away

    enemy_settings should look like this: {'run_distance': 0, 'follow_distance': 300}

    'run_distance' will determine how far away the enemy has to be from the player to stop running

    'follow_distance' will determine how close the enemy has to be to the player to stop following

    'run distance' should always be bigger than 'follow_distance'
    """
    
    all = []

    chase_settings = {
        'run_distance': 0,
        'follow_distance': 300
    }

    run_settings = {
        'run_distance': 500,
        'follow_distance': 1000
    }

    def __init__(self, projectile_speed = 20, shooting_pattern: list[int] = Shooter.SP_normal, x = -100, y = -100, enemy_settings: dict = chase_settings):
        super().__init__(projectile_speed, shooting_pattern, x, y)

        self.run_distance = enemy_settings['run_distance'] #will accelerate away from the player until being this far away from the player
        self.follow_distance = enemy_settings['follow_distance'] #will accelerate towards the player until being this far away from the player

        self.slow_percentage = 0.95
        self.slow_constant = 0.1  #do not set this to a high number like 10 lmao it makes the enemies move really weird

        self.idle_movement = 1

        self.frames_elapsed = 0


    def update(self, player: Player):
        self.frames_elapsed += 1
        super().update(player)

        distance_from_player = math.dist((player.middle_x, player.middle_y), (self.middle_x, self.middle_y))

        if distance_from_player > self.follow_distance:
            x_acceleration, y_acceleration = PhysicsHelper.find_vector(self.middle_x, self.middle_y, player.middle_x, player.middle_y)

            self.x_speed += x_acceleration
            self.y_speed += y_acceleration
        

        elif distance_from_player < self.run_distance:
            x_acceleration, y_acceleration = PhysicsHelper.find_vector(self.middle_x, self.middle_y, player.middle_x, player.middle_y)

            self.x_speed -= x_acceleration
            self.y_speed -= y_acceleration


        #lil bit of randomness
        self.x_speed += random.uniform(- self.idle_movement, self.idle_movement)
        self.y_speed += random.uniform(- self.idle_movement, self.idle_movement)

        #slow down
        #erm, chat? why is this in the Player class?? update: i just moved it to PhysicsHelper they call me the programmer
        self.x_speed = PhysicsHelper.slow_down(self.x_speed, self.slow_percentage, self.slow_constant)
        self.y_speed = PhysicsHelper.slow_down(self.y_speed, self.slow_percentage, self.slow_constant)

        #check offscreen
        self.x, self.y, self.x_speed, self.y_speed = PhysicsHelper.check_offscreen(self.x, self.y, self.x_speed, self.y_speed, self.width, self.height)


#for the moving walls 
class Wall(MovingGameObject):
    all = []

    def __init__(self, speed, gap = 400, center_y = None, shooter: Shooter = None):
        'negative speed means the wall is coming from the right, and positive speed means from the left'

        super().__init__(import_sprite('wall.png', 5, True))

        if speed > 0:
            self.x = - self.width
        elif speed < 0:
            self.x = constants['SCREEN_WIDTH']
        else:
            raise ValueError("bruh! speed can't be equal to 0 bozo")

        self.x_speed = speed
        self.shooter = shooter

        self.padding = gap / 2 #the area on the top/bottom of the screen where the walls can't be centered on
        self.gap = gap #the area between the walls
        self.half_gap = self.gap / 2
        if center_y is None:
            self.center_y = random.uniform(self.padding, constants['PLAYABLE_HEIGHT'] - self.padding) #the middle of the gap between the walls

        elif center_y < self.padding or center_y > constants['PLAYABLE_HEIGHT'] - self.padding:
                raise ValueError("bruh! center_y was out of bounds")
        
        else:
            self.center_y = center_y

        self.top_rect = self.rect.copy()
        self.top_rect.y = (self.center_y - self.half_gap) - self.rect.height
        
        self.bottom_rect = self.rect.copy()
        self.bottom_rect.y = self.center_y + self.half_gap

        if self.shooter:
            self.shooter_position = random.choice(['top', 'bottom'])
            if self.shooter_position == 'top':
                self.shooter.y = self.center_y - self.half_gap - self.shooter.height
            elif self.shooter_position == 'bottom':
                self.shooter.y = self.center_y + self.half_gap

    def update(self, player: Player): #called every frame
        super().update()

        self.top_rect.x = self.rect.x
        self.bottom_rect.x = self.rect.x

        if pygame.Rect.colliderect(self.top_rect, player.rect) or pygame.Rect.colliderect(self.bottom_rect, player.rect):
            player.take_damage(12.5, 60)

        if self.shooter:
            self.shooter.x = self.x + (self.width / 2) - (self.shooter.width / 2)
        
        if (self.x < - self.width - 100) or (self.x > constants['SCREEN_WIDTH'] + 100):
            self.delete = True

            if self.shooter:
                self.shooter.delete = True
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprite, self.top_rect)
        screen.blit(self.sprite, self.bottom_rect)

    @classmethod
    def update_all(cls, player: Player):
        super().update_all(player)
    
    @staticmethod
    def wall_based_on_previous(previous_wall_center_y: int, min_range: int, max_range: int, speed, gap = 400, shooter: Shooter = None) -> 'Wall':
        '''creates a new wall based on the position of a previous wall
        
        creates a new wall with a random position that is at least 'min_range' away from the previous_wall's 'center_y' and at most 'max_range' away
        '''

        padding = gap / 2

        #make sure the bounds are bounded???
        lower_bound = previous_wall_center_y - max_range
        upper_bound = previous_wall_center_y + max_range

        if lower_bound < padding:
            lower_bound = padding
        if upper_bound > constants['PLAYABLE_HEIGHT'] - padding:
            upper_bound = constants['PLAYABLE_HEIGHT'] - padding

        #find the minimum distances from the previous wall
        lower_min = previous_wall_center_y - min_range
        upper_min = previous_wall_center_y + min_range

        #determine if the new y pos will be lower or higher
        if lower_min < padding:
            wall_will_be = 'higher'
        elif upper_min > constants['PLAYABLE_HEIGHT'] - padding:
            wall_will_be = 'lower'
        else:
            wall_will_be = random.choice(['higher', 'lower'])

        #finally create the new center y position
        if wall_will_be == 'higher':
            new_center_y = random.uniform(upper_min, upper_bound)
        elif wall_will_be == 'lower':
            new_center_y = random.uniform(lower_bound, lower_min)
        
        return Wall(speed, gap, new_center_y, shooter)
        




#for health bar, time bar, etc on the hud
class HealthBar(GameObject):
    all = []

    def __init__(self, x, total):
        self.width = 100 * 5
        self.height = 13 * 5
        self.x = x
        self.y = constants['PLAYABLE_HEIGHT'] + ((constants['SCREEN_HEIGHT'] - constants['PLAYABLE_HEIGHT']) / 2) - (self.height / 2)

        super().__init__((import_sprite('health bar outline.png', 5), pygame.Rect(self.x, self.y, self.width, self.height)))

        self.total = total

        self.top, self.bar_rect = import_sprite('health bar green.png', 5, True, (self.x + 45, self.y))
        self.middle = import_sprite('health bar yellow.png', 5)
        self.bottom = import_sprite('health bar red.png', 5)

        self.top_width = self.bar_rect.width
        self.middle_width = self.bar_rect.width

        self.middle_shown = self.middle.subsurface(pygame.Rect(0, 0, self.middle_width, self.height))
        self.top_shown = self.top.subsurface(pygame.Rect(0, 0, self.top_width, self.height))

    
    def update(self, value):
        percent_remaining = value / self.total
        if percent_remaining > 1:
            percent_remaining = 1
        elif percent_remaining < 0:
            percent_remaining = 0
            
        self.top_width = self.bar_rect.width * percent_remaining

        if self.top_width <= 0:
            self.top_width = 0

        if self.top_width < self.middle_width:
            self.middle_width -= ((self.middle_width - self.top_width) * 0.1) + 0.1

            if self.top_width > self.middle_width:
                self.middle_width = self.top_width

            self.middle_shown = self.middle.subsurface(pygame.Rect(0, 0, self.middle_width, self.height))

        self.top_shown = self.top.subsurface(pygame.Rect(0, 0, self.top_width, self.height))

    
    def draw(self, screen):
        screen.blit(self.bottom, self.bar_rect)
        screen.blit(self.middle_shown, self.bar_rect)
        screen.blit(self.top_shown, self.bar_rect)
        screen.blit(self.sprite, self.rect)


class TimeBar(GameObject):
    all = []

    def __init__(self, x, total):
        self.width = 100 * 5
        self.height = 13 * 5
        self.x = x
        self.y = constants['PLAYABLE_HEIGHT'] + ((constants['SCREEN_HEIGHT'] - constants['PLAYABLE_HEIGHT']) / 2) - (self.height / 2)

        super().__init__((import_sprite('time bar outline.png', 5), pygame.Rect(self.x, self.y, self.width, self.height)))

        self.total = total

        self.top, self.bar_rect = import_sprite('time bar blue.png', 5, True, (self.x + 45, self.y))
        self.bottom = import_sprite('time bar orange.png', 5)

        self.top_width = self.bar_rect.width

        self.top_shown = self.top.subsurface(pygame.Rect(0, 0, self.top_width, self.height))

    def update(self, value):
        percent_remaining = (self.total - value) / self.total
        if percent_remaining > 1:
            percent_remaining = 1
        elif percent_remaining < 0:
            percent_remaining = 0

        self.top_width = self.bar_rect.width * percent_remaining

        self.top_shown = self.top.subsurface(pygame.Rect(0, 0, self.top_width, self.height))
    
    def draw(self, screen):
        screen.blit(self.bottom, self.bar_rect)
        screen.blit(self.top_shown, self.bar_rect)
        screen.blit(self.sprite, self.rect)


#for showing the bars/other stuff
class Hud(GameObject):
    all = []

    def __init__(self, max_player_health, time_remaining):
        sprite = import_sprite('HUD background.png', 10)
        rect = pygame.Rect(0, constants['PLAYABLE_HEIGHT'], constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'] - constants['PLAYABLE_HEIGHT'])
        super().__init__((sprite, rect))

        self.health_bar = HealthBar(100, max_player_health)
        self.time_bar = TimeBar(700, time_remaining)
    
    def update(self, player_health, time_remaining):
        self.health_bar.update(player_health)
        self.time_bar.update(time_remaining)

    def draw(self, screen):
        super().draw(screen)
        self.health_bar.draw(screen)
        self.time_bar.draw(screen)


class Everything:

    def update(events: dict):
        player: Player = Player.all[0]
        hud: Hud = Hud.all[0]

        player.update(events)
        
        Wall.update_all(player)
        Shooter.update_all(player)
        Enemy.update_all(player)
        Projectile.update_all(player)

        hud.update(player.health, player.time_remaining)

        
    def draw(screen: pygame.Surface):
        player: Player = Player.all[0]
        hud: Hud = Hud.all[0]

        player.draw(screen)

        Wall.draw_all(screen)
        Shooter.draw_all(screen)
        Enemy.draw_all(screen)
        Projectile.draw_all(screen)

        hud.draw(screen)


    #clears all of the "all" variables
    def delete() -> None:
        Player.all = []
        Hud.all = []
        HealthBar.all = []
        TimeBar.all = []

        Wall.all = []
        Shooter.all = []
        Enemy.all = []
        Projectile.all = []