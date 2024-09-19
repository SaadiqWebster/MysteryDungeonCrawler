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
        self.text_log_visibility = True
        self.minimap_visibility = True

    def update(self):
        self.minimap.update()

        self.text_log_visibility = self.floormanager.get_active_menu() is None
        self.minimap_visibility = self.floormanager.get_active_menu() is None

        for unit_id in self.floormanager.units:
            unit = self.floormanager.units[unit_id]

            if unit_id == self.floormanager.player_id:
                self.player_name = unit.id
                self.player_stats = unit.stats

    def draw(self):
        screen_surf = pygame.Surface(self.screen_size)
        screen_surf.set_colorkey((0,0,0))
        screen_surf.fill((0,0,0))

        if self.minimap_visibility:
            minimap_surf = self.minimap.draw()
            screen_surf.blit(minimap_surf, (-2, self.screen_size[1] - minimap_surf.get_height() - 2))

        if self.text_log_visibility:
            text_log_surf = self.floormanager.text_log.draw()
            screen_surf.blit(text_log_surf, (self.screen_size[0] - text_log_surf.get_width() - 4, self.screen_size[1] - 4 - text_log_surf.get_height()))

        draw_cor = [1,1]
        screen_surf.blit(self.font.render('Dungeon Name', False, self.font_color), draw_cor)
        draw_cor[1] += self.font.get_linesize()
        floor_number_text = str(self.floormanager.floor_number)+'F'
        screen_surf.blit(self.font.render(floor_number_text, False, self.font_color), draw_cor)
        draw_cor[1] = 1

        bar_width = 50
        player_stat_indent = draw_cor[0] + self.font.size('Dungeon Name')[0] + 30

        draw_cor[0] = player_stat_indent
        screen_surf.blit(self.font.render(self.player_name, False, self.font_color), draw_cor)
        draw_cor[1] += self.font.get_linesize()
        
        draw_cor[0] = player_stat_indent
        screen_surf.blit(self.font.render('HP', False, self.font_color), draw_cor)
        draw_cor[0] += self.font.size('HP')[0]
        pygame.draw.rect(screen_surf, self.font_color, pygame.Rect(draw_cor[0], draw_cor[1], bar_width, self.font.get_ascent()), 1)
        fill_width = math.ceil((bar_width - 4) * (self.player_stats['hp'] / self.player_stats['max_hp']))
        pygame.draw.rect(screen_surf, (0,255,0), pygame.Rect(draw_cor[0]+2, draw_cor[1]+2, fill_width, self.font.get_ascent()-4), 0)
        draw_cor[0] += bar_width + 1
        stat_text = str(self.player_stats['hp']) + '/' + str(self.player_stats['max_hp'])
        screen_surf.blit(self.font.render(stat_text, False, self.font_color), draw_cor)

        draw_cor[0] = player_stat_indent
        draw_cor[1] += self.font.get_linesize()
        screen_surf.blit(self.font.render('SP', False, self.font_color), draw_cor)
        draw_cor[0] += self.font.size('SP')[0]
        pygame.draw.rect(screen_surf, self.font_color, pygame.Rect(draw_cor[0], draw_cor[1], bar_width, self.font.get_ascent()), 1)
        fill_width = math.ceil((bar_width - 4) * (self.player_stats['sp'] / self.player_stats['max_sp']))
        pygame.draw.rect(screen_surf, (0,255,255), pygame.Rect(draw_cor[0]+2, draw_cor[1]+2, fill_width, self.font.get_ascent()-4), 0)
        draw_cor[0] += bar_width + 1
        stat_text = str(self.player_stats['sp']) + '/' + str(self.player_stats['max_sp'])
        screen_surf.blit(self.font.render(stat_text, False, self.font_color), draw_cor)

        draw_cor[0] = player_stat_indent
        draw_cor[1] += self.font.get_linesize()
        screen_surf.blit(self.font.render('EN', False, self.font_color), draw_cor)
        draw_cor[0] += self.font.size('EN')[0]
        pygame.draw.rect(screen_surf, self.font_color, pygame.Rect(draw_cor[0], draw_cor[1], bar_width, self.font.get_ascent()), 1)
        fill_width = math.ceil((bar_width - 4) * (self.player_stats['en'] / self.player_stats['max_en']))
        pygame.draw.rect(screen_surf, (255,150,0), pygame.Rect(draw_cor[0]+2, draw_cor[1]+2, fill_width, self.font.get_ascent()-4), 0)
        draw_cor[0] += bar_width + 1
        stat_text = str(self.player_stats['en']) + '/' + str(self.player_stats['max_en'])
        screen_surf.blit(self.font.render(stat_text, False, self.font_color), draw_cor)

        return screen_surf
