from pygame import Surface, SRCALPHA, Rect
from pygame.sprite import Sprite, AbstractGroup


class GameObject(Sprite):
    def __init__(self, *groups: AbstractGroup, size=(0, 0), pos=(0, 0)):
        super().__init__(*groups)

        self.image = Surface(size, SRCALPHA, 32)
        self.rect = Rect(pos, size)
        self.image_update()

    def image_update(self) -> None: ...
