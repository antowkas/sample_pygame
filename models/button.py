from typing import Tuple

from pygame import mouse, Color
from pygame.sprite import Group

from .game import GameObject


def pg_color_to_hex(color: Color):
    hex_color = "#%02x%02x%02x" % (color.r, color.g, color.b)
    if color.a != 255:
        hex_color += "%02x" % color.a
    return hex_color


class Button(GameObject):
    def __init__(self, *groups: Group, size=(0, 0), pos=(0, 0), color_fill=Color(0, 0, 0), click_callbacks=None):
        self.is_pressed = False
        self.color_fill = Color(color_fill)
        if click_callbacks is None:
            click_callbacks = []
        self.click_callbacks = click_callbacks

        super().__init__(*groups, size=size, pos=pos)

    def update(self, *args, **kwargs):
        self.get_input()

    def image_update(self):
        self.image.fill(self.color_fill)

    def pressed(self):
        if not self.is_pressed:
            self.clicked()
        self.is_pressed = True

    def clicked(self):
        for callback in self.click_callbacks:
            # CPython
            args = callback.__code__.co_argcount
            if args == 1:
                callback(self)
            else:
                callback()

    def unpressed(self):
        self.is_pressed = False

    def get_input(self):
        mouse_buttons = mouse.get_pressed()
        if mouse_buttons[0]:
            mouse_pos = mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.pressed()
        else:
            self.unpressed()

    def __str__(self):
        res = super().__str__().split(" ")
        res = res[:1] + [pg_color_to_hex(self.color_fill)] + res[1:]
        return " ".join(res)
