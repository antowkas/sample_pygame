from random import random
from functools import partial

from pygame import draw, Color
from pygame.sprite import Group

from .button import Button
from .game import GameObject


def generate_random_color():
    color = Color(255, 255, 255)
    color.hsva = (int(360 * random()), 100, 100, 100)
    return color


class Window(GameObject):
    def __init__(self, *groups: Group, size=(0, 0), pos=(0, 0), debug=False):
        self.game_objects: Group[GameObject] = Group()

        super().__init__(*groups, size=size, pos=pos)
        self.last_pos = self.rect.x, self.rect.y

        self.debug_color = generate_random_color() if debug else None
        if self.debug_color is not None:
            draw.rect(self.image, self.debug_color, (0, 0, self.rect.width, self.rect.height), 5)

    def add_game_object(self, game_object_partial: partial[GameObject]):
        pos = game_object_partial.keywords.setdefault("pos", (0, 0))
        pos = pos[0] + self.rect.x, pos[1] + self.rect.y
        game_object_partial(*self.groups(), self.game_objects, self.game_objects, pos=pos)

    def update(self, *args, **kwargs):
        if (self.rect.x, self.rect.y) != (self.last_pos[0], self.last_pos[1]):
            dx = self.rect.x - self.last_pos[0]
            dy = self.rect.y - self.last_pos[1]
            for game_object in self.game_objects:
                game_object.rect.x += dx
                game_object.rect.y += dy

        self.last_pos = self.rect.x, self.rect.y
        self.game_objects.update(*args, **kwargs)

    def image_update(self):
        for game_object in self.game_objects:
            game_object.image_update()


class MyWindow(Window):
    def __init__(self, *groups: Group, **kwargs):
        super().__init__(*groups, **kwargs)
        self.add_game_object(partial(Button,
                                     size=(100, 100), pos=(100, 50), color_fill="white"))
        self.add_game_object(partial(Window,
                                     size=(50, 50), pos=(25, 50), debug=True))

    def update(self, *args, **kwargs):
        self.rect.y += 1 - random() * 2
        self.rect.x += 1 - random() * 2
        super().update()
