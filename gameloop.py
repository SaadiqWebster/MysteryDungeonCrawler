import pygame, time, sys, math, random
import inputreader as _ir, camera as _c, customfont as _font
import spritestack as _ss
import floormanager as _fm, hud as _h, minimap as _m

# -- INIT
pygame.mixer.pre_init()
pygame.init()
pygame.joystick.init()
pygame.mixer.set_num_channels(300)
pygame.display.set_caption('mystery dungeon')
WINDOW_SIZE = (320, 180)
CAMERA_SIZE = (320, 180)
FPS = 60
window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
camera = _c.Camera(CAMERA_SIZE)
clock = pygame.time.Clock()
input = _ir.InputReader()

#classic_font = _font.CustomFont(pygame.image.load('fonts/font_classic.png'))
future_font = pygame.font.Font('fonts/ORGAN___.TTF', 8)

class GameLoop:
    def __init__(self):
        self.Run = True
        self.clock_last_time = time.time()
        self.clock_dT = 0

    def run(self):
        while self.Run:
            self.start()
            self.read_events()
            self.update()
            self.draw()
            self.end()

    def start(self):
        camera.clear()
        self.clock_dT = (time.time()-self.clock_last_time) * 60 # frame-rate independence, display locked at 60 FPS
        self.clock_last_time = time.time()

    def read_events(self):
        input.refresh()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            input.read_event(event)

    def update(self):
        pass

    def draw(self):
        pass

    def end(self):
        scaled_camera_size = [window.get_height() * float(camera.camera_size[0] / camera.camera_size[1]), window.get_width() * float(camera.camera_size[1] / camera.camera_size[0])]
        if window.get_width() < scaled_camera_size[0]:
            scaled_camera_size[0] = window.get_width()
        else:
            scaled_camera_size[1] = window.get_height()
        window.blit(pygame.transform.scale(camera.draw(), scaled_camera_size), ((window.get_width() / 2) - (scaled_camera_size[0] / 2), (window.get_height() / 2) - (scaled_camera_size[1] / 2)))
        # --- for some reason pygame.transform.scale lowers the performance when the screen is larger. use the below line if perfrormance is too jarring ----
        #window.blit(camera.draw(), ((window.get_width() / 2) - (scaled_camera_size[0] / 2), (window.get_height() / 2) - (scaled_camera_size[1] / 2)))
        pygame.display.update()
        clock.tick(FPS)
        print(clock.get_fps())

