import pygame, math

class Camera():
    def __init__(self, CAMERA_SIZE):
        self.camera_size = CAMERA_SIZE
        self.surf = pygame.Surface(self.camera_size)
        self.camera_pos = [0,0]
        self.fill_color = (100,100,100) #(100,100,100)
        self.compass = 0 # in radians
        
        # DEBUG
        self.tile_size = 3 # when units are a fixed size, this will no longer be needed

    def get_center_screen(self):
        return [float(self.camera_size[0] / 2), float(self.camera_size[1] / 2)]
    
    def get_center_position(self):
        return [self.camera_pos[0] + float(self.camera_size[0] / 2), self.camera_pos[1] + float(self.camera_size[1] / 2)]

    def set_position(self, cor):
        self.camera_pos = cor.copy()

    def clear(self):
        self.surf.fill(self.fill_color)

    def toggle_zoom(self, ZOOM_IN):
        self.tile_size = 20 if ZOOM_IN else 3

    # angle must be in radians
    def rotate_vector(self, vector, angle):
        rotated_cor = [0,0]
        pivot = self.get_center_screen()
        vector[0] -= pivot[0]
        vector[1] -= pivot[1]
        rotated_cor[0] = float((vector[0] * math.cos(angle)) - (vector[1] * math.sin(angle)))
        rotated_cor[1] = float((vector[0] * math.sin(angle)) + (vector[1] * math.cos(angle)))
        rotated_cor[0] += pivot[0]
        rotated_cor[1] += pivot[1]
        return rotated_cor

    def follow_unit(self, unit):
        if unit is not None and unit.state != 'attack_forward' and unit.state != 'attack_backward':
            unit_draw_cor = unit.draw()
            camera_pos_x = (unit_draw_cor[0]*self.tile_size)-(self.camera_size[0]/2)+(self.tile_size/2)
            camera_pos_y = (unit_draw_cor[1]*self.tile_size)-(self.camera_size[1]/2)+(self.tile_size/2)
            self.set_position([camera_pos_x, camera_pos_y])

    def draw_tile(self, tile, cor):
        self.surf.blit(tile, ((cor[0]*self.tile_size)-self.camera_pos[0], (cor[1]*self.tile_size)-self.camera_pos[1]))
    
    def draw_to_screen(self, img, cor):
        self.surf.blit(img, cor)
    
    def draw(self):
        return self.surf
