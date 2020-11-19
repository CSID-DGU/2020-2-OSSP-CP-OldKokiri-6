from src.setting import *


class Heart:

    def __init__(self, sizex=-1, sizey=-1, x=-1, y=-1):
        self.images, self.rect = load_sprite_sheet("heart.png", 2, 1, sizex, sizey, -1)
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


class HeartIndicator:

    def __init__(self, life):
        self.heart_size = 40
        self.life = life
        self.life_set = []

    def draw(self):
        for life in self.life_set:
            life.draw()

    def update(self, life):
        self.life = life
        self.life_set = [Heart(self.heart_size, self.heart_size, width * 0.01 + i * self.heart_size) for i in range(self.life)]


