from random import random

from pygame import draw, Color, Surface
from pygame.sprite import Group

from .background import Background, FallingBackground
from .game import GameObject


def generate_random_color():
    color = Color(255, 255, 255)
    color.hsva = (int(360 * random()), 100, 100, 100)
    return color


class Window(GameObject):
    def __init__(self, *groups: Group, size=(0, 0), coord=(0, 0), debug=False):
        self.game_objects: Group[GameObject] = Group()
        self.debug_color = generate_random_color() if debug else None
        super().__init__(*groups, size=size, coord=coord)

    def update(self, *args, **kwargs):
        self.game_objects.update(*args, **kwargs)

    @property
    def image(self):
        self.game_objects.draw(self._image)
        if self.debug_color is not None:
            draw.rect(self._image, self.debug_color, (0, 0, self.rect.width, self.rect.height), 5)
        return self._image

    @image.setter
    def image(self, value: Surface):
        self._image = value

    def image_update(self):
        for game_object in self.game_objects:
            game_object.image_update()


class MyWindow(Window):
    def __init__(self, *groups: Group, **kwargs):
        super().__init__(*groups, **kwargs)
        Background(self.game_objects, size=(500, 500), color_fill="gray")
        FallingBackground(self.game_objects, size=(100, 100), color_fill="white")

    def update(self, *args, **kwargs):
        self.rect.y += 1
        super().update()
