import pygame

from models.window2 import Window, MyWindow

pygame.font.init()
pygame.init()


size = width, height = 1000, 800
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
running = True
FPS = 60

all_sprites = pygame.sprite.Group()
# Background(all_sprites, size=(100, 100), color_fill="white")
# MyWindow(all_sprites, size=(500, 500), debug=True)
MyWindow(all_sprites, size=(300, 300), pos=(200, 100), debug=True)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)
