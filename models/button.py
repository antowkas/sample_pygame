from pygame import mouse, Color
from pygame.sprite import Group

from .game import GameObject


class Button(GameObject):
    def __init__(self, *groups: Group, size=(0, 0), pos=(0, 0), color_fill=Color(0, 0, 0), callbacks=None):
        self.color_fill = color_fill
        self.i = 0

        if callbacks is None:
            callbacks = []
        self.callbacks = callbacks

        super().__init__(*groups, size=size, pos=pos)

    def update(self):
        self.get_input()

    def image_update(self):
        self.image.fill(self.color_fill)

    def pressed(self):
        self.i += 1
        print("press", self.i)
        for callback in self.callbacks:
            callback()

    def get_input(self):
        mouse_buttons = mouse.get_pressed()
        if mouse_buttons[0]:
            mouse_pos = mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.pressed()
