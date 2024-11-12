import pygame, time, sys, math, random
import inputreader as _ir, camera as _c, customfont as _font
import floormanager as _fm, hud as _h

# -- INIT
pygame.mixer.pre_init()
pygame.init()
pygame.joystick.init()
pygame.mixer.set_num_channels(300)
pygame.display.set_caption('mystery dungeon')
WINDOW_SIZE = (640, 360)
CAMERA_SIZE = (480, 270) #(320, 180)
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
        pygame.display.update()
        clock.tick(FPS)


class MainLoop(GameLoop):
    def __init__(self):
        super().__init__()

        self.DEBUG = {
            'framerate': False,
            'visible_traps': False,
            'visible_minimap': False
        }
    
        self.flrmgr = _fm.FloorManager('Mystery Dungeon')
        self.hud = _h.Hud(CAMERA_SIZE, self.flrmgr)
        floor_properties = { # mystery dungeon maps are around 56 x 72 units in size
            'floor_width': 30,
            'floor_height': 30,
            'tile_size': 31,
            'max_rooms': 7,
            'max_room_area': 35,
            'max_path_size': 4,
            'num_shortcuts': 5,
            'shortcut_threshold': 20
        }
        self.flrmgr.set_floor_properties(floor_properties)
        self.flrmgr.generate_new_floor()
        if self.DEBUG['visible_minimap']:
            self.flrmgr.visibility_map = self.flrmgr.floor.generate_empty_map(1)
        #self.flrmgr.floor.print_map(flrmgr.floor.room_map)

    def read_events(self):
        super().read_events()

        if input.iskeydown('a') or input.isbuttondown('right stick left'):
            scale_factor = abs(input.get_axis_value('right stick left')) if input.isbuttondown('right stick left') else 1
            camera.turn_clockwise(scale_factor)
        
        if input.iskeydown('d') or input.isbuttondown('right stick right'):
            scale_factor = abs(input.get_axis_value('right stick right')) if input.isbuttondown('right stick right') else 1
            camera.turn_counterclockwise(scale_factor)
        
        if input.iskeypressed('q') or input.isbuttonpressed(4):
            camera.snap_clockwise()

        if input.iskeypressed('e') or input.isbuttonpressed(5):
            camera.snap_counterclockwise()

        if input.iskeypressed('tab') or input.isbuttonpressed(15):
            self.flrmgr.generate_new_floor()
            if self.DEBUG['visible_minimap']:
                self.flrmgr.visibility_map = self.flrmgr.floor.generate_empty_map(1)

    def update(self):
        self.flrmgr.read_input(input, camera)
        self.flrmgr.update_objects()
        camera.follow_unit(self.flrmgr.get_player(), self.flrmgr.floor.tile_size)
        camera.update()
        self.flrmgr.update_sprites(camera)
        self.hud.update()

    def draw(self):
        self.flrmgr.floor_sprite_group.draw(camera.surf)
        self.flrmgr.trap_sprite_group.draw(camera.surf)
        self.flrmgr.obj_sprite_group.draw(camera.surf)
        camera.draw_to_screen(self.hud.draw(), (0, 0))

        for menu in self.flrmgr.active_menus:
            camera.draw_to_screen(menu.draw(), menu.draw_cor)

    def end(self):
        super().end()
        if self.DEBUG['framerate']:
            print(clock.get_fps())
