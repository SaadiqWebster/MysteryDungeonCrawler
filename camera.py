import pygame, math

class Camera():
    def __init__(self, CAMERA_SIZE):
        self.camera_size = CAMERA_SIZE
        self.surf = pygame.Surface(self.camera_size)
        self.camera_pos = [0,0]
        self.fill_color = (0,0,0) #(3, 157, 252)
        self.compass = round(float(math.pi/4), 7) # in radians
        self.target_compass = self.compass
        self.snap_angle = round(float(math.pi/4), 7)
        self.turn_speed = 0.04
        self.ease_speed = 8

    def get_center_screen(self):
        return [float(self.camera_size[0] / 2), float(self.camera_size[1] / 2)]
    
    def get_center_position(self):
        return [self.camera_pos[0] + float(self.camera_size[0] / 2), self.camera_pos[1] + float(self.camera_size[1] / 2)]

    def set_position(self, cor):
        self.camera_pos = cor.copy()

    def clear(self):
        self.surf.fill(self.fill_color)

    def turn_clockwise(self, scale_factor=1):
        self.target_compass -= round(self.turn_speed * scale_factor, 7)

    def turn_counterclockwise(self, scale_factor=1):
        self.target_compass += round(self.turn_speed * scale_factor, 7)
    
    def snap_clockwise(self):
        mod = round(self.target_compass % self.snap_angle, 7)
        angle = self.snap_angle if mod == 0.00 else mod
        self.target_compass -= angle

    def snap_counterclockwise(self):
        mod = round(self.target_compass % self.snap_angle, 7)
        angle = 0 if mod == self.snap_angle else mod
        self.target_compass += self.snap_angle - angle

    def rotate_vector(self, vector, angle): # angle must be in radians
        rotated_cor = [0,0]
        pivot = self.get_center_screen()
        vector[0] -= pivot[0]
        vector[1] -= pivot[1]
        rotated_cor[0] = float((vector[0] * math.cos(angle)) - (vector[1] * math.sin(angle)))
        rotated_cor[1] = float((vector[0] * math.sin(angle)) + (vector[1] * math.cos(angle)))
        rotated_cor[0] += pivot[0]
        rotated_cor[1] += pivot[1]
        return rotated_cor

    def follow_unit(self, unit, tile_size):
        if unit is not None and unit.state != 'attack_forward' and unit.state != 'attack_backward':
            unit_draw_cor = unit.get_draw_cor(tile_size)
            unit_draw_cor[0] -= float(unit.image.get_height() / 2)
            unit_draw_cor[1] -= float(unit.image.get_width() / 2)
            camera_pos_x = unit_draw_cor[0]-(self.camera_size[0]/2)+(unit.image.get_width()/2)
            camera_pos_y = unit_draw_cor[1]-(self.camera_size[1]/2)+(unit.image.get_height()/2)
            self.set_position([camera_pos_x, camera_pos_y])

    def update(self):
        self.compass += round((self.target_compass - self.compass) / self.ease_speed, 3)

    def draw_tile(self, tile, cor, tile_size):
        self.surf.blit(tile, ((cor[0]*tile_size)-self.camera_pos[0], (cor[1]*tile_size)-self.camera_pos[1]))
    
    def draw_to_screen(self, img, cor):
        self.surf.blit(img, cor)
    
    def draw(self):
        return self.surf

