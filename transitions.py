import pygame

class Transition:
    def __init__(self, screen_size, fade, duration, color):
        self.screen_size = screen_size
        self.color = color
        self.surf = pygame.Surface(self.screen_size)
        self.surf.fill(self.color)
        self.duration = duration
        self.timer = self.duration
        self.fade = fade
        self.end = False
    
    def update(self):
        self.timer = max(0, self.timer-1)
        self.end = self.timer <= 0
    
    def fade_in(self, duration = -1):
        self.fade = 'in'
        if duration > -1:
            self.duration = duration
        self.timer = self.duration
    
    def fade_out(self, duration = -1):
        self.fade = 'out'
        if duration > -1:
            self.duration = duration
        self.timer = self.duration
    
    def draw(self):
        alpha = 255 * (self.timer / self.duration)

        if self.fade == 'in':
            self.surf.set_alpha(255 - alpha)

        elif self.fade == 'out':
            self.surf.set_alpha(alpha)

        return self.surf