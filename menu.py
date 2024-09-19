import pygame
import customfont as _f

class Menu():
    def __init__(self, draw_cor, options):
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

        self.draw_cor = draw_cor
        self.window_width = 5 + (self.hor_padding * 2) + longest_length
        self.window_height = 5 + (self.ver_padding * 2) + (self.text_height * len(options)) + (self.line_spacing * (len(options)-1))
        self.options = options
        self.select = 0

    def get_option(self):
        if len(self.options) > 0:
            return self.options[self.select]
    
    def cursor_forward(self):
        if len(self.options) > 0:
            self.select = (self.select-1) % len(self.options)

    def cursor_backward(self):
        if len(self.options) > 0:
            self.select = (self.select+1) % len(self.options)

    def draw(self):
        surf = pygame.Surface((self.window_width, self.window_height))
        surf.fill((0,0,0))
        menu_border = pygame.Rect(1, 1, self.window_width-2, self.window_height-2)
        pygame.draw.rect(surf, (255,255,255), menu_border, 1)

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
    def __init__(self, draw_cor, inventory):
        self.inventory = inventory
        item_list = [item.id for item in inventory]
        super().__init__(draw_cor, item_list)
        self.id = 'inventory'
        self.max_line_count = 8
        self.window_width = 101
        self.window_height = 5 + (self.ver_padding * 2) + (self.text_height * self.max_line_count) + (self.line_spacing * (self.max_line_count-1))
        
    def get_selected(self):
        return self.inventory[self.select]
    
    def pop_selected(self):
        self.options.pop(self.select)
        return self.inventory.pop(self.select)
    
    # this is copy and paste from the inherited class. the text color will change if an item is equipped.
    def draw(self):
        surf = pygame.Surface((self.window_width, self.window_height))
        surf.fill((0,0,0))
        menu_border = pygame.Rect(1, 1, self.window_width-2, self.window_height-2)
        pygame.draw.rect(surf, (255,255,255), menu_border, 1)

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