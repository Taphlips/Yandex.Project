# импорт необходимых модулей
import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Ошибка', name)
        raise SystemExit(message)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image = image.convert()
        image.set_colorkey(colorkey)
    else:

        image = image.convert_alpha()
    return image


# класс меню перед игрой
class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.intro_text = ["YANDEX.GAME", "", "",
                           "Start new game", "",
                           "Options", "",
                           "Exit"]

        self.fon = pygame.transform.scale(load_image('fon.jpg'), (self.width, self.height))
        screen.blit(self.fon, (0, 0))
        self.text_render()

    def text_render(self):
        font = pygame.font.Font(None, 100)
        text_coord = 100
        for line in self.intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 2
            intro_rect.top = text_coord
            intro_rect.center = self.width // 2, intro_rect.top
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)


# инициализация pygame
pygame.init()

pygame.display.set_caption('Без названия')
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
surface = pygame.display.get_surface()
x, y = surface.get_width(), surface.get_height()
screen.fill((0, 0, 0))
running = True
menu = Menu(x, y)

while running:
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            running = False
    pygame.display.flip()
pygame.quit()
