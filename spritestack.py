import pygame, math

DEBUG = {
    'transparency': True,
    'show rotated_cor': True,
    'show draw_cor': True
}

class SpriteStack(pygame.sprite.Sprite):
    def __init__(self, spawn_cor, model_strip, dimensions, draw_offset=0, rotation_offset=0): # rotation in degrees
        pygame.sprite.Sprite.__init__(self)
        self.cor = spawn_cor
        self.image = pygame.Surface((0,0))
        self.rect = self.image.get_rect()
        self.layers = []
        self.layer_width = dimensions[0]
        self.layer_height = dimensions[1]
        self.layer_offset = 1.0
        self.draw_offset = draw_offset
        self.render_cache = {}

        self.total_angles = 360
        self.rotation_angle = 360 // self.total_angles 
        self.rotation_offset = (rotation_offset % 360) // self.rotation_angle
        self.render_model(model_strip)
    
    def cut_image(self,surf,cor,width,height):
        surf_copy = surf.copy()
        clip = pygame.Rect(cor[0], cor[1], width, height)
        surf_copy.set_clip(clip)
        cut = surf.subsurface(surf_copy.get_clip())
        return cut.copy()
    
    def render_model(self, model_strip):
        cut_cor = [0, 0]
        while cut_cor[1] < model_strip.get_height():
            model_layer = self.cut_image(model_strip, cut_cor, self.layer_width, self.layer_height)
            self.layers.insert(0, model_layer)
            cut_cor[1] += self.layer_height

        for angle in range(self.total_angles):
            viewing_angle = angle * self.rotation_angle
            base_surf = pygame.Surface((self.layer_width, self.layer_height))
            base_surf = pygame.transform.rotate(base_surf, viewing_angle)
            render_surf = pygame.Surface((base_surf.get_width(), base_surf.get_height() + float(((len(self.layers)-1) * self.layer_offset)) ))
            if DEBUG['transparency']:
                render_surf.set_colorkey((0,0,0))

            for i, layer in enumerate(self.layers):
                rotated_layer = pygame.transform.rotate(layer, viewing_angle)
                render_surf.blit(rotated_layer, (0, float((len(self.layers)-1-i) * self.layer_offset)))

            self.render_cache[angle] = render_surf

    def update_model(self, camera):
        angle = -math.degrees(camera.compass) // self.rotation_angle + self.rotation_offset
        angle = int(angle % self.total_angles)
        self.image = self.render_cache[angle]

        current_cor = self.cor.copy()
        current_cor[0] -= camera.camera_pos[0]
        current_cor[1] -= camera.camera_pos[1]
        rotated_cor = camera.rotate_vector(current_cor, camera.compass)

        draw_cor = [0,0]
        draw_cor[0] = rotated_cor[0] - self.image.get_width() // 2
        draw_cor[1] = rotated_cor[1] - self.image.get_height() // 2
        draw_cor[1] -= self.draw_offset

        self.rect = self.image.get_rect()
        self.rect.x = draw_cor[0]
        self.rect.y = draw_cor[1]

        # if DEBUG['show rotated_cor']:
        #     pygame.draw.circle(camera.surf, (0,0,255), rotated_cor, 1)
        # if DEBUG['show draw_cor']:
        #     pygame.draw.circle(camera.surf, (0,255,0), draw_cor, 1)

