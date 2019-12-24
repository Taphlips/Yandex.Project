# импорт необходимых модулей
import pygame
import sys
import os
from pygame import sprite


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


def terminate():
    pygame.quit()
    sys.exit()


# Класс, создающий кнопку в указанный координатах
class Button:
    def __init__(self,x, y, height, width, text):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text

    def draw(self):
        mp = pygame.mouse.get_pos()

        # Фон кнопки
        fon_image = pygame.transform.scale(load_image('start_menu_button.png'), (self.width, self.height))
        screen.blit(fon_image, (self.x, self.y))

        # Надпись на кнопке
        font = pygame.font.SysFont('comicsans', 60)
        text = font.render(self.text, 1, (0, 0, 0))
        screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        # Если позиция курсора на кнопке, то фон меняется на другую картинку (в данном случае голубая кнопка)
        if self.x < mp[0] < self.x + self.width and self.y < mp[1] < self.y + self.height:
            fon_image = pygame.transform.scale(load_image('menu_button_selected.png'), (self.width, self.height))
            screen.blit(fon_image, (self.x, self.y))
            screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        else:
            fon_image = pygame.transform.scale(load_image('start_menu_button.png'), (self.width, self.height))
            screen.blit(fon_image, (self.x, self.y))
            screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


# класс меню перед игрой
class Menu:
    def __init__(self, width, height):
        self.width = width
        # Создание кнопок с помощью класса Button
        self.start_button = Button(800, 300, 70, 300, 'Играть')
        self.options_button = Button(800, 400, 70, 300, 'Настройки')
        self.exit_button = Button(800, 500, 70, 300, 'Выход')

    def start(self):
        # Основной цико меню
        menu_running = True
        while menu_running:
            mp = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Если нажать ЛКМ
                    if event.button == 1:
                        # по кнопке "Выход"
                        if (self.exit_button.x < mp[0] < self.exit_button.x + self.exit_button.width and
                                self.exit_button.y < mp[1] < self.exit_button.y + self.exit_button.height):
                            terminate()
                        # по кнопке "Настройки" (тут пока ничего нет)
                        elif (self.options_button.x < mp[0] < self.options_button.x + self.options_button.width and
                                self.options_button.y < mp[1] < self.options_button.y + self.options_button.height):
                            # изменение
                            screen.fill((255, 255, 255))
                            options.start()
                        # по кнопке "Играть" (выйдет из цикла меню и войдет в основной цикл с игрой)
                        elif (self.start_button.x < mp[0] < self.start_button.x + self.start_button.width and
                                self.start_button.y < mp[1] < self.start_button.y + self.start_button.height):
                            menu_running = False
            # Название игры вверху экрана
            # изменение
            font = pygame.font.Font(None, 150)
            string_rendered = font.render('YANDEX.GAME', 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.center = self.width // 2, 100
            screen.blit(string_rendered, intro_rect)
            self.start_button.draw()
            self.options_button.draw()
            self.exit_button.draw()
            pygame.display.flip()
            clock.tick(FPS)
        screen.fill((255, 255, 255))
        game.start()

# Пока тестовый класс настроек
class Options:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.btn = Button(800, 300, 70, 300, "Просто")

    def start(self):
        # Надпись настройки
        font = pygame.font.Font(None, 150)
        string_rendered = font.render('НАСТРОЙКИ', 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.center = self.width // 2, 100
        screen.blit(string_rendered, intro_rect)

        # Цикл настроек
        options_running = True
        while options_running:
            mp = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # изменение
                    screen.fill((255, 255, 255))
                    return
            self.btn.draw()
            pygame.display.flip()
            clock.tick(FPS)

# класс игры
class Play:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def start(self):
        flag = 0
        pygame.display.flip()
        game_running = True
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                if event.type == pygame.KEYDOWN:
                    if event.key == 27:
                        game_running = False
                        terminate()
                    elif event.key == 32:
                        flag = True
                        pos = 0
            self.game_draw()
            if flag:
                if pos < 50:
                    Character.jump(hero)
                    pos += 1
                elif pos < 100:
                    Character.fall(hero)
                    pos += 1
                else:
                    flag = False
            pygame.display.flip()

    def game_draw(self):
        screen.fill(pygame.Color('aquamarine'), pygame.Rect(0, 0, self.width, self.height // 15 * 14))
        screen.fill(pygame.Color('peru'), pygame.Rect(0, self.height // 15 * 14, self.width, self.height))
        pygame.draw.circle(screen, pygame.Color('yellow'), (self.width // 15 * 13, self.height // 15 * 2),
                           self.height // 10)
        all_sprites.draw(screen)
        Character.move(hero)


# инициализация pygame
pygame.init()

pygame.display.set_caption('Без названия')
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
surface = pygame.display.get_surface()
x, y = surface.get_width(), surface.get_height()
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
FPS = 50


class Character(sprite.Sprite):
    image = pygame.transform.scale(load_image('Пробник.png'), (100, 100))

    def __init__(self, skin, width, height):
        super().__init__(skin)
        self.image = Character.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = height - (height // 15) - 102

    def move(self):
        self.rect.x += 1

    def jump(self):
        self.rect.y -= 1

    def fall(self):
        self.rect.y += 1


running = True
options = Options(x, y)
menu = Menu(x, y)
game = Play(x, y)

all_sprites = sprite.Group()

hero = Character(all_sprites, x, y)
menu.start()

# Основной цикл (тут будет игра (пока зеленый фон))
while running:
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            running = False
    pygame.display.flip()
pygame.quit()