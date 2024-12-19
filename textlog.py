import pygame
import customfont as _f

class TextLog():
    def __init__(self):
        self.log_limit = 50
        self.log_width = 300
        self.line_count = 4
        self.next_logs = []
        self.written_logs = ['']
        self.font = pygame.font.Font('fonts/Coolville.ttf', 10)
        self.textbox_color = (0,0,0)
        self.visibility = False
        self.cursor_speed = 1
        self.cursor_timer = 0
        self.pause_duration = 8
        self.pause_timer = 0

    def add(self, message):
        if len(self.written_logs) > self.log_limit:
            self.written_logs.pop(0)
        self.next_logs.append(message)
        self.visibility = True

    def clear(self):
        self.next_logs = []
        self.written_logs = ['']
    
    def update(self):
        self.cursor_timer = max(self.cursor_timer - 1, 0)

        if self.cursor_timer <= 0 and self.next_logs:
            log = self.next_logs[0]
            if log != '':
                self.written_logs[-1] += log[0]
                self.next_logs[0] = log[1:]
                self.cursor_timer = self.cursor_speed
            else:
                self.pause_timer = max(self.pause_timer - 1, 0)
                if self.pause_timer <= 0 and len(self.next_logs) > 1:
                    self.next_logs.pop(0)
                    self.written_logs.append('')
                    self.pause_timer = self.pause_duration
                    

    def draw(self):
        surf_width = self.log_width
        surf_height = (self.font.get_linesize() * self.line_count) + 6
        surf = pygame.Surface((surf_width, surf_height))
        surf.fill(self.textbox_color)
        # menu_border = pygame.Rect(1, 1, surf_width-2, surf_height-2)
        # pygame.draw.rect(surf, (255, 255, 255), menu_border, 1)

        x_offset = 4
        y_offset = 4
        for i in range(max(0, len(self.written_logs) - self.line_count), len(self.written_logs)):
            message = self.written_logs[i]
            text = self.font.render(message, False, (255,255,255))
            text_shadow = self.font.render(message, False, (1,0,0))
            surf.blit(text_shadow, (x_offset+1, y_offset+1))
            surf.blit(text, (x_offset, y_offset))
            y_offset += self.font.get_linesize()

        return surf
