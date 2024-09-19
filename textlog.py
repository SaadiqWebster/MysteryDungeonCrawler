import pygame
import customfont as _f

class TextLog():
    def __init__(self):
        self.log_limit = 50
        self.line_count = 4
        self.logs = []
        self.font = pygame.font.Font('fonts/Coolville.ttf', 10)
        self.textbox_color = (1,0,0)

    def add(self, message):
        if len(self.logs) > self.log_limit:
            self.logs.pop(0)
        self.logs.append(message)

    def clear(self):
        self.logs = []
    
    def draw(self):
        surf_width = 180
        surf_height = (self.font.get_linesize() * self.line_count) + 6
        surf = pygame.Surface((surf_width, surf_height))
        surf.fill(self.textbox_color)
        menu_border = pygame.Rect(1, 1, surf_width-2, surf_height-2)
        pygame.draw.rect(surf, (255, 255, 255), menu_border, 1)

        x_offset = 4
        y_offset = 4
        for i in range(max(0, len(self.logs) - self.line_count), len(self.logs)):
            message = self.logs[i]
            text = self.font.render(message, False, (255,255,255))
            surf.blit(text, (x_offset, y_offset))
            y_offset += self.font.get_linesize()

        return surf