class MainLoop(GameLoop):
    def __init__(self):
        super().__init__()

        self.DEBUG = {
            'zoom_in': True,
            'visible_traps': False
        }
        camera.toggle_zoom(self.DEBUG['zoom_in'])
        
        self.flrmgr = _fm.FloorManager('Mystery Dungeon')
        self.hud = _h.Hud(CAMERA_SIZE, self.flrmgr)
        floor_properties = { # mystery dungeon maps are around 56 x 72 units in size
            'floor_width': 30,
            'floor_height': 30,
            'max_rooms': 7,
            'max_room_area': 35,
            'max_path_size': 4,
            'num_shortcuts': 5,
            'shortcut_threshold': 20
        }
        self.flrmgr.set_floor_properties(floor_properties)
        self.flrmgr.generate_new_floor()
        #self.flrmgr.floor.print_map(flrmgr.floor.room_map)

    def read_events(self):
        super().read_events()
        
        if input.iskeypressed('tab') or input.isbuttonpressed(6):
            self.flrmgr.generate_new_floor()
        
        if input.iskeypressed('left shift') or input.isbuttonpressed(15):
            self.DEBUG['zoom_in'] = not self.DEBUG['zoom_in']
            camera.toggle_zoom(self.DEBUG['zoom_in'])

    def update(self):
        self.flrmgr.read_input(input)
        self.flrmgr.update_objects()
        self.hud.update()


        if not self.DEBUG['zoom_in']:
            camera.set_position([0,0])
        else:
            player = self.flrmgr.get_player()
            camera.follow_unit(player)

    def draw(self):
        for x in range(self.flrmgr.floor.floor_width):
            for y in range(self.flrmgr.floor.floor_height):
                cor = [x,y]
                tile_color = (75,75,75) if self.flrmgr.floor.get_tile_signature(cor) != '11111111' else (150,150,150)
                map_value = self.flrmgr.floor.get_floor_map(cor)
                if map_value == 1:
                    tile_color = (0,0,255)
                if map_value == 2:
                    tile_color = (255,0,0)
                if map_value == 3:
                    tile_color = (0,255,0)
                if map_value == 4:
                    tile_color = (255,0,255)
                if map_value == 5:
                    tile_color = (0,255,255)
                tile = pygame.Surface(((camera.tile_size-1, camera.tile_size-1)))
                tile.fill(tile_color)
                camera.draw_tile(tile, cor)

        stairs_draw_color = (255,0,255)
        tile = pygame.Surface(((camera.tile_size-1, camera.tile_size-1)))
        tile.fill(stairs_draw_color)
        camera.draw_tile(tile, self.flrmgr.stairs_cor)

        for trap_id in self.flrmgr.traps:
            trap = self.flrmgr.get_trap(trap_id)
            if trap.visible or self.DEBUG['visible_traps']:
                tile = pygame.Surface(((camera.tile_size-1, camera.tile_size-1)))
                tile.fill(trap.draw_color)
                camera.draw_tile(tile, trap.draw())

        for item_id in self.flrmgr.items:
            item = self.flrmgr.get_item(item_id)
            tile = pygame.Surface(((camera.tile_size-1, camera.tile_size-1)))
            tile.fill(item.draw_color)
            camera.draw_tile(tile, item.draw())
        
        for unit_id in self.flrmgr.units:
            unit = self.flrmgr.get_unit(unit_id)
            tile = pygame.Surface(((camera.tile_size-1, camera.tile_size-1)))
            tile.fill(unit.draw_color)

            tile.set_alpha(unit.alpha)
            camera.draw_tile(tile, unit.draw())

        for item_id in self.flrmgr.thrown_items:
            item = self.flrmgr.get_item(item_id)
            tile = pygame.Surface(((camera.tile_size-1, camera.tile_size-1)))
            tile.fill(item.draw_color)
            camera.draw_tile(tile, item.draw())

        camera.draw_to_screen(self.hud.draw(), (0, 0))

        for menu in self.flrmgr.active_menus:
            camera.draw_to_screen(menu.draw(), menu.draw_cor)

class SpriteStackLoop(GameLoop):
    def __init__(self):
        super().__init__()
        self.movement_speed = 1
        self.velocity = [0,0]
        deer_model_strip = pygame.image.load('models/deer.png')
        knight_model_strip = pygame.image.load('models/chr_knight.png')
        spawn_cor = camera.get_center_position()
        spawn_cor[1] -= 50
        self.deer1 = _ss.SpriteStack(spawn_cor, deer_model_strip, (16, 9), 13)
        spawn_cor = camera.get_center_position()
        spawn_cor[1] += 50
        self.deer2 = _ss.SpriteStack(spawn_cor, knight_model_strip, (20, 21), 13)

    def start(self):
        super().start()
        self.velocity = [0,0]

    def read_events(self):
        super().read_events()

        if input.iskeydown('a') or input.isbuttondown('right stick left'):
            camera.compass -= 0.05
        if input.iskeydown('d') or input.isbuttondown('right stick right'):
            camera.compass += 0.05
        
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

    def draw(self):
        pygame.draw.circle(camera.surf, (255,0,0), camera.get_center_screen(), 4)
        self.deer1.draw(camera)
        self.deer2.draw(camera)

        # uncomment to draw each layer of model
        # camera.clear()
        # draw_cor = [0, 0]
        # for i, layer in enumerate(self.deer1.layers):
        #     camera.draw_to_screen(layer, draw_cor)
        #     draw_cor[1] += self.deer1.layer_height



# FOR TESTING ONLY, COMMENT TO PUT AWAY
if __name__ == "__main__":
    gameloop = SpriteStackLoop()
    gameloop.run()

