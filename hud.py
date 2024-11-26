import pygame, math
import textlog as _l, minimap as _m

class Hud:
    def __init__(self, CAMERA_SIZE, floormanager):
        self.screen_size = CAMERA_SIZE
        self.floormanager = floormanager
        self.font = pygame.font.Font('fonts/ORGAN___.TTF', 7)
        self.font_color = (255, 255, 255)
        self.background_alpha = 0
        self.player_name = ''
        self.player_stats = {'hp':1,'max_hp':1,'sp':1,'max_sp':1,'en':1,'max_en':1,}
        self.minimap = _m.Minimap(self.floormanager)
        self.minimap_visibility = True

    def update(self):
        self.minimap.update()

        #self.textlog_visibility = self.floormanager.get_active_menu() is None
        #self.minimap_visibility = self.floormanager.get_active_menu() is None

        for unit_id in self.floormanager.units:
            unit = self.floormanager.units[unit_id]

            if unit_id == self.floormanager.player_id:
                self.player_name = unit.id
                self.player_stats = unit.stats

    def draw(self):
        screen_surf = pygame.Surface(self.screen_size)
        screen_surf.fill((0,0,0))
        screen_surf.set_colorkey((0,0,0))

        if self.minimap_visibility:
            minimap_surf = self.minimap.draw()
            minimap_pos = (self.screen_size[0] - minimap_surf.get_width() - 40, 45)
            screen_surf.blit(minimap_surf, minimap_pos)

        if self.floormanager.text_log.visibility:
            textlog_surf = self.floormanager.text_log.draw()
            textlog_pos = (4, self.screen_size[1] - 4 - textlog_surf.get_height())
            screen_surf.blit(textlog_surf, textlog_pos)

        dungeon_name_length = self.font.size(self.floormanager.dungeon_name)[0]
        draw_cor = [self.screen_size[0] - dungeon_name_length - 56, 19]
        screen_surf.blit(self.font.render(self.floormanager.dungeon_name, False, self.font_color), draw_cor)

        line_start_pos = [draw_cor[0], draw_cor[1]+self.font.get_linesize() + 1]
        line_end_pos = [line_start_pos[0] + dungeon_name_length + 1, line_start_pos[1]]
        pygame.draw.line(screen_surf, (255, 255, 255), line_start_pos, line_end_pos)

        floor_number_text = 'Floor ' + str(self.floormanager.floor_number)
        floor_number_length = self.font.size(floor_number_text)[0]
        draw_cor[0] = self.screen_size[0] - floor_number_length - 56
        draw_cor[1] += self.font.get_linesize() + 3
        screen_surf.blit(self.font.render(floor_number_text, False, self.font_color), draw_cor)

        self.draw_player_info(screen_surf, [2, 19])

        return screen_surf

    def draw_player_info(self, screen_surf, pos):
        bar_width = 50
        draw_cor = pos.copy()

        screen_surf.blit(self.font.render(self.player_name, False, self.font_color), draw_cor)
        draw_cor[1] += self.font.get_linesize()
        pygame.draw.line(screen_surf, (255,255,255), draw_cor, [draw_cor[0]+135, draw_cor[1]])
        draw_cor[1] += 2
        
        screen_surf.blit(self.font.render('HP', False, self.font_color), draw_cor)
        draw_cor[0] += self.font.size('HP')[0]
        pygame.draw.rect(screen_surf, self.font_color, pygame.Rect(draw_cor[0], draw_cor[1], bar_width, self.font.get_ascent()), 1)
        fill_width = math.ceil((bar_width - 4) * (self.player_stats['hp'] / self.player_stats['max_hp']))
        pygame.draw.rect(screen_surf, (0,255,0), pygame.Rect(draw_cor[0]+2, draw_cor[1]+2, fill_width, self.font.get_ascent()-4), 0)
        draw_cor[0] += bar_width + 1
        stat_text = str(self.player_stats['hp']) + '/' + str(self.player_stats['max_hp'])
        screen_surf.blit(self.font.render(stat_text, False, self.font_color), draw_cor)

        draw_cor[0] = pos[0]
        draw_cor[1] += self.font.get_linesize()
        screen_surf.blit(self.font.render('SP', False, self.font_color), draw_cor)
        draw_cor[0] += self.font.size('SP')[0]
        pygame.draw.rect(screen_surf, self.font_color, pygame.Rect(draw_cor[0], draw_cor[1], bar_width, self.font.get_ascent()), 1)
        fill_width = math.ceil((bar_width - 4) * (self.player_stats['sp'] / self.player_stats['max_sp']))
        pygame.draw.rect(screen_surf, (0,255,255), pygame.Rect(draw_cor[0]+2, draw_cor[1]+2, fill_width, self.font.get_ascent()-4), 0)
        draw_cor[0] += bar_width + 1
        stat_text = str(self.player_stats['sp']) + '/' + str(self.player_stats['max_sp'])
        screen_surf.blit(self.font.render(stat_text, False, self.font_color), draw_cor)

        draw_cor[0] = pos[0]
        draw_cor[1] += self.font.get_linesize()
        screen_surf.blit(self.font.render('EN', False, self.font_color), draw_cor)
        draw_cor[0] += self.font.size('EN')[0]
        pygame.draw.rect(screen_surf, self.font_color, pygame.Rect(draw_cor[0], draw_cor[1], bar_width, self.font.get_ascent()), 1)
        fill_width = math.ceil((bar_width - 4) * (self.player_stats['en'] / self.player_stats['max_en']))
        pygame.draw.rect(screen_surf, (255, 0, 64), pygame.Rect(draw_cor[0]+2, draw_cor[1]+2, fill_width, self.font.get_ascent()-4), 0)
        draw_cor[0] += bar_width + 1
        stat_text = str(self.player_stats['en']) + '/' + str(self.player_stats['max_en'])
        screen_surf.blit(self.font.render(stat_text, False, self.font_color), draw_cor)