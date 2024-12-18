import pygame, math

DEBUG = {
    'total angles': 360,
    'non-transparency': False,
    'show rotated_cor': False,
    'show draw_cor': False
}

class SpriteStackModel(pygame.sprite.Sprite):
    def __init__(self, model_strip, dimensions, draw_offset=0, rotation_offset=0): # rotation in degrees
        pygame.sprite.Sprite.__init__(self)
        self.model_layers = []
        self.model_angles = {}
        self.layer_width = dimensions[0]
        self.layer_height = dimensions[1]
        self.layer_space = 1.0 # space in-between layers
        self.draw_offset = draw_offset

        self.total_angles = DEBUG['total angles']
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
        cut_cor = [0,0]
        while cut_cor[1] < model_strip.get_height():
            model_layer = self.cut_image(model_strip, cut_cor, self.layer_width, self.layer_height)
            self.model_layers.insert(0, model_layer)
            cut_cor[1] += self.layer_height
        
        for angle in range(self.total_angles):
            viewing_angle = angle * self.rotation_angle
            base_surf = pygame.Surface((self.layer_width, self.layer_height))
            base_surf = pygame.transform.rotate(base_surf, viewing_angle)
            render_surf = pygame.Surface((base_surf.get_width(), base_surf.get_height() + float(((len(self.model_layers)-1) * self.layer_space)) ))
            if not DEBUG['non-transparency']:
                render_surf.set_colorkey((0,0,0))

            for i, layer in enumerate(self.model_layers):
                rotated_layer = pygame.transform.rotate(layer, viewing_angle)
                render_surf.blit(rotated_layer, (0, float((len(self.model_layers)-1-i) * self.layer_space)))

            self.model_angles[angle] = render_surf

    def get_image(self, angle):
        img_angle = -math.degrees(angle) // self.rotation_angle + self.rotation_offset
        img_angle = int(img_angle % self.total_angles)
        return self.model_angles[img_angle]


class SingleLayerModel(SpriteStackModel):
    def __init__(self, image, model_height, draw_offset=0, rotation_offset=0): # rotation in degrees
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.model_angles = {}
        self.layer_width = image.get_width()
        self.layer_height = image.get_height()
        self.layer_space = 1.0 # space in-between layers
        self.model_height = model_height
        self.draw_offset = draw_offset

        self.total_angles = DEBUG['total angles']
        self.rotation_angle = 360 // self.total_angles 
        self.rotation_offset = (rotation_offset % 360) // self.rotation_angle

        self.render_model(image)

    def render_model(self, image):
        # self.model_layers = []
        # for i in range(self.model_height-1):
        #     model_layer = pygame.Surface((self.layer_width, self.layer_height))
        #     model_layer.fill((0,0,0))
        #     self.model_layers.append(model_layer)
        # self.model_layers.insert(0, image)
        
        for angle in range(self.total_angles):
            viewing_angle = angle * self.rotation_angle
            base_surf = pygame.Surface((self.layer_width, self.layer_height))
            base_surf = pygame.transform.rotate(base_surf, viewing_angle)
            render_surf = pygame.Surface((base_surf.get_width(), base_surf.get_height() + float(((self.model_height-1) * self.layer_space)) ))
            render_surf.fill((0,0,0))
            if not DEBUG['non-transparency']:
                render_surf.set_colorkey((0,0,0))

            # for i, layer in reversed(list(enumerate(self.model_layers))):
            #     rotated_layer = pygame.transform.rotate(layer, viewing_angle)
            #     render_surf.blit(rotated_layer, (0, float((self.model_height-1-i) * self.layer_space)))
            
            rotated_layer = pygame.transform.rotate(image, viewing_angle)
            render_surf.blit(rotated_layer, (0, float((self.model_height-1) * self.layer_space)))
            
            self.model_angles[angle] = render_surf


class ModelRender(pygame.sprite.Sprite):
    def __init__(self, cor, model):
        pygame.sprite.Sprite.__init__(self)
        self.cor = cor
        self.model = model
        self.image = self.model.get_image(0)
        self.rect = self.image.get_rect()
 
    def get_draw_cor(self, tile_size):
        return [self.cor[0]*tile_size, self.cor[1]*tile_size]
    
    def update_image(self, tile_size, camera):
        self.image = self.model.get_image(camera.compass)
        self.get_rect(tile_size, camera)
    
    def get_rect(self, tile_size, camera):
        current_cor = self.get_draw_cor(tile_size)
        current_cor[0] -= camera.camera_pos[0]
        current_cor[1] -= camera.camera_pos[1]
        rotated_cor = camera.rotate_vector(current_cor, camera.compass)

        draw_cor = [0,0]
        draw_cor[0] = rotated_cor[0] - self.image.get_width() // 2
        draw_cor[1] = rotated_cor[1] - self.image.get_height() // 2
        draw_cor[1] -= self.model.draw_offset

        #self.rect = self.image.get_rect(center=draw_cor)
        self.rect.x = draw_cor[0]
        self.rect.y = draw_cor[1]
        #self.rect.x -= camera.camera_pos[0]
        #self.rect.y -= camera.camera_pos[1]


class ObjectRender(pygame.sprite.Sprite):
    def __init__(self, cor, image):
        pygame.sprite.Sprite.__init__(self)
        self.cor = cor
        self.image = image
        self.rect = self.image.get_rect()
        self.draw_offset = [0,0]
 
    def get_draw_cor(self, tile_size):
        draw_cor = [0,0]
        draw_cor[0] = (self.cor[0] + self.draw_offset[0]) * tile_size
        draw_cor[1] = (self.cor[1] + self.draw_offset[1]) * tile_size
        return draw_cor
    
    def update_image(self, tile_size, camera):
        self.get_rect(tile_size, camera)
    
    def get_rect(self, tile_size, camera):
        current_cor = self.get_draw_cor(tile_size)
        current_cor[0] -= camera.camera_pos[0]
        current_cor[1] -= camera.camera_pos[1]
        rotated_cor = camera.rotate_vector(current_cor, camera.compass)

        draw_cor = [0,0]
        draw_cor[0] = rotated_cor[0] - self.image.get_width() // 2
        draw_cor[1] = rotated_cor[1] - self.image.get_height() // 2

        #self.rect = self.image.get_rect(center=draw_cor)
        self.rect.x = draw_cor[0]
        self.rect.y = draw_cor[1]
        #self.rect.x -= camera.camera_pos[0]
        #self.rect.y -= camera.camera_pos[1]