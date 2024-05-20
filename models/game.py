from pygame import Surface, SRCALPHA, Rect
from pygame.sprite import Sprite, Group


class GameObject(Sprite):
    def __init__(self, *groups: Group, size=(0, 0), coord=(0, 0)):
        super().__init__(*groups)

        self.image = Surface(size, SRCALPHA, 32)
        self.rect = Rect(coord, size)
        self.image_update()

    def image_update(self) -> None: ...
