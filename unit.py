import pygame, models as _m

class Unit(pygame.sprite.Sprite):
    def __init__(self, spawn_cor):
        pygame.sprite.Sprite.__init__(self)
        self.id = 'Unit'
        self.state = 'idle'
        self.cor = spawn_cor.copy()
        self.prev_cor = spawn_cor.copy()
        self.direction = 0
        self.draw_offset = [0,0]
        self.draw_color = (255,255,255)
        self.image = pygame.Surface((32, 32))
        self.image.fill(self.draw_color)
        self.rect = self.image.get_rect()
        self.alpha = 255
        self.hit_flash_speed = 4
        
        self.stats = {
            'hp':1,
            'max_hp':1,
            'atk':1,
            'magic':1
        }

        self.stat_modifiers = {
            'hp':0,
            'max_hp':0,
            'atk':0,
            'magic':0
        }
        
        self.affinities = {
            'fire':0,
            'water':9,
            'ice':0,
            'electricity':0
        }

        self.state_timer = 0 # NEED TO IMPLEMENT DELTA TIME INTO THE MOVEMENT OR THE MOVEMENT TIMER
        self.state_durations = {
            'move':12,
            'attack_forward':8,
            'attack_backward':8,
            'hit':20,
            'destroy':30
        }

    def get_modified_stat(self, stat):
        return round(self.stats[stat] + max(0, (self.stats[stat] * self.stat_modifiers[stat])))
    
    def set_stat_modifier(self, stat, value):
        self.stat_modifiers[stat] += float(value)

    def set_state(self, state):
        self.state = state
        self.state_timer = self.state_durations[state]

    def set_direction(self, target_cor):
        x_distance = abs(target_cor[0] - self.cor[0])
        y_distance = abs(target_cor[1] - self.cor[1])

        # diagonal directions
        if x_distance == y_distance and target_cor[0] > self.cor[0] and target_cor[1] < self.cor[1]:
            self.direction = 1
        elif x_distance == y_distance and target_cor[0] > self.cor[0] and target_cor[1] > self.cor[1]:
            self.direction = 3
        elif x_distance == y_distance and target_cor[0] < self.cor[0] and target_cor[1] > self.cor[1]:
            self.direction = 5
        elif x_distance == y_distance and target_cor[0] < self.cor[0] and target_cor[1] < self.cor[1]:
            self.direction = 7

        # cardinal directions
        elif x_distance < y_distance and target_cor[1] < self.cor[1]:
            self.direction = 0
        elif x_distance > y_distance and target_cor[0] > self.cor[0]:
            self.direction = 2
        elif x_distance < y_distance and target_cor[1] > self.cor[1]:
            self.direction = 4
        elif x_distance > y_distance and target_cor[0] < self.cor[0]:
            self.direction = 6

    def move(self, next_cor):
        if self.cor != next_cor:
            self.prev_cor = self.cor.copy()
            self.cor = next_cor.copy()
            self.set_state('move')

    def attack(self):
        self.set_state('attack_forward')

    def hit(self, damage):
        self.stats['hp'] -= damage
        self.set_state('hit')

    def destroy(self):
        self.set_state('destroy')

    def update_state(self):
        if self.state != 'idle':
            self.state_timer = max(0, self.state_timer-1)
            if self.state_timer == 0:
                if self.state == 'attack_forward':
                    self.set_state('attack_backward')
                else:
                    self.state = 'idle'
                    self.alpha = 255
                    self.draw_offset = [0,0]
                return True
        return False
    
    def update_animation(self):
        if self.state == 'idle':
            self.draw_offset = [0,0]

        if self.state == 'move':
            x_distance = self.cor[0] - self.prev_cor[0]
            y_distance = self.cor[1] - self.prev_cor[1]
            proportion_traveled = float(self.state_timer / self.state_durations['move'])
            self.draw_offset = [(x_distance * proportion_traveled) * -1, (y_distance * proportion_traveled) * -1]

        if self.state == 'attack_forward':
            dir_x = [0,1,1,1,0,-1,-1,-1]
            dir_y = [-1,-1,0,1,1,1,0,-1]
            next_cor = [self.cor[0]+dir_x[self.direction], self.cor[1]+dir_y[self.direction]]
            x_distance = float((next_cor[0] - self.cor[0]) / 2)
            y_distance = float((next_cor[1] - self.cor[1]) / 2)
            proportion_traveled = 1 - float(self.state_timer / self.state_durations['attack_forward'])
            self.draw_offset = [(x_distance * proportion_traveled), (y_distance * proportion_traveled)]

        if self.state == 'attack_backward':
            dir_x = [0,1,1,1,0,-1,-1,-1]
            dir_y = [-1,-1,0,1,1,1,0,-1]
            next_cor = [self.cor[0]+dir_x[self.direction], self.cor[1]+dir_y[self.direction]]
            x_distance = float((next_cor[0] - self.cor[0]) / 2)
            y_distance = float((next_cor[1] - self.cor[1]) / 2)
            proportion_traveled = float(self.state_timer / self.state_durations['attack_forward'])
            self.draw_offset = [(x_distance * proportion_traveled), (y_distance * proportion_traveled)]

        if self.state == 'hit':
            if self.state_timer % self.hit_flash_speed == 0:
                self.alpha = 0 if self.alpha == 255 else 255

        if self.state == 'destroy':
            self.alpha = 255 * float(self.state_timer / self.state_durations['destroy'])
    
    def get_draw_cor(self, tile_size):
        draw_cor = [0,0]
        draw_cor[0] = (self.cor[0] + self.draw_offset[0]) * tile_size
        draw_cor[1] = (self.cor[1] + self.draw_offset[1]) * tile_size
        return draw_cor

    def update_image(self, tile_size, camera):
        self.image.set_alpha(self.alpha)
        self.get_rect(tile_size, camera)
    
    def get_rect(self, tile_size, camera):
        current_cor = self.get_draw_cor(tile_size)
        current_cor[0] -= camera.camera_pos[0]
        current_cor[1] -= camera.camera_pos[1]
        rotated_cor = camera.rotate_vector(current_cor, camera.compass)

        draw_cor = [0,0]
        draw_cor[0] = rotated_cor[0] - self.image.get_width() // 2
        draw_cor[1] = rotated_cor[1] - self.image.get_height() // 2

        #self.rect = self.image.get_rect(center = draw_cor)
        self.rect.x = draw_cor[0]
        self.rect.y = draw_cor[1]
        #self.rect.x -= camera.camera_pos[0]
        #self.rect.y -= camera.camera_pos[1]
    