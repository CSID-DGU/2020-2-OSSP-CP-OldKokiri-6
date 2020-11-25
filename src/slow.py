from src.setting import *

class Slow:

    def __init__(self, sizex=-1, sizey=-1, x=-1, y=-1):
        self.images, self.rect = load_sprite_sheet("slow_pic.png", 2, 1, sizex, sizey, -1)
        self.image = self.images[1]
        if x == -1:
            self.rect.left = width * 0.01
        else:
            self.rect.left = x

        if y == -1:
            self.rect.top = height * 0.01
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image, self.rect)
