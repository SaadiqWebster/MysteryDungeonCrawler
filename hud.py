import pygame, math
import textlog as _l, minimap as _m

class Hud:
    def __init__(self, CAMERA_SIZE, floormanager):
        self.screen_size = CAMERA_SIZE
        self.floormanager = floormanager
        self.font = pygame.font.Font('fonts/ORGAN___.TTF', 7)
        self.font_color = (255, 255, 255)
        self.background_alpha = 0
        self.minimap = _m.Minimap(self.floormanager)
        self.minimap_visibility = True

    def swap_color(self, img, old_color, new_color):
        img_copy = pygame.Surface(img.get_size())
        img_copy.fill(new_color)
        img.set_colorkey(old_color)
        img_copy.blit(img, (0,0))
        return img_copy
    
    def update(self):
        self.minimap.update()

        #self.textlog_visibility = self.floormanager.get_active_menu() is None
        #self.minimap_visibility = self.floormanager.get_active_menu() is None

    def draw(self):
        screen_surf = pygame.Surface(self.screen_size)
        screen_surf.fill((0,0,0))
        screen_surf.set_colorkey((0,0,0))

        if self.minimap_visibility:
            minimap_surf = self.minimap.draw()
            minimap_shadow = pygame.mask.from_surface(minimap_surf)
            minimap_shadow.invert()
            minimap_shadow = minimap_shadow.to_surface()
            minimap_shadow = self.swap_color(minimap_shadow, (0,0,0), (1,0,0))
            minimap_shadow.set_colorkey((255,255,255))
            minimap_pos = (self.screen_size[0] - minimap_surf.get_width() - 20, self.screen_size[1] - minimap_surf.get_height() - 12)
            screen_surf.blit(minimap_shadow, (minimap_pos[0]+1, minimap_pos[1]+1))
            screen_surf.blit(minimap_surf, minimap_pos)

        if self.floormanager.text_log.visibility:
            textlog_surf = self.floormanager.text_log.draw()
            textlog_pos = (4, self.screen_size[1] - 4 - textlog_surf.get_height())
            screen_surf.blit(textlog_surf, textlog_pos)
            screen_surf.blit(self.font.render('Log', False, (1,0,0)), (textlog_pos[0]+1, textlog_pos[1] - self.font.size('Log')[1]+1))
            screen_surf.blit(self.font.render('Log', False, (255,255,255)), (textlog_pos[0], textlog_pos[1] - self.font.size('Log')[1]))
            pygame.draw.line(screen_surf, (1,0,0), (textlog_pos[0]+1, textlog_pos[1]+4), (textlog_pos[0]+1, textlog_pos[1]+textlog_surf.get_height()-4))
            pygame.draw.line(screen_surf, (255,255,255), (textlog_pos[0], textlog_pos[1]+3), (textlog_pos[0], textlog_pos[1]+textlog_surf.get_height()-5))

        dungeon_name_length = self.font.size(self.floormanager.dungeon_name)[0]
        draw_cor = [self.screen_size[0] - dungeon_name_length - 4, 8]
        screen_surf.blit(self.font.render(self.floormanager.dungeon_name, False, (1,0,0)), (draw_cor[0]+1, draw_cor[1]+1))
        screen_surf.blit(self.font.render(self.floormanager.dungeon_name, False, self.font_color), draw_cor)

        #line_start_pos = [draw_cor[0], draw_cor[1]+self.font.get_linesize() + 1]
        #line_end_pos = [line_start_pos[0] + dungeon_name_length + 1, line_start_pos[1]]
        #pygame.draw.line(screen_surf, (255, 255, 255), line_start_pos, line_end_pos)

        floor_number_text = 'Floor ' + str(self.floormanager.floor_number)
        floor_number_length = self.font.size(floor_number_text)[0]
        draw_cor[0] = self.screen_size[0] - floor_number_length - 4
        draw_cor[1] += self.font.get_linesize() + 3
        screen_surf.blit(self.font.render(floor_number_text, False, (1,0,0)), (draw_cor[0]+1, draw_cor[1]+1))
        screen_surf.blit(self.font.render(floor_number_text, False, self.font_color), draw_cor)

        if self.floormanager.get_player() is not None:
            self.draw_player_info(screen_surf, [4, 8])

        return screen_surf

    def draw_player_info(self, screen_surf, pos):
        player = self.floormanager.get_player()
        draw_cor = pos.copy()

        level_text = 'Lv ' + str(player.stats['level'])
        hp_stat_text = str(player.stats['hp']) + '/' + str(player.stats['max_hp'])
        sp_stat_text = str(player.stats['sp']) + '/' + str(player.stats['max_sp'])
        maxhp_stat_text = str(player.stats['max_hp']) + '/' + str(player.stats['max_hp'])
        maxsp_stat_text = str(player.stats['max_sp']) + '/' + str(player.stats['max_sp'])
        energy_stat_text = str(math.ceil((player.stats['en']/player.stats['max_en']) * 100)) + '%'
        hp_bar_width = self.font.size('HPA')[0] + self.font.size(maxhp_stat_text)[0]
        sp_bar_width = self.font.size('SPA')[0] + self.font.size(maxsp_stat_text)[0]
        energy_bar_width = self.font.size('ENA')[0] + self.font.size('100%')[0]
        hp_fill_width = math.ceil((hp_bar_width - 4) * (player.stats['hp'] / player.stats['max_hp']))
        sp_fill_width = math.ceil((sp_bar_width - 4) * (player.stats['sp'] / player.stats['max_sp']))
        energy_fill_width = math.ceil((energy_bar_width - 4) * (player.stats['en'] / player.stats['max_en']))
        line_length = max(self.font.size(player.id+'A'+level_text)[0], 
                          self.font.size('HP'+'A'+maxhp_stat_text+'A'+'SP'+'A'+maxsp_stat_text+'A'+'EN'+'A'+'100%')[0] - 1)

        # player name and level
        screen_surf.blit(self.font.render(player.id, False, (1, 0, 0)), (draw_cor[0]+1, draw_cor[1]+1))
        screen_surf.blit(self.font.render(player.id, False, self.font_color), draw_cor)
        draw_cor[0] += self.font.size(player.id)[0] + self.font.size('A')[0]
        screen_surf.blit(self.font.render(level_text, False, (1, 0, 0)), (draw_cor[0]+1, draw_cor[1]+1))
        screen_surf.blit(self.font.render(level_text, False, self.font_color), draw_cor)
        
        # horizontal line
        draw_cor[0] = pos[0]
        draw_cor[1] += self.font.get_linesize()
        pygame.draw.line(screen_surf, (1,0,0), draw_cor, [draw_cor[0]+line_length+1, draw_cor[1]+1])
        pygame.draw.line(screen_surf, (255,255,255), draw_cor, [draw_cor[0]+line_length, draw_cor[1]])
        
        # hp stat
        draw_cor[1] += 2
        screen_surf.blit(self.font.render('HP', False, (1,0,0)), (draw_cor[0]+1, draw_cor[1]+1))
        screen_surf.blit(self.font.render('HP', False, self.font_color), draw_cor)
        draw_cor[0] += self.font.size('HPA')[0] + self.font.size(maxhp_stat_text)[0]
        screen_surf.blit(self.font.render(hp_stat_text, False, (1,0,0)), (draw_cor[0] - self.font.size(hp_stat_text)[0]+1, draw_cor[1]+1))
        screen_surf.blit(self.font.render(hp_stat_text, False, self.font_color), (draw_cor[0] - self.font.size(hp_stat_text)[0], draw_cor[1]))

        # sp stat
        draw_cor[0] += self.font.size('A')[0]
        screen_surf.blit(self.font.render('SP', False, (1,0,0)), (draw_cor[0]+1, draw_cor[1]+1))
        screen_surf.blit(self.font.render('SP', False, self.font_color), draw_cor)
        draw_cor[0] += self.font.size('SPA')[0] + self.font.size(maxsp_stat_text)[0]
        screen_surf.blit(self.font.render(sp_stat_text, False, (1,0,0)), (draw_cor[0] - self.font.size(sp_stat_text)[0]+1, draw_cor[1]+1))
        screen_surf.blit(self.font.render(sp_stat_text, False, self.font_color), (draw_cor[0] - self.font.size(sp_stat_text)[0], draw_cor[1]))

        # energy stat
        draw_cor[0] += self.font.size('A')[0]
        screen_surf.blit(self.font.render('EN', False, (1,0,0)), (draw_cor[0]+1, draw_cor[1]+1))
        screen_surf.blit(self.font.render('EN', False, self.font_color), draw_cor)
        draw_cor[0] += self.font.size('ENA')[0] + self.font.size('100%')[0]
        screen_surf.blit(self.font.render(energy_stat_text, False, (1,0,0)), (draw_cor[0] - self.font.size(energy_stat_text)[0]+1, draw_cor[1]+1))
        screen_surf.blit(self.font.render(energy_stat_text, False, self.font_color), (draw_cor[0] - self.font.size(energy_stat_text)[0], draw_cor[1]))

        # hp bar
        draw_cor[0] = pos[0]
        draw_cor[1] += self.font.get_linesize()
        pygame.draw.rect(screen_surf, (1,0,0), pygame.Rect(draw_cor[0]+1, draw_cor[1]+1, hp_bar_width, self.font.get_ascent()))
        pygame.draw.rect(screen_surf, (255,255,255), pygame.Rect(draw_cor[0], draw_cor[1], hp_bar_width, self.font.get_ascent()), 1)
        pygame.draw.rect(screen_surf, (1,0,0), pygame.Rect(draw_cor[0]+1, draw_cor[1]+1, hp_bar_width-2, self.font.get_ascent()-2))
        pygame.draw.rect(screen_surf, (255,0,0), pygame.Rect(draw_cor[0]+2, draw_cor[1]+2, hp_fill_width, self.font.get_ascent()-4), 0)
        
        # sp bar
        draw_cor[0] += self.font.size('HPA')[0] + self.font.size(maxhp_stat_text + 'A')[0]
        pygame.draw.rect(screen_surf, (1,0,0), pygame.Rect(draw_cor[0]+1, draw_cor[1]+1, sp_bar_width, self.font.get_ascent()))
        pygame.draw.rect(screen_surf, (255,255,255), pygame.Rect(draw_cor[0], draw_cor[1], sp_bar_width, self.font.get_ascent()), 1)
        pygame.draw.rect(screen_surf, (1,0,0), pygame.Rect(draw_cor[0]+1, draw_cor[1]+1, sp_bar_width-2, self.font.get_ascent()-2))
        pygame.draw.rect(screen_surf, (0,0,255), pygame.Rect(draw_cor[0]+2, draw_cor[1]+2, sp_fill_width, self.font.get_ascent()-4), 0)
        
        # energy bar
        draw_cor[0] += self.font.size('SPA')[0] + self.font.size(maxsp_stat_text + 'A')[0]
        pygame.draw.rect(screen_surf, (1, 0, 0), pygame.Rect(draw_cor[0]-2+1, draw_cor[1]+1+1, 3, self.font.get_ascent()-2))
        pygame.draw.rect(screen_surf, (1, 0, 0), pygame.Rect(draw_cor[0]+1, draw_cor[1]+1, energy_bar_width, self.font.get_ascent()))
        pygame.draw.rect(screen_surf, (255, 255, 255), pygame.Rect(draw_cor[0]-2, draw_cor[1]+1, 3, self.font.get_ascent()-2))
        pygame.draw.rect(screen_surf, (255, 255, 255), pygame.Rect(draw_cor[0], draw_cor[1], energy_bar_width, self.font.get_ascent()), 1)
        pygame.draw.rect(screen_surf, (1,0,0), pygame.Rect(draw_cor[0]+1, draw_cor[1]+1, energy_bar_width-2, self.font.get_ascent()-2))
        pygame.draw.rect(screen_surf, (252, 240, 3), pygame.Rect(draw_cor[0]+2, draw_cor[1]+2, energy_fill_width, self.font.get_ascent()-4), 0)


