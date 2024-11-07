import pygame, math

class Minimap:
    def __init__(self, floormanager):
        self.small_player_icon = True
        self.icon_timer = 0
        self.icon_timer_duration = 30
        self.floormanager = floormanager
        self.unit_size = 4
        self.floor_color = (1,0,0)
        self.unit_color = (255,0,0)
        self.player_color = (255,255,255)
        self.item_color = (0,255,255)
        self.stairs_color = (0,255,255)
        self.trap_color = (0,255,0)
        self.floor_alpha = 255

    def update(self):
        if self.floormanager.get_player().state != 'idle':
            self.icon_timer = self.icon_timer_duration
            self.small_player_icon = False
        else:
            self.icon_timer = max(0, self.icon_timer-1)

        if self.icon_timer == 0:
            self.small_player_icon = not self.small_player_icon
            self.icon_timer = self.icon_timer_duration
    
    def draw(self):
        surf = pygame.Surface(((self.floormanager.floor.floor_width * self.unit_size), (self.floormanager.floor.floor_height * self.unit_size)))
        surf.set_colorkey((0,0,0))

        for i in range(self.floormanager.floor.floor_width):
            for j in range(self.floormanager.floor.floor_height):
                map_cor = [i, j]

                if self.floormanager.get_visibility_map(map_cor) > 0:
                    pin_radius = 2
                    #cell = self.draw_floor_cell(map_cor)
                    cell = self.draw_floor_cell() if self.floormanager.floor.get_floor_map(map_cor) == 1 else self.draw_wall_cell(map_cor)

                    if map_cor == self.floormanager.stairs_cor:
                        pygame.draw.rect(cell, self.stairs_color, pygame.Rect(0, 0, 4, 4), 1)

                    trap_id = self.floormanager.get_trap_map(map_cor)
                    if trap_id > -1:
                        trap = self.floormanager.get_trap(trap_id)
                        if trap.visible:
                            pygame.draw.line(cell, self.trap_color, (0, 0), (self.unit_size-1, self.unit_size-1))
                            pygame.draw.line(cell, self.trap_color, (0, self.unit_size-1), (self.unit_size-1, 0))
                    
                    item_id = self.floormanager.get_item_map(map_cor)
                    if item_id > -1:
                            pygame.draw.circle(cell, self.item_color, (pin_radius, pin_radius), pin_radius)
                            #pygame.draw.rect(cell, self.item_color, pygame.Rect(1, 1, 3, 3))

                    unit_id = self.floormanager.get_unit_map(map_cor)
                    if unit_id > -1 and unit_id == self.floormanager.player_id and not self.small_player_icon:
                        pygame.draw.circle(cell, self.player_color, (pin_radius, pin_radius), pin_radius)
                        #pygame.draw.rect(cell, self.player_color, pygame.Rect(1, 1, 3, 3))
                    elif unit_id > -1 and unit_id == self.floormanager.player_id and self.small_player_icon:
                        pygame.draw.rect(cell, self.player_color, pygame.Rect(1, 1, 2, 2))
                    elif unit_id > -1 and unit_id != self.floormanager.player_id:
                        pygame.draw.circle(cell, self.unit_color, (pin_radius, pin_radius), pin_radius)
                        #pygame.draw.rect(cell, self.unit_color, pygame.Rect(1, 1, 3, 3))

                    surf.blit(cell, (i * self.unit_size, j * self.unit_size))

        #pygame.draw.rect(surf, (255,255,255), pygame.Rect(0, 0, surf.get_width(), surf.get_height()), 1)
        return surf

    # -- this function draws a border on the floor tile if there is a wall next to it
    # def draw_floor_cell(self, map_cor):
    #     cell = pygame.Surface((self.unit_size, self.unit_size))
    #     fill_color = (0,0,0) if self.floormanager.floor.get_floor_map(map_cor) == 0 else self.floor_color
    #     cell.fill(fill_color)
    #     dir_x = [0,1,1,1,0,-1,-1,-1]
    #     dir_y = [-1,-1,0,1,1,1,0,-1]

    #     for i in range(len(dir_x)):
    #         neighbor_cor = [map_cor[0] + dir_x[i], map_cor[1] + dir_y[i]]
    #         if self.floormanager.floor.get_floor_map(map_cor) == 1 and self.floormanager.floor.get_floor_map(neighbor_cor) == 0:
    #             if i == 0:
    #                 pygame.draw.line(cell, (255, 255, 255), (0, 0), (self.unit_size-1, 0))
    #             if i == 1:
    #                 cell.set_at((self.unit_size-1, 0), (255, 255, 255))
    #             if i == 2:
    #                 pygame.draw.line(cell, (255, 255, 255), (self.unit_size-1, 0), (self.unit_size-1, self.unit_size-1))
    #             if i == 3:
    #                 cell.set_at((self.unit_size-1, self.unit_size-1), (255, 255, 255))
    #             if i == 4:
    #                 pygame.draw.line(cell, (255, 255, 255), (0, self.unit_size-1), (self.unit_size-1, self.unit_size-1))
    #             if i == 5:
    #                 cell.set_at((0, self.unit_size-1), (255, 255, 255))
    #             if i == 6:
    #                 pygame.draw.line(cell, (255, 255, 255), (0, 0), (0, self.unit_size-1))
    #             if i == 7:
    #                 cell.set_at((0, 0), (255, 255, 255))
    #     return cell
    
    def draw_floor_cell(self):
        cell = pygame.Surface((self.unit_size, self.unit_size))
        cell.fill(self.floor_color)
        cell.set_alpha(self.floor_alpha)
        return cell

    def draw_wall_cell(self, map_cor):
        cell = pygame.Surface((self.unit_size, self.unit_size))
        cell.fill((0,0,0))
        dir_x = [0,1,1,1,0,-1,-1,-1]
        dir_y = [-1,-1,0,1,1,1,0,-1]

        for i in range(len(dir_x)):
            neighbor_cor = [map_cor[0] + dir_x[i], map_cor[1] + dir_y[i]]
            if self.floormanager.floor.isinbound(neighbor_cor) and self.floormanager.floor.get_floor_map(neighbor_cor) == 1 and self.floormanager.get_visibility_map(neighbor_cor) > 0:
                if i == 0:
                    pygame.draw.line(cell, (255, 255, 255), (0, 0), (self.unit_size-1, 0))
                if i == 1:
                    cell.set_at((self.unit_size-1, 0), (255, 255, 255))
                if i == 2:
                    pygame.draw.line(cell, (255, 255, 255), (self.unit_size-1, 0), (self.unit_size-1, self.unit_size-1))
                if i == 3:
                    cell.set_at((self.unit_size-1, self.unit_size-1), (255, 255, 255))
                if i == 4:
                    pygame.draw.line(cell, (255, 255, 255), (0, self.unit_size-1), (self.unit_size-1, self.unit_size-1))
                if i == 5:
                    cell.set_at((0, self.unit_size-1), (255, 255, 255))
                if i == 6:
                    pygame.draw.line(cell, (255, 255, 255), (0, 0), (0, self.unit_size-1))
                if i == 7:
                    cell.set_at((0, 0), (255, 255, 255))
        return cell
    