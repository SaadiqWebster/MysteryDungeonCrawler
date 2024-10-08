import pygame, math
from gameloop import *
import models as _m

class SpriteStackTestLoop(GameLoop):
    def __init__(self):
        super().__init__()

        self.movement_speed = 1
        self.velocity = [0,0]
        
        deer_model_strip = pygame.image.load('models/deer.png')
        knight_model_strip = pygame.image.load('models/chr_knight.png')

        camera_center = camera.get_center_position()
        spawn_cor = [camera_center[0], camera_center[1]-50]
        self.deer1 = _m.SpriteStackModel(spawn_cor, deer_model_strip, (16, 9), 13)
        spawn_cor = [camera_center[0]-10, camera_center[1]-60]
        self.deer2 = _m.SpriteStackModel(spawn_cor, deer_model_strip, (16, 9), 13)
        spawn_cor = [camera_center[0]+10, camera_center[1]-60]
        self.deer3 = _m.SpriteStackModel(spawn_cor, deer_model_strip, (16, 9), 13)
        
        camera_center = camera.get_center_position()
        spawn_cor = [camera_center[0], camera_center[1]+50]
        self.knight1 = _m.SpriteStackModel(spawn_cor, knight_model_strip, (20, 21), 13)
        spawn_cor = [camera_center[0]-10, camera_center[1]+60]
        self.knight2 = _m.SpriteStackModel(spawn_cor, knight_model_strip, (20, 21), 13)
        spawn_cor = [camera_center[0]+10, camera_center[1]+60]
        self.knight3 = _m.SpriteStackModel(spawn_cor, knight_model_strip, (20, 21), 13)

        self.sprite_group = pygame.sprite.LayeredUpdates()
        self.sprite_group.add(self.deer1)
        self.sprite_group.add(self.deer2)
        self.sprite_group.add(self.deer3)
        self.sprite_group.add(self.knight1)
        self.sprite_group.add(self.knight2)
        self.sprite_group.add(self.knight3)

    def start(self):
        super().start()
        self.velocity = [0,0]

    def read_events(self):
        super().read_events()

        if input.iskeydown('a') or input.isbuttondown('right stick left'):
            camera.turn_counterclockwise()
        if input.iskeydown('d') or input.isbuttondown('right stick right'):
            camera.turn_clockwise()
        
        if input.iskeydown('up') or input.isbuttondown('left stick up') or input.isbuttondown(11):
            self.velocity[1] -= self.movement_speed
        if input.iskeydown('down')  or input.isbuttondown('left stick down') or input.isbuttondown(12):
            self.velocity[1] += self.movement_speed
        if input.iskeydown('left')  or input.isbuttondown('left stick left') or input.isbuttondown(13):
            self.velocity[0] -= self.movement_speed
        if input.iskeydown('right')  or input.isbuttondown('left stick right') or input.isbuttondown(14):
            self.velocity[0] += self.movement_speed
        
        if self.velocity[0] > 0 and self.velocity[1] > 0:
            self.velocity[0] *= 1 / math.sqrt(2)
            self.velocity[1] *= 1 / math.sqrt(2)

    def update(self):
        rotated_velocity = [0,0]
        if self.velocity != [0,0]:
            rotated_velocity[0] = float((self.velocity[0] * math.cos(-camera.compass)) - (self.velocity[1] * math.sin(-camera.compass)))
            rotated_velocity[1] = float((self.velocity[0] * math.sin(-camera.compass)) + (self.velocity[1] * math.cos(-camera.compass)))
            magnitude = float(math.sqrt(self.velocity[0]**2 + self.velocity[1]**2))
            rotated_velocity[0] /= magnitude
            rotated_velocity[1] /= magnitude
        camera.camera_pos[0] += rotated_velocity[0]
        camera.camera_pos[1] += rotated_velocity[1]

        for sprite in self.sprite_group.sprites():
            sprite.update_model(camera)
            self.sprite_group.change_layer(sprite, sprite.rect.y)

    def draw(self):
        pygame.draw.circle(camera.surf, (255,0,0), camera.get_center_screen(), 4)
        self.sprite_group.draw(camera.surf)

        # uncomment to draw each layer of model
        # camera.clear()
        # draw_cor = [0, 0]
        # for i, layer in enumerate(self.deer1.layers):
        #     camera.draw_to_screen(layer, draw_cor)
        #     draw_cor[1] += self.deer1.layer_height


if __name__ == "__main__":
    gameloop = SpriteStackTestLoop()
    gameloop.run()

