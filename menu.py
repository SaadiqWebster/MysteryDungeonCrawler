import pygame
import customfont as _f

class Menu():
    def __init__(self, options):
        self.id = 'menu'
        self.text = pygame.font.Font('fonts/Coolville.ttf', 10)
        self.text_height = self.text.get_ascent()
        self.hor_padding = 2
        self.ver_padding = 2
        self.line_spacing = 4

        longest_length = 0
        for option in options:
            text_width = self.text.size(option)[0]
            longest_length = max(longest_length, text_width)

        self.draw_cor = [0,0]
        self.window_width = 5 + (self.hor_padding * 2) + longest_length
        self.window_height = 5 + (self.ver_padding * 2) + (self.text_height * len(options)) + (self.line_spacing * (len(options)-1))
        self.options = options
        self.select = 0
        self.animation_state = 'open'
        self.animation_duration = 3
        self.animation_timer = self.animation_duration

    def set_draw_cor(self, draw_cor):
        self.draw_cor = draw_cor.copy()

    def close(self):
        self.animation_state = 'close'
        self.animation_timer = self.animation_duration

    def get_option(self):
        if len(self.options) > 0:
            return self.options[self.select]
    
    def is_open(self):
        return self.animation_state == 'open' and self.animation_timer <= 0
    
    def is_closed(self):
        return self.animation_state == 'close' and self.animation_timer <= 0

    def cursor_forward(self):
        if len(self.options) > 0:
            self.select = (self.select-1) % len(self.options)

    def cursor_backward(self):
        if len(self.options) > 0:
            self.select = (self.select+1) % len(self.options)

    def update_animation(self):
        self.animation_timer = max(self.animation_timer-1, 0)

    def draw(self):
        surf = pygame.Surface((self.window_width+1, self.window_height+1))
        surf.fill((0,0,0))
        surf.set_colorkey((0,0,0))

        border_width = (self.window_width-1) * (self.animation_timer / self.animation_duration)
        border_height = (self.window_height-1) * (self.animation_timer / self.animation_duration)
        if self.animation_state == 'open':
            border_width = (self.window_width-1) - border_width
            border_height = (self.window_height-1) - border_height

        menu_border = pygame.Rect(0, 0, border_width, border_height)
        border_shadow = pygame.Rect(1, 1, border_width, border_height)
        pygame.draw.rect(surf, (1,0,0), border_shadow)
        pygame.draw.rect(surf, (255,255,255), menu_border, 1)

        if self.is_open():
            x_offset = 2 + self.hor_padding
            y_offset = 2 + self.ver_padding
            for i in range(len(self.options)):
                text_color = (255, 255, 255)
                if i == self.select:
                    text_color = (1, 0, 0)
                    highlight = pygame.Surface((self.window_width - 4 - (self.hor_padding * 2), self.text_height+2))
                    highlight.fill((255, 255, 255))
                    surf.blit(highlight, (x_offset, y_offset))

                surf.blit(self.text.render(self.options[i], False, text_color), (x_offset+1, y_offset+1))
                y_offset += self.text_height + self.line_spacing

        return surf
    
class InventoryMenu(Menu):
    def __init__(self, inventory):
        self.inventory = inventory
        item_list = [item.id for item in inventory]
        super().__init__(item_list)
        self.id = 'inventory'
        self.max_line_count = 12
        self.window_width = 101
        self.window_height = 5 + (self.ver_padding * 2) + (self.text_height * self.max_line_count) + (self.line_spacing * (self.max_line_count-1))
        
    def get_selected(self):
        return self.inventory[self.select]
    
    def pop_selected(self):
        self.options.pop(self.select)
        return self.inventory.pop(self.select)
    
    # this is copy and paste from the inherited class. the text color will change if an item is equipped.
    def draw(self):
        surf = pygame.Surface((self.window_width+1, self.window_height+1))
        surf.fill((0,0,0))
        surf.set_colorkey((0,0,0))

        border_width = (self.window_width-1) * (self.animation_timer / self.animation_duration)
        border_height = (self.window_height-1) * (self.animation_timer / self.animation_duration)
        if self.animation_state == 'open':
            border_width = (self.window_width-1) - border_width
            border_height = (self.window_height-1) - border_height

        menu_border = pygame.Rect(0, 0, border_width, border_height)
        border_shadow = pygame.Rect(1, 1, border_width, border_height)
        pygame.draw.rect(surf, (1,0,0), border_shadow)
        pygame.draw.rect(surf, (255,255,255), menu_border, 1)

        if self.is_open():
            x_offset = 2 + self.hor_padding
            y_offset = 2 + self.ver_padding
            for i in range(len(self.options)):
                text_color = (255, 255, 255)
                item = self.inventory[i]
                if item.effect == 'equip' and item.isequipped:
                    text_color = (255, 255, 0)

                if i == self.select:
                    text_color = (1, 0, 0)
                    highlight = pygame.Surface((self.window_width - 4 - (self.hor_padding * 2), self.text_height+2))
    
                    highlight_color = (255, 255, 255)
                    if item.effect == 'equip' and item.isequipped:
                        highlight_color = (255, 255, 0)
                    
                    highlight.fill(highlight_color)
                    surf.blit(highlight, (x_offset, y_offset))

                surf.blit(self.text.render(self.options[i], False, text_color), (x_offset+1, y_offset+1))
                y_offset += self.text_height + self.line_spacing

        return surf
        