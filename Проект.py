# импорт необходимых модулей
import pygame
import sys
import os
from pygame import sprite

# инициализация pygame
pygame.init()


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
    def __init__(self, image, image_act,  screen, x, y, height, width, text):
        self.x = x
        self.image = image
        self.image_act = image_act
        self.screen = screen
        self.y = y
        self.height = height
        self.width = width
        self.text = text

    def draw(self):
        mp = pygame.mouse.get_pos()

        # Фон кнопки
        fon_image = pygame.transform.scale(load_image(self.image), (self.width, self.height))
        self.screen.blit(fon_image, (self.x, self.y))

        # Надпись на кнопке
        font = pygame.font.SysFont('comicsans', 60)
        text = font.render(self.text, 1, (0, 0, 0))
        self.screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        # Если позиция курсора на кнопке, то фон меняется на другую картинку (в данном случае голубая кнопка)
        if self.x < mp[0] < self.x + self.width and self.y < mp[1] < self.y + self.height:
            fon_image = pygame.transform.scale(load_image(self.image_act), (self.width, self.height))
            self.screen.blit(fon_image, (self.x, self.y))
            self.screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        else:
            fon_image = pygame.transform.scale(load_image(self.image), (self.width, self.height))
            self.screen.blit(fon_image, (self.x, self.y))
            self.screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


# класс меню перед игрой
class Menu:
    def __init__(self, width, height):
        self.width = width
        # Создание кнопок с помощью класса Button
        self.start_button = Button('menu_btn.png', 'menu_btn_act.png', menu_screen, 800, 300, 70, 300, 'Играть')
        self.options_button = Button('menu_btn.png', 'menu_btn_act.png', menu_screen, 800, 400, 70, 300, 'Настройки')
        self.exit_button = Button('menu_btn.png', 'menu_btn_act.png', menu_screen, 800, 500, 70, 300, 'Выход')

    def start(self):
        # Основной цикл меню
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
                        # по кнопке "Настройки" выполнит запуск настроек
                        elif (self.options_button.x < mp[0] < self.options_button.x + self.options_button.width and
                                self.options_button.y < mp[1] < self.options_button.y + self.options_button.height):
                            options.start()
                        # по кнопке "Играть" (выйдет из цикла меню и войдет в основной цикл с игрой)
                        elif (self.start_button.x < mp[0] < self.start_button.x + self.start_button.width and
                                self.start_button.y < mp[1] < self.start_button.y + self.start_button.height):
                            menu_running = False
            # Название игры вверху экрана
            font = pygame.font.Font(None, 150)
            string_rendered = font.render('YANDEX.GAME', 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.center = self.width // 2, 100
            menu_screen.blit(string_rendered, intro_rect)
            self.start_button.draw()
            self.options_button.draw()
            self.exit_button.draw()
            pygame.display.flip()
            clock.tick(FPS)
        menu_screen.fill((255, 255, 255))
        game.start()


# Класс настроек
class Options:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.back_to_menu = Button('yellow_back_btn.png', 'blue_back_btn.png', options_screen, 600, 75, 49, 49, "<")

    def start(self):
        menu_screen.fill((255, 255, 255))

        # Цикл настроек
        options_running = True
        while options_running:
            mp = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Если нажать ЛКМ
                    if event.button == 1:
                        # по кнопке "<" холст настроек переключается на холст меню
                        if (self.back_to_menu.x < mp[0] < self.back_to_menu.x + self.back_to_menu.width and
                                self.back_to_menu.y < mp[1] < self.back_to_menu.y + self.back_to_menu.height):
                            # Само переключение:
                            menu_screen.fill((255, 255, 255))
                            options_screen.blit(menu_screen, (0, 0))
                            return
            font = pygame.font.Font(None, 150)
            string_rendered = font.render('OPTIONS', 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.center = self.width // 2, 100
            options_screen.blit(string_rendered, intro_rect)
            self.back_to_menu.draw()
            menu_screen.blit(options_screen, (0, 0))
            pygame.display.flip()
            clock.tick(FPS)


# класс игры
class Play:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def start(self):
        pos = 200
        action = 'jump'
        flag = False
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
                        # прыжок на пробел
                        if flag is False and pos == 200:
                            action = 'jump'
                            flag = True
                            pos = 0
                if event.type == pygame.KEYUP:
                    # остановка прыжка
                    if event.key == 32 and flag is True:
                        flag = False
                        if action == 'jump':
                            action = 'fall'
                            zn = 100 - pos
                            pos = 100 + zn

            self.game_draw()
            # прыжок
            if flag:
                if pos < 100:
                    Character.jump(hero)
                    pos += 2
                elif pos < 200:
                    action = 'fall'
                    Character.fall(hero)
                    pos += 2
                else:
                    action = 'stop'
                    flag = False
            elif action == 'fall' and 100 <= pos < 200 and flag is False:
                Character.fall(hero)
                pos += 2
            pygame.display.flip()

    def game_draw(self):
        # обновление фона
        menu_screen.fill(pygame.Color('aquamarine'), pygame.Rect(0, 0, self.width, self.height // 15 * 14))
        menu_screen.fill(pygame.Color('peru'), pygame.Rect(0, self.height // 15 * 14, self.width, self.height))
        pygame.draw.circle(menu_screen, pygame.Color('yellow'), (self.width // 15 * 13, self.height // 15 * 2),
                           self.height // 10)
        # отрисовка героя
        all_sprites.draw(menu_screen)
        # отрисовка препятствий
        Obstacle.draw_obstacle(barrier)
        # движение героя
        Character.move(hero)
        # обновление камеры
        camera.update(hero)
        for sprite in all_sprites:
            camera.apply(sprite)

# класс Камеры
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dx = 1
        self.dy = 1

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -1
        self.dy = 0

# класс препятствий(тестовый)
class Obstacle:
    def __init__(self, width, height):
        self.fi = width
        self.width = width // 10
        self.height = height
        self.num = 0

    def move_obstacle(self):
        # 4 - скорость движения препятствий навстречу
        if self.fi <= 0 and self.num > 0:
            self.num -= 4
        elif self.fi > 0 and x - self.fi < self.width:
            self.fi -= 4
            self.num += 4
        elif self.num <= 0 and self.fi <= 0:
            self.fi = x
        else:
            self.fi -= 4

    def draw_obstacle(self):
        menu_screen.fill((255, 255, 255), pygame.Rect(self.fi, self.height, self.num,
                                                      self.height))
        self.move_obstacle()

# будущий класс бонусов
class Bonus(Obstacle):
    pass


# Название окна
pygame.display.set_caption('YANDEX.GAME')

# Холст, на котором будет рисоваться меню
menu_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
menu_screen.fill((255, 255, 255))
# Холст, на котором будут рисоваться настройки
options_screen = pygame.Surface(menu_screen.get_size())
options_screen.fill((255, 255, 255))

surface = pygame.display.get_surface()
x, y = surface.get_width(), surface.get_height()
clock = pygame.time.Clock()
FPS = 50


# класс персонажа
class Character(sprite.Sprite):
    # установка спрайта
    image = pygame.transform.scale(load_image('Probnik.png'), (200, 200))
    # зеркалю картинку(просто пример не в ту сторону)
    image = pygame.transform.flip(image, True, False)

    def __init__(self, skin, width, height):
        super().__init__(skin)
        self.image = Character.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = height - (height // 15) * 5 + 10

    def move(self):
        self.rect.x += 1

    # прыжок
    def jump(self):
        self.rect.y -= 2

    # падение
    def fall(self):
        self.rect.y += 2

    def return_x(self):
        return self.rect.x

    def return_y(self):
        return self.rect.y


running = True
options = Options(x, y)
menu = Menu(x, y)
game = Play(x, y)

all_sprites = sprite.Group()

hero = Character(all_sprites, x, y)
barrier = Obstacle(x, 300)
camera = Camera(x, y)
menu.start()