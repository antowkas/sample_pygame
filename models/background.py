from pygame import Color

from .game import GameObject


class Background(GameObject):
    def __init__(self, *groups, size=(0, 0), pos=(0, 0), color_fill=Color(0, 0, 0)):
        self.color_fill = color_fill
        super().__init__(*groups, size=size, pos=pos)

    def image_update(self):
        self.image.fill(self.color_fill)


class FallingBackground(Background):
    def update(self, *args, **kwargs):
        self.rect.y += 1
