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
        self.offset = pos
        self.game_objects: Group[GameObject] = Group()
        self.last_game_objects: set[GameObject] = set()

        super().__init__(*groups, size=size, pos=pos)
        self.last_pos = self.rect.x, self.rect.y

        self.debug_color = generate_random_color() if debug else None
        if self.debug_color is not None:
            draw.rect(self.image, self.debug_color, (0, 0, self.rect.width, self.rect.height), 5)

    def add_game_object(self, game_object_partial: partial[GameObject]) -> GameObject:
        game_object = game_object_partial(self.game_objects)
        self.update_new_object(game_object)
        return game_object

    def update(self, *args, **kwargs):
        self.update_new_objects()
        self.update_objects_pos()

    def update_new_objects(self):
        new_game_objects = self.find_new_game_object()
        if new_game_objects:
            for game_object in new_game_objects:
                self.update_new_object(game_object)

    def find_new_game_object(self):
        set_game_objects = set(self.game_objects)
        return set_game_objects - self.last_game_objects

    def update_new_object(self, game_object):
        game_object.rect.x += self.offset[0]
        game_object.rect.y += self.offset[1]
        if isinstance(game_object, Window):
            game_object.last_pos = game_object.rect.x, game_object.rect.y
        for group in self.groups():
            group.add(game_object)
        self.last_game_objects.add(game_object)

    def update_objects_pos(self):
        if (self.rect.x, self.rect.y) != (self.last_pos[0], self.last_pos[1]):
            dx = self.rect.x - self.last_pos[0]
            dy = self.rect.y - self.last_pos[1]
            self.offset = (self.offset[0] + dx, self.offset[1] + dy)
            for game_object in self.game_objects:
                if isinstance(game_object, Window):
                    game_object.last_pos = (game_object.last_pos[0] + dx, game_object.last_pos[1] + dy)
                game_object.rect.x += dx
                game_object.rect.y += dy
        self.last_pos = self.rect.x, self.rect.y

    def image_update(self):
        for game_object in self.game_objects:
            game_object.image_update()


class MyWindow(Window):
    def __init__(self, *groups: Group, **kwargs):
        super().__init__(*groups, **kwargs)
        self.add_game_object(partial(Button,
                                     size=(100, 100), pos=(100, 125), color_fill="white"))
        # self.w: Window = self.add_game_object(partial(Window,
        #                                  size=(50, 50), pos=(25, 50), debug=True))

        self.w = Window(self.game_objects, size=(50, 50), pos=(25, 25), debug=True)

        # Тут нет ошибки
        # https://youtrack.jetbrains.com/issue/PY-45958/Type-error-sorting-Iterable-of-dataclassorderTrue-instances
        self.w.game_objects.add(Button(size=(100, 100), pos=(25, 25), color_fill=Color(0, 255, 128, 128),
                                       click_callbacks=(lambda x: print(str(x)),)))

    def update(self, *args, **kwargs):
        self.rect.y += 1 - random() * 2
        self.rect.x += 1 - random() * 2
        super().update()
