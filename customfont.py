import pygame

class CustomFont:
    def __init__(self, font_img, hor_space=1):
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','.',',','"','\'','?','!','_','#','%','&','(',')','+','-','/',':','<','>']
        self.characters = {}
        self.hor_space = hor_space
        self.char_space_width = 3

        char_count = 0
        char_width = 0
        for i in range(font_img.get_width()):
            color = font_img.get_at((i, 0))
            if color != (255,0,0):
                char_width += 1
            else:
                char_img = self.cut_surf(font_img, i - char_width, 0, char_width, font_img.get_height())
                self.characters[self.character_order[char_count]] = char_img
                char_count += 1
                char_width = 0

    def get_height(self):
        return self.characters['A'].get_height()
    
    def get_width(self, text):
        width = 0
        for char in text:
            if char == ' ':
                width += self.char_space_width
            elif char in self.characters:
                width += self.characters[char].get_width()
            width += self.hor_space
        return width
    
    def cut_surf(self, surf, x, y, width, height):
        surf_copy = surf.copy()
        clip = pygame.Rect(x, y, width, height)
        surf_copy.set_clip(clip)
        cut = surf.subsurface(surf_copy.get_clip())
        return cut.copy()

    def swap_color(self, img, old_color, new_color):
        img_copy = pygame.Surface(img.get_size())
        img_copy.fill(new_color)
        img.set_colorkey(old_color)
        img_copy.blit(img, (0,0))
        return img_copy

    def draw(self, text, color=(255,255,255), alpha=255, size=1):
        text_surf = pygame.Surface((self.get_width(text), self.get_height()))

        char_x_position = 0
        for char in text:
            if char not in self.characters:
                char_x_position += self.char_space_width + self.hor_space
            else:
                char_img = self.characters[char]
                char_img = self.swap_color(char_img, (255,255,255), color)
                text_surf.blit(char_img, (char_x_position, 0))
                char_x_position += self.characters[char].get_width() + self.hor_space

        text_surf.set_colorkey((0,0,0))
        text_surf.set_alpha(alpha)
        return pygame.transform.scale_by(text_surf, size)      
    