import pygame, time, sys, math, random
import inputreader as _ir, soundmanager as _s, camera as _c, customfont as _font, transitions as _t
import floormanager as _fm, hud as _h

# -- INIT
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.joystick.init()
pygame.mixer.set_num_channels(300)
pygame.display.set_caption('Cyber Mystery Dungeon')
WINDOW_SIZE = (640, 360)
CAMERA_SIZE = (480, 270) #(320, 180)
FPS = 60
window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
camera = _c.Camera(CAMERA_SIZE)
clock = pygame.time.Clock()
input = _ir.InputReader()
sounds = _s.SoundManager('sounds/')

#classic_font = _font.CustomFont(pygame.image.load('fonts/font_classic.png'))
future_font = pygame.font.Font('fonts/ORGAN___.TTF', 8)

class GameLoop:
    def __init__(self):
        self.Run = True
        self.clock_last_time = time.time()
        self.clock_dT = 0

    def run(self):
        self.Run = True
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

        self.transition = _t.Transition(CAMERA_SIZE, 'out', 30, (0,0,0))
        self.flrmgr = _fm.FloorManager('The Terminal', sounds)
        self.hud = _h.Hud(CAMERA_SIZE, self.flrmgr)
        floor_properties = { # mystery dungeon maps are around 56 x 72 units in size
            'floor_width': 30,
            'floor_height': 25,
            'tile_size': 31,
            'max_rooms': 5,
            'min_room_size':[5,5],
            'max_room_size':[10,10],
            'max_room_area': 35,
            'max_path_size': 7,
            'num_shortcuts': 3,
            'shortcut_threshold': 20
        }
        self.flrmgr.set_floor_properties(floor_properties)
        self.flrmgr.generate_new_floor()
        if self.DEBUG['visible_minimap']:
            self.flrmgr.visibility_map = self.flrmgr.floor.generate_empty_map(1)
        #self.flrmgr.floor.print_map(flrmgr.floor.room_map)

        #sounds.play_music('mm8-frost-man.wav', 1000)
        sounds.play_music('mm8-opening.wav')
        #sounds.play_music('azali-outer-space-carnival.wav', 3000)

        self.dungeon_intro = DungeonIntroduction(self.flrmgr)
        self.dungeon_intro.run()

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
        
        if input.iskeydown('left shift') or input.isbuttonpressed(6):
            self.flrmgr.text_log.visibility = not self.flrmgr.text_log.visibility
            self.hud.minimap_visibility = not self.hud.minimap_visibility

        if input.iskeypressed('tab') or input.isbuttonpressed(15):
            self.flrmgr.to_next_floor = True

    def update(self):
        if not self.flrmgr.to_next_floor:
            self.flrmgr.read_input(input, camera)

        if self.flrmgr.to_next_floor and self.transition.fade != 'in':
            self.transition.fade_in()

        self.flrmgr.update_objects()
        camera.follow_unit(self.flrmgr.get_player(), self.flrmgr.floor.tile_size)
        camera.update()
        self.flrmgr.update_menus()
        self.flrmgr.update_sprites(camera)
        self.hud.update()

        self.transition.update()

        if self.transition.end and self.transition.fade == 'in':
            self.flrmgr.generate_new_floor()
            if self.DEBUG['visible_minimap']:
                self.flrmgr.visibility_map = self.flrmgr.floor.generate_empty_map(1)
            #self.flrmgr.floor.print_map(flrmgr.floor.room_map)
            self.dungeon_intro.run()
            self.transition.fade_out()
            camera.set_angle(camera.start_angle)

    def draw(self):
        self.flrmgr.floor_sprite_group.draw(camera.surf)
        self.flrmgr.trap_sprite_group.draw(camera.surf)
        self.flrmgr.obj_sprite_group.draw(camera.surf)
        camera.draw_to_screen(self.hud.draw(), (0, 0))

        for menu in self.flrmgr.active_menus:
            camera.draw_to_screen(menu.draw(), menu.draw_cor)

        # --- code to display compass onto the screen
        # compass_needle = pygame.transform.rotate(pygame.image.load('sprites/compass_needle.png'), -math.degrees(camera.compass))
        # compass_circle = pygame.image.load('sprites/compass_circle.png')
        # compass_directions = pygame.image.load('sprites/compass_directions.png')
        # draw_pos = [CAMERA_SIZE[0]-28, 27]
        # draw_pos[0] -= compass_directions.get_width()//2
        # draw_pos[1] -= compass_directions.get_height()//2
        # camera.draw_to_screen(compass_directions, draw_pos)
        # draw_pos = [CAMERA_SIZE[0]-28, 27]
        # draw_pos[0] -= compass_circle.get_width()//2
        # draw_pos[1] -= compass_circle.get_height()//2
        # camera.draw_to_screen(compass_circle, draw_pos)
        # draw_pos = [CAMERA_SIZE[0]-28, 27]
        # draw_pos[0] -= compass_needle.get_width()//2
        # draw_pos[1] -= compass_needle.get_height()//2
        # camera.draw_to_screen(compass_needle, draw_pos)

        camera.draw_to_screen(self.transition.draw(), (0, 0))

    def end(self):
        super().end()
        if self.DEBUG['framerate']:
            print(clock.get_fps())


class DungeonIntroduction(GameLoop):
    def __init__(self, floormanager):
        super().__init__()
        self.floormanager = floormanager
        self.transition = _t.Transition(CAMERA_SIZE, 'out', 60, (0,0,0))
        self.font = pygame.font.Font('fonts/ORGAN___.TTF', 7)
        self.font_color = (255, 255, 255)
        self.text_timer = 60

    def run(self):
        self.transition.fade_out()
        self.text_timer = 60
        super().run()

    def update(self):
        camera.update()
        self.transition.update()

        if self.transition.end and self.transition.fade == 'out':
            self.text_timer -= 1
            if self.text_timer <= 0:
                self.transition.fade_in()
    
        elif self.transition.end and self.transition.fade == 'in':
            self.Run = False
    
    def draw(self):
        center_screen = camera.get_center_screen()

        dungeon_name_size = self.font.size(self.floormanager.dungeon_name)
        dungeon_name_pos = (center_screen[0] - (dungeon_name_size[0]/2), center_screen[1] - (dungeon_name_size[1]/2) - self.font.get_linesize())
        camera.draw_to_screen(self.font.render(self.floormanager.dungeon_name, False, self.font_color), dungeon_name_pos)
        
        floor_number_size = self.font.size('Floor ' + str(self.floormanager.floor_number))
        floor_number_pos = (center_screen[0] - (floor_number_size[0]/2), center_screen[1] - (floor_number_size[1]/2) + self.font.get_linesize())
        camera.draw_to_screen(self.font.render('Floor ' + str(self.floormanager.floor_number), False, self.font_color), floor_number_pos)
        
        camera.draw_to_screen(self.transition.draw(), (0, 0))
        



    