# импорт необходимых модулей
import pygame, sys, os, random
from pygame import sprite

# инициализация pygame
pygame.init()
pygame.mixer.music.load("Sound.wav")
click_sound = pygame.mixer.Sound('Click_sound.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0)


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


def restart(width, height):
    global hero, all_sprites, all_objects
    game.over = False
    game.jump_flag = False
    game.score = 0
    game.jump_num = 0
    game.dx = 0
    game.coins = 0
    all_sprites = sprite.Group()
    hero = Character(all_sprites, surface.get_width() // 10 * 3, y)
    all_objects = []
    all_objects.append(Obstacle(all_sprites, surface.get_width() + random.randrange(100, 500),
                                random.randrange(surface.get_height() // 15 * 5, surface.get_height() // 15 * 12),
                                'wrong_answer.png'))
    all_objects.append(Obstacle(all_sprites, surface.get_width() + random.randrange(100, 500) + 350,
                                random.randrange(surface.get_height() // 15 * 5, surface.get_height() // 15 * 12),
                                'wrong_answer.png'))
    all_objects.append(Bonus(all_sprites, surface.get_width() + random.randrange(100, 500) + 1050,
                             surface.get_height() // 10 * 8,
                             'coin.png', 'деньги'))


def boost():
    for i in all_objects:
        i.speed += 1


class Object(sprite.Sprite):
    def __init__(self, skin, image, dx):
        super().__init__(skin)
        self.dx = dx
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = surface.get_width() + self.dx
        self.rect.y = surface.get_height() // 10 * 2

    def move(self):
        if self.rect.x > -260:
            self.rect = self.rect.move(-0.5, 0)
        else:
            self.rect.x = surface.get_width() + self.dx


# Класс, создающий кнопку в указанный координатах
class Button:
    def __init__(self, image, image_act, screen, x, y, height, width, text):
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
        self.music_flag = True
        self.snd_level = 5
        self.width = width
        self.height = height
        # Создание кнопок с помощью класса Button
        x = self.width // 10 * 4
        y = self.height // 10 * 4
        delta_y = self.height // 10
        self.start_button = Button('menu_btn.png', 'menu_btn_act.png', menu_screen, x, y,
                                   70, 300, 'Играть')
        y += delta_y
        self.options_button = Button('menu_btn.png', 'menu_btn_act.png', menu_screen, x, y,
                                     70, 300, 'Настройки')
        y += delta_y
        self.exit_button = Button('menu_btn.png', 'menu_btn_act.png', menu_screen, x, y, 70, 300, 'Выход')

        self.background_image = load_image('game_background_1.png')

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
                            click_sound.play()
                            terminate()
                        # по кнопке "Настройки" выполнит запуск настроек
                        elif (self.options_button.x < mp[0] < self.options_button.x + self.options_button.width and
                              self.options_button.y < mp[1] < self.options_button.y + self.options_button.height):
                            click_sound.play()
                            options.start()
                        # по кнопке "Играть" (выйдет из цикла меню и войдет в основной цикл с игрой)
                        elif (self.start_button.x < mp[0] < self.start_button.x + self.start_button.width and
                              self.start_button.y < mp[1] < self.start_button.y + self.start_button.height):
                            click_sound.play()
                            menu_running = False
                            restart(x, y)
                            game.start()
            # Название игры вверху экрана
            menu_screen.blit(self.background_image, (0, 0))
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


# Класс настроек
class Options:
    def __init__(self, width, height):
        self.snd_flag = False
        self.width = width
        self.height = height
        size = height // 10
        pos_y = height // 10 * 9
        pos_x = height - pos_y - size
        self.back_to_menu = Button('yellow_back_btn.png', 'blue_back_btn.png', options_screen, pos_x, pos_y,
                                   size, size, "<")
        pos_x = width // 10 * 9
        pos_y = height // 10 * 7
        self.less = Button('yellow_back_btn.png', 'blue_back_btn.png', options_screen, pos_x, pos_y,
                           size, size, "-")
        pos_x = width // 10 * 9
        pos_y = height // 10 * 3
        self.more = Button('yellow_back_btn.png', 'blue_back_btn.png', options_screen, pos_x, pos_y,
                           size, size, "+")

        self.background_image = load_image('game_background_1.png')

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
                            click_sound.play()
                            return
                        elif (self.less.x < mp[0] < self.less.x + self.less.width and
                              self.less.y < mp[1] < self.less.y + self.less.height):
                            click_sound.play()
                            self.loudness('-')
                        elif (self.more.x < mp[0] < self.more.x + self.more.width and
                              self.more.y < mp[1] < self.more.y + self.more.height):
                            click_sound.play()
                            self.loudness('+')
            options_screen.blit(self.background_image, (0, 0))
            font = pygame.font.Font(None, 150)
            string_rendered = font.render('OPTIONS', 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.center = self.width // 2, 100
            options_screen.blit(string_rendered, intro_rect)
            self.back_to_menu.draw()
            self.less.draw()
            self.more.draw()
            menu_screen.blit(options_screen, (0, 0))
            if menu.snd_level == 0:
                self.pic_sound('No sound.png', 10)
                pygame.mixer.music.pause()
                menu.music_flag = False
            elif menu.snd_level == 10:
                self.pic_sound('Max sound.png', 7)
            else:
                if self.snd_flag == True:
                    self.snd_flag = False
                    options_screen.fill((255, 255, 255))
            pygame.display.flip()
            clock.tick(FPS)

    def loudness(self, sign):
        snd_lev = menu.snd_level
        if sign == '-' and snd_lev > 0:
            snd_lev -= 1
            pygame.mixer.music.set_volume(snd_lev / 10)
        elif sign == '+' and snd_lev < 10:
            snd_lev += 1
            if menu.music_flag is False:
                pygame.mixer.music.unpause()
                menu.music_flag = True
            pygame.mixer.music.set_volume(snd_lev / 10)
        menu.snd_level = snd_lev

    def pic_sound(self, name, divide):
        self.image = pygame.transform.scale(load_image(name), (self.width // divide, self.width // 10))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        options_screen.blit(self.image, (self.rect.x, self.rect.y))
        self.snd_flag = True


# класс игры
class Play:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.point = 0
        self.jump_flag = False
        self.jump_num = 0
        self.over = False
        self.score = 0
        self.coins = 0
        self.background_image = load_image("game_background_3.png")
        self.dx1 = 0
        self.dx2 = 1920

    def start(self):
        menu_screen.fill((255, 255, 255))
        game_running = True
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                if event.type == pygame.KEYDOWN:
                    if event.key == 27:
                        game_menu.draw_game_menu()
                    elif event.key == 32:
                        # прыжок на пробел
                        self.jump_flag = True
                        self.jump_num += 1
                        if -hero.jump_h < hero.jumpc < hero.jump_h:
                            if self.jump_num < 3:
                                hero.jumpc = hero.jump_h
            self.game_draw()
            if self.score % 100 == 0:
                self.coins += 1
            if self.jump_flag:
                hero.jump()
            if self.over:
                game_over_menu.draw()
            menu_screen.blit(game_screen, (0, 0))
            pygame.display.flip()
            clock.tick(FPS)

    def game_draw(self):
        coin_font = pygame.font.Font(None, 70)

        # Вывод картинки монеты на экран
        coin_image = load_image('coin.png')
        coin_string = coin_font.render('X' + str(int(self.coins)), 1, pygame.Color('black'))
        coin_rect = coin_string.get_rect()
        coin_rect.x, coin_rect.y = surface.get_width() // 20 * 2, surface.get_height() // 20 * 2.2

        score_font = pygame.font.Font(None, 50)
        # Вывод счета игрока на экран:
        score_string = score_font.render('Ваш счет: ' + str(int(self.score)), 1, pygame.Color('black'))
        score_rect = score_string.get_rect()
        score_rect.x, score_rect.y = surface.get_width() // 20, surface.get_height() // 20

        # обновление фона
        game_screen.blit(self.background_image, (self.dx1, 0))
        game_screen.blit(self.background_image, (self.dx2, 0))
        pygame.draw.rect(game_screen, (27, 24, 48),
                         (0, surface.get_height() // 10 * 7 - 20 + 206, surface.get_width(), surface.get_height()))
        game_screen.blit(score_string, score_rect)
        game_screen.blit(coin_string, coin_rect)
        game_screen.blit(coin_image, (surface.get_width() // 20, surface.get_height() // 20 * 2))
        # передвижение препятствий
        # отрисовка героя
        all_sprites.draw(game_screen)
        hero.move()
        hero.update()
        # обновление камеры
        camera.update(hero)
        for i in all_objects:
            i.move_object()
        for sprite in all_sprites:
            camera.apply(sprite)
        self.point += 1


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
        self.dx = len(all_objects) * -1
        self.dy = 0


# меню во время игры
class Game_Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        fi_pos = self.width // 10 * 4
        increment = self.height // 10
        se_pos = self.height // 10 * 3
        self.continue_button = Button('menu_btn.png', 'menu_btn_act.png', menu_screen, fi_pos, se_pos,
                                      70, 300, 'Продолжить')
        se_pos += increment
        self.restart_button = Button('menu_btn.png', 'menu_btn_act.png', menu_screen, fi_pos, se_pos,
                                     70, 300, 'Заново')
        se_pos += increment
        self.exit_button = Button('menu_btn.png', 'menu_btn_act.png', menu_screen, fi_pos, se_pos,
                                  70, 300, 'Выход')

    def draw_game_menu(self):
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
                            click_sound.play()
                            terminate()
                        # по кнопке "Заново"
                        elif (self.restart_button.x < mp[0] < self.restart_button.x + self.restart_button.width and
                              self.restart_button.y < mp[1] < self.restart_button.y + self.restart_button.height):
                            click_sound.play()
                            menu_running = False
                            restart(x, y)
                            game.start()
                        # по кнопке "Продолжить"
                        elif (self.continue_button.x < mp[0] < self.continue_button.x + self.continue_button.width and
                              self.continue_button.y < mp[1] < self.continue_button.y + self.continue_button.height):
                            click_sound.play()
                            return
                if event.type == pygame.KEYDOWN:
                    if event.key == 27:
                        return
            font = pygame.font.Font(None, 150)
            string_rendered = font.render('Пауза', 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.center = self.width // 2, 100
            menu_screen.blit(string_rendered, intro_rect)
            self.continue_button.draw()
            self.restart_button.draw()
            self.exit_button.draw()
            pygame.display.flip()
            clock.tick(FPS)


class Game_Over_menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        x = self.width // 10 * 4
        increment = self.height // 10
        y = self.height // 10 * 3
        self.restart_button = Button('menu_btn.png', 'menu_btn_act.png', menu_screen, x, y,
                                     70, 300, 'Заново')
        y += increment
        self.to_menu = Button('menu_btn.png', 'menu_btn_act.png', menu_screen, x, y,
                              70, 300, 'Главное меню')
        y += increment
        self.exit_button = Button('menu_btn.png', 'menu_btn_act.png', menu_screen, x, y,
                                  70, 300, 'Выход')

    def draw(self):
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
                            click_sound.play()
                            terminate()
                        # по кнопке "Заново"
                        elif (self.restart_button.x < mp[0] < self.restart_button.x + self.restart_button.width and
                              self.restart_button.y < mp[1] < self.restart_button.y + self.restart_button.height):
                            click_sound.play()
                            menu_running = False
                            restart(x, y)
                            game.start()
                        # по кнопке "Выход в меню"
                        elif (self.to_menu.x < mp[0] < self.to_menu.x + self.to_menu.width and
                              self.to_menu.y < mp[1] < self.to_menu.y + self.to_menu.height):
                            click_sound.play()
                            menu_running = False
                            game.over = False
                            menu_screen.fill((255, 255, 255))
                            menu.start()
            font = pygame.font.Font(None, 150)
            string_rendered = font.render('Игра окончена', 1, pygame.Color('red'))
            font2 = pygame.font.Font(None, 80)
            # Строка с результатом (по очкам)(сделай пж такую же, только про монеты)
            score_string = font2.render('Результат: ' + str(int(game.score)), 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.center = self.width // 2, 100
            score_rect = score_string.get_rect()
            score_rect.center = self.width // 2, 220
            menu_screen.blit(string_rendered, intro_rect)
            menu_screen.blit(score_string, score_rect)
            self.to_menu.draw()
            self.restart_button.draw()
            self.exit_button.draw()
            pygame.display.flip()
            clock.tick(FPS)


# Название окна
pygame.display.set_caption('YANDEX.GAME')

# Холст, на котором будет рисоваться меню
menu_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
menu_screen.fill((255, 255, 255))
# Холст, на котором будут рисоваться настройки
options_screen = pygame.Surface(menu_screen.get_size())
options_screen.fill((255, 255, 255))
# Холст, на котором будет рисоваться игра
game_screen = pygame.Surface(menu_screen.get_size())
game_screen.fill((255, 255, 255))

surface = pygame.display.get_surface()
x, y = surface.get_width(), surface.get_height()
clock = pygame.time.Clock()
FPS = 80


# класс персонажа
class Character(sprite.Sprite):
    def __init__(self, skin, width, height):
        super().__init__(skin)

        self.run_frames = []
        self.cut_sheet(load_image("First skin.png"), 6, 1, 'r_f')
        self.cur_frame = 0
        self.image = self.run_frames[self.cur_frame]

        self.jump_frames = []
        self.cut_sheet(load_image("Second skin.png"), 6, 1, 'j_f')

        self.fall_frames = []
        self.cut_sheet(load_image("Third skin.png"), 6, 1, 'f_f')

        self.rect = self.rect.move(x, y)
        self.rect.x = width // 2
        self.jump_h = 20
        self.jumpc = self.jump_h
        self.rect.y = surface.get_height() // 10 * 7 - 20
        self.const = height - (height // 15) * 5 + 10
        self.speed = 1
        self.tank = False
        self.last_update = pygame.time.get_ticks()
        self.frames = self.run_frames
        self.flag = 'run'

    def move(self):
        if self.tank:
            for i in all_objects:
                if not pygame.sprite.collide_mask(self, i):
                    self.rect.x += self.speed
                    game.score += 0.1
                else:
                    pass
        else:
            for i in all_objects:
                if not pygame.sprite.collide_mask(self, i):
                    self.rect.x += self.speed
                    game.score += 0.1
                else:
                    i.rect.x = 20000
                    i.function()
        game.dx1 -= 8
        game.dx2 -= 8

        if game.dx1 < -1920:
            game.dx1 = 1920

        if game.dx2 < -1920:
            game.dx2 = 1920

    def cut_sheet(self, sheet, columns, rows, name):
        new = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                new.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

        if name == 'r_f':
            self.run_frames = new
        elif name == 'j_f':
            self.jump_frames = new
        elif name == 'f_f':
            self.fall_frames = new

    # прыжок
    def jump(self):
        if self.jumpc >= -self.jump_h:
            self.rect.y -= self.jumpc
            self.jumpc -= 1
            if self.jumpc > 0:
                self.frames = self.jump_frames
            elif self.jumpc < 0:
                self.frames = [self.fall_frames[5]]
        else:
            if self.rect.y < surface.get_height() // 10 * 7 - 20:
                self.rect.y = min(surface.get_height() // 10 * 7 - 20, self.rect.y - self.jumpc)
                self.jumpc -= 1
            else:
                self.jumpc = self.jump_h
                game.jump_flag = False
                game.jump_num = 0
                self.frames = self.run_frames

    def jump_back(self):
        x_count = 20
        y_count = 10
        if y_count >= -10 and x_count >= -20:
            self.rect.y -= y_count
            self.rect.x -= x_count
            x_count -= 2

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.ch_mask = pygame.mask.from_surface(self.image)
            self.last_update = now


# класс препятствий
class Obstacle(sprite.Sprite):
    def __init__(self, skin, x, y, image):
        super().__init__(skin)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.ob_mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def move_object(self):
        if self.rect.x > -200:
            self.rect.x -= self.speed
        else:
            self.rect.x = self.x
            self.rect.y = self.y

    def function(self):
        game.over = True


# будущий(уже настоящий) класс бонусов
class Bonus(sprite.Sprite):
    def __init__(self, skin, x, y, image, func):
        super().__init__(skin)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.ob_mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.func = func
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def move_object(self):
        if self.rect.x > -200:
            self.rect.x -= self.speed
        else:
            self.rect.x = self.x
            self.rect.y = self.y

    def function(self):
        if self.func == 'ускорение':
            for i in all_objects:
                i.speed += 5
        elif self.func == 'танк':
            hero.tank = True
        elif self.func == 'высокие прыжки':
            hero.jump_h = 25
        elif self.func == 'деньги':
            game.coins += 3


all_sprites = sprite.Group()

running = True
options = Options(x, y)
menu = Menu(x, y)
game = Play(x, y)

hero = Character(all_sprites, surface.get_width() // 10 * 3, y)
camera = Camera(x, y)
game_menu = Game_Menu(x, y)
game_over_menu = Game_Over_menu(x, y)
menu.start()
