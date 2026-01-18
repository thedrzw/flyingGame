def main(screen):
    import pygame
    import random
    from H_constants import constants

    #define colors
    BLACK = [0, 0, 0]

    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]

    YELLOW = [255, 255, 0]
    PURPLE = [255, 0, 255]
    LIGHT_BLUE = [0, 255, 255]

    WHITE = [255, 255, 255]

    GRAY = [100, 100, 100]
    DARK_GRAY = [50, 50, 50]

    #create clock
    clock = pygame.time.Clock()


    #onscreen text
    #print(pygame.font.get_fonts())
    font = pygame.font.Font(pygame.font.match_font('lucidasans'), 20)

    debug_text = font.render('', True, WHITE)
    debug_text_rect = debug_text.get_rect()
    debug_text_rect.topleft = (10, 10)

    def display_multiple_lines(text: str, rect, color = WHITE, spacing = 20):
        lines = text.split('\n')
        for i, line in enumerate(lines):
            rendered_line = font.render(line, True, color)
            screen.blit(rendered_line, [rect[0], rect[1] + (i * spacing)])

    def normalize_vectors(x_vector, y_vector):
        scale_factor = ((x_vector ** 2) + (y_vector ** 2)) ** 0.5
        normalized_x = x_vector / scale_factor
        normalized_y = y_vector / scale_factor
        return normalized_x, normalized_y


    class AllMethods():
        @classmethod
        def update_all(cls):
            i = 0
            while i < len(cls.all):
                instance = cls.all[i]
                deleted = False
                deleted = instance.update()
                if not deleted:
                    i += 1
        
        @classmethod
        def draw_all(cls):
            for instance in cls.all:
                instance.draw()   


    #for player data, drawing player
    class Player():
        def __init__(self):
            self.width = 25
            self.height = 25

            self.x = (constants['SCREEN_WIDTH'] - self.width) / 2
            self.y = (constants['PLAYABLE_HEIGHT'] - self.height) / 2

            self.x_speed = 0
            self.y_speed = 0

            self.x_speed_limit = 20
            self.y_speed_limit = 15

            self.move_strength = 1
            self.jump_strength = 1

            self.gravity = 0.4
            self.resistance = 0.4

            self.health = 100 #default is 100

            self.display = pygame.Rect(self.x, self.y, self.width, self.height)

            self.invincibility = 0

        @staticmethod
        def slow_down(value, slow_factor) -> int:
            if value == 0:
                return value
            
            elif value > 0:
                value -= slow_factor
                if value < 0:
                    return 0
                else:
                    return value
            
            elif value < 0:
                value += slow_factor
                if value > 0:
                    return 0
                else:
                    return value

        def take_damage(self, damage, i_frames, kb_vector = [0, 0], kb_strength = 2): #called when the player is hit
            if self.invincibility == 0:
                self.health -= damage
                self.invincibility += i_frames

                self.x_speed += kb_vector[0] * kb_strength
                self.y_speed -= kb_vector[1] * kb_strength
        
        def calculate_physics(self): #called every frame
            #decrement player invincibility
            if self.invincibility > 0:
                self.invincibility -= 1

            #x speed slowing (air resistance i guess??)
            self.x_speed = Player.slow_down(self.x_speed, self.resistance)

            #gravity calculation
            self.y_speed -= self.gravity


            #keeps the player on the screen
            if self.x >= constants['SCREEN_WIDTH'] - self.width and self.x_speed > 0:
                self.x_speed = 0
                self.x = constants['SCREEN_WIDTH'] - self.width
            
            if self.x < 0 and self.x_speed < 0:
                self.x_speed = 0
                self.x = 0
            
            if self.y >= constants['PLAYABLE_HEIGHT'] - self.height and self.y_speed < 0:
                self.y_speed = 0
                self.y = constants['PLAYABLE_HEIGHT'] - self.height
            
            if self.y < 0 and self.y_speed > 0:
                self.y_speed = 0
                self.y = 0
        
            
            #limits player speed
            if abs(self.x_speed) > self.x_speed_limit:
                if self.x_speed > 0:
                    self.x_speed = self.x_speed_limit
                if self.x_speed < 0:
                    self.x_speed = - self.x_speed_limit

            if abs(self.y_speed) > self.y_speed_limit:
                if self.y_speed > 0:
                    self.y_speed = self.y_speed_limit
                if self.y_speed < 0:
                    self.y_speed = - self.y_speed_limit
            

            #adds player speed to current position
            self.x += self.x_speed
            self.y -= self.y_speed

        def draw(self):
            self.display.update(self.x, self.y, self.width, self.height)
            if self.invincibility > 0:
                pygame.draw.rect(screen, PURPLE, self.display)
            else:
                pygame.draw.rect(screen, RED, self.display)        
        

    #for handling bullet movement/collision
    class Projectile(AllMethods):
        all = []

        def __init__(self, x, y, target_x, target_y, speed):
            Projectile.all.append(self)

            self.width = 10
            self.height = 10

            self.x = x - (self.width / 2)
            self.y = y - (self.height / 2)
            self.target_x = target_x - (self.width / 2)
            self.target_y = target_y - (self.height / 2)
            self.speed = speed

            #math mmmm yes
            self.x_vector = self.target_x - self.x
            self.y_vector = self.target_y - self.y

            self.x_vector, self.y_vector = normalize_vectors(self.x_vector, self.y_vector)

            self.display = pygame.Rect(self.x, self.y, self.width, self.height)

        def update(self):
            #updates the x and y position of the projectile
            self.x += self.x_vector * self.speed
            self.y += self.y_vector * self.speed
                
            if pygame.Rect.colliderect(self.display, player.display):
                player.take_damage(2, 0)
                # player.take_damage(2, 0, [self.x_vector, self.y_vector], 10)
                self.delete()
                return True

            if self.x > constants['SCREEN_WIDTH'] + 100 or self.x < -100 or self.y > constants['PLAYABLE_HEIGHT'] + 100 or self.y < -100:
                self.delete()
                return True
            
            return False
            
        def draw(self):
            self.display.update(self.x, self.y, 10, 10)
            pygame.draw.rect(screen, PURPLE, self.display) 

        def delete(self):
            Projectile.all.remove(self)
            del self


    #for enemies that shoot projectiles
    class Shooter(AllMethods):
        all = []

        #shooting patterns
        SP_minigun = [120, 15, 14, 12, 9, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        SP_burst = [20, 3, 3]
        SP_normal = [30]

        #shooting pattern is the number of frames in between each shot (eg. SP = [10, 20] means shoot, wait 10 frames, shoot, wait 20 frames, repeat)
        def __init__(self, x, y, projectile_speed, shooting_pattern: list[int]):
            Shooter.all.append(self)

            self.x = x
            self.y = y
            self.projectile_speed = projectile_speed
            self.SP = shooting_pattern

            self.width = 50
            self.height = 50

            self.frames_elapsed = 0
            self.SP_index = 0

            self.display = pygame.Rect(self.x, self.y, self.width, self.height)
        
        #shoots a new projectile towards the player
        def update(self):
            self.frames_elapsed += 1
            if self.frames_elapsed >= self.SP[self.SP_index]:
                Projectile(self.x + (self.width / 2), self.y + (self.height / 2), player.x + (player.width / 2), player.y + (player.height / 2), self.projectile_speed)
                self.frames_elapsed = 0
                self.SP_index += 1
                self.SP_index = self.SP_index % len(self.SP)
        
        def draw(self):
            self.display = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(screen, BLUE, self.display)

        def delete(self):
            Shooter.all.remove(self)
            del self


    #for the moving walls 
    class Wall(AllMethods):
        all = []

        def __init__(self, speed, shooter = None):
            Wall.all.append(self)

            self.speed = speed
            self.shooter = shooter
            self.shooter_position = random.choice(['top', 'bottom'])

            self.padding = 200 #the area on the top/bottom of the screen where the walls can't be centered on
            self.gap = 400 #the area between the walls

            self.x = constants['SCREEN_WIDTH']
            self.y = random.randrange(self.padding, constants['SCREEN_HEIGHT'] - self.gap)

            self.width = 100

            self.top_rect = pygame.Rect(self.x, 0, self.width, self.y - (self.gap / 2))
            self.bottom_rect = pygame.Rect(self.x, self.y + (self.gap / 2), self.width, constants['SCREEN_HEIGHT'])

        
        def update(self): #called every frame
            self.x -= self.speed

            self.top_rect.update(self.x, 0, self.width, self.y - (self.gap / 2))
            self.bottom_rect.update(self.x, self.y + (self.gap / 2), self.width, constants['SCREEN_HEIGHT'])

            if pygame.Rect.colliderect(self.top_rect, player.display) or pygame.Rect.colliderect(self.bottom_rect, player.display):
                player.take_damage(10, 60)

            if self.shooter:
                self.shooter.x = self.x + (self.width / 2) - (self.shooter.width / 2)

                if self.shooter_position == 'top':
                    self.shooter.y = self.y - (self.gap / 2) - self.shooter.height

                elif self.shooter_position == 'bottom':
                    self.shooter.y = self.y - (self.gap / 2) + self.gap
            
            if self.x <= - self.width:
                self.delete()
                return True
            
            return False
        
        def draw(self):
            pygame.draw.rect(screen, WHITE, self.top_rect)
            pygame.draw.rect(screen, WHITE, self.bottom_rect)

        def delete(self):
            if self.shooter:
                self.shooter.delete()
            
            Wall.all.remove(self)
            del self


    #for health bar, time bar, etc on the hud
    class Bar():
        all = []

        def __init__(self, x, total):
            Bar.all.append(self)

            self.height = 70
            self.width = 400
            self.padding = 10

            self.x = x
            self.y = constants['PLAYABLE_HEIGHT'] + ((constants['SCREEN_HEIGHT'] - constants['PLAYABLE_HEIGHT']) / 2) - (self.height / 2)
            self.total = total

            self.padding_rect = pygame.Rect(self.x - self.padding, self.y - self.padding, self.width + (2 * self.padding), self.height + (2 * self.padding))
            self.top_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            self.middle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            self.bottom_rect = pygame.Rect(self.x, self.y, self.width, self.height)

            self.middle_width = self.width
        
        def update(self, value):
            percent_remaining = value / self.total

            if self.top_rect.width < self.middle_rect.width:
                self.middle_width -= ((self.middle_rect.width - self.top_rect.width) * 0.1) + 0.1

                if self.top_rect.width > self.middle_width:
                    self.middle_width = self.top_rect.width

                self.middle_rect.update(self.x, self.y, self.middle_width, self.height)
            
            self.top_rect.update(self.x, self.y, self.width * percent_remaining, self.height)


    #for showing the bars/other stuff
    class Hud():
        def __init__(self):
            self.hud_rect = pygame.Rect(0, constants['PLAYABLE_HEIGHT'], constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'] - constants['PLAYABLE_HEIGHT'])
        
        def draw(self):
            #draw HUD
            pygame.draw.rect(screen, GRAY, self.hud_rect)
            
            #update health and time bar
            health_bar.update(player.health)
            time_bar.update(difficulty_timer)

            #draw health bar
            pygame.draw.rect(screen, BLACK, health_bar.padding_rect)
            pygame.draw.rect(screen, DARK_GRAY, health_bar.bottom_rect)
            pygame.draw.rect(screen, YELLOW, health_bar.middle_rect)
            pygame.draw.rect(screen, RED, health_bar.top_rect)

            #draw time bar
            pygame.draw.rect(screen, BLACK, time_bar.padding_rect)
            pygame.draw.rect(screen, DARK_GRAY, time_bar.bottom_rect)
            pygame.draw.rect(screen, PURPLE, time_bar.top_rect)        


    difficulty = 0 #ranges from 0 to 1
    #difficulty changes:
    # - how often walls appear
    # - wall speed
    # - how often shooters appear
    # - projectile speed
    # - TODO shooting patterns

    def change_difficulty(difficulty: int):
        if difficulty > 1:
            difficulty = 1

        base_wall_frequency = 60 * 3
        wall_frequency = base_wall_frequency * (1 - (difficulty * 0.75))

        base_wall_speed = 10
        wall_speed = base_wall_speed * (1 + (difficulty * 0.5))

        shooter_chance = 0.6 + (difficulty * 0.25)
        if shooter_chance > 1:
            shooter_chance = 1

        return wall_frequency, wall_speed, shooter_chance


    #define/instantiate
    running = True

    holding_up = False
    holding_left = False
    holding_right = False

    debug_shown = False

    wall_timer = 0
    difficulty_timer = 0
    DIFFICULTY_TIME_INTERVAL = 60 * 5

    player = Player()

    health_bar = Bar(50, player.health)
    time_bar = Bar(500, DIFFICULTY_TIME_INTERVAL)

    hud = Hud()

    wall_frequency, wall_speed, shooter_chance = change_difficulty(difficulty)

    # for i in range(0, 1):
    #     Shooter(0, i * 100, 25, Shooter.SP_minigun)


    #game loop
    while running == True:
        #event handler ----
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            
            #keyDOWN events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    holding_up = True
                
                if event.key == pygame.K_a:
                    holding_left = True
                
                if event.key == pygame.K_d:
                    holding_right = True
                
                if event.key == pygame.K_1:
                    debug_shown = not debug_shown

                if event.key == pygame.K_ESCAPE:
                    running = False
            
            #keyUP events
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    holding_up = False
                
                if event.key == pygame.K_a:
                    holding_left = False
                
                if event.key == pygame.K_d:
                    holding_right = False


        #calculations ----
        if holding_up:
            player.y_speed += player.jump_strength

        if holding_left:
            player.x_speed -= player.move_strength
        
        if holding_right:
            player.x_speed += player.move_strength

        player.calculate_physics()

        #do time-related things
        difficulty_timer += 1
        wall_timer += 1

        #do difficulty stuff
        if difficulty_timer >= DIFFICULTY_TIME_INTERVAL:
            difficulty += 0.1
            wall_frequency, wall_speed, shooter_chance = change_difficulty(difficulty)

            difficulty_timer = 0

        #create walls
        if wall_timer >= wall_frequency:
            if random.random() <= shooter_chance:
                Wall(wall_speed, Shooter(-100, -100, 20, Shooter.SP_normal))
            else:
                Wall(wall_speed)
            
            wall_timer = 0

        Wall.update_all()
        Shooter.update_all()
        Projectile.update_all()


        #draw stuff to the screen ----
        screen.fill(BLACK)

        player.draw()
        Wall.draw_all()
        Shooter.draw_all()
        Projectile.draw_all()
        hud.draw()
        
        if debug_shown:
            debug_info = f'''Difficulty info:
difficulty = {round(difficulty, 2)}

wall_frequency = {round(wall_frequency, 2)}
wall_speed = {round(wall_speed, 2)}
shooter_chance = {round(shooter_chance, 2)}

Player info:
x position: {round(player.x, 2)}
y position: {round(player.y, 2)}

x speed: {round(player.x_speed, 2)}
y speed: {round(player.y_speed, 2)}'''

            display_multiple_lines(debug_info, debug_text_rect, GREEN, 25)
            # debug_text = font.render(debug_info, True, WHITE)
            # screen.blit(debug_text, debug_text_rect)

        pygame.display.flip()

        #tick tock im the clock
        clock.tick(60)

        if player.health <= 0:
            pass#running = False
        


    return 'level_select'

# if __name__ == '__main__':
#     #this code is so messy and terrible wtf
#     #it work tho
#     import sys
#     from pathlib import Path
#     sys.path.append(str(Path(__file__).parent.parent))
#     print(sys.path)

#     from constants import constants
#     import pygame
#     screen = pygame.display.set_mode((constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT']), flags = pygame.SCALED | pygame.FULLSCREEN, vsync = 1)
#     pygame.init()
#     main(screen, constants)
#     pygame.quit