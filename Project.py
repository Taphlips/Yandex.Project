# импорт необходимых модулей
import pygame, sys, os, random, sqlite3
from pygame import sprite

# изъятие громкости из базы данных, чтобы подстроиться под пользователя
con = sqlite3.connect('For project.db')
cur = con.cursor()
result = cur.execute("""SELECT Loudness FROM Players
                            WHERE Nickname = 'Player'""").fetchall()
song_result = cur.execute("""SELECT Song FROM Players
                            WHERE Nickname = 'Player'""").fetchall()
result = result[0][0]
song_result = song_result[0][0]
con.close()

# инициализация pygame
pygame.init()
pygame.mixer.music.load(song_result)
click_sound = pygame.mixer.Sound('Click_sound.wav')
pygame.mixer.music.set_volume(result * 0.1)
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
    game.active_bonuses = 0
    game.jump_boost = False
    game.boost = False
    game.tank = False
    all_sprites = sprite.Group()
    hero = Character(all_sprites, surface.get_width() // 10 * 3, y)
    all_objects = [Obstacle(all_sprites, surface.get_width() + 50,
                            surface.get_height() // 10 * 7 - 14, 'wrong_answer.png'),
                   Obstacle(all_sprites, surface.get_width() + 150,
                            surface.get_height() // 10 * 7 + 36, 'wrong_answer2.png'),
                   Obstacle(all_sprites, surface.get_width() + 800,
                            surface.get_height() // 10 * 7 - 14, 'wrong_answer.png'),
                   Obstacle(all_sprites, surface.get_width() + 1500,
                            surface.get_height() // 10 * 7 + 36, 'wrong_answer2.png'),
                   Bonus(all_sprites, surface.get_width() + 3200,
                         surface.get_height() // 10 * 7 - 30, 'jump_boost.png', 'высокие прыжки'),
                   Bonus(all_sprites, surface.get_width() + 2000,
                         surface.get_height() // 10 * 7 - 30, 'boost.png', 'ускорение'),
                   Bonus(all_sprites, surface.get_width() + 500,
                         surface.get_height() // 10 * 7 - 30, 'tank.png', 'танк'),
                   Bonus(all_sprites, surface.get_width() + 4000,
                         surface.get_height() // 10 * 7 - 30, 'coin.png', 'деньги')]


def rad(array):
    maxi = max(array[0].rect.x, array[1].rect.x, array[2].rect.x, array[3].rect.x)
    if maxi < surface.get_width():
        rad = surface.get_width()
        if rad - maxi < 250:
            rad += 100
    else:
        rad = maxi

    ch = random.randint(0, 4)
    if ch == 0:
        rad += random.randrange(100, 150)
    else:
        rad += random.randrange(200, 300)

    return rad


def draw_objects(array):
    for o in array:
        check = o.move_object()
        if not check:
            radius = rad(array)
            o.move(radius)


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
        self.snd_level = result
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
        if song_result == 'Sound.wav':
            self.song = 'Billy'
        elif song_result == 'Sound 2.wav':
            self.song = 'Slipknot'
        elif song_result == 'Психободун.wav':
            self.song = 'Eminem'

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

        pos_x = width // 10 * 3
        pos_y = height // 10 * 3
        self.first = Button('yellow_back_btn.png', 'blue_back_btn.png', options_screen, pos_x, pos_y,
                            int(1.5 * size), 7 * size, "Billy Talent - Red Flag")

        pos_x = width // 10 * 3
        pos_y = height // 10 * 5
        self.second = Button('yellow_back_btn.png', 'blue_back_btn.png', options_screen, pos_x, pos_y,
                             int(1.5 * size), 7 * size, "Slipknot - Psychosocial")

        pos_x = width // 10 * 3
        pos_y = height // 10 * 7
        self.third = Button('yellow_back_btn.png', 'blue_back_btn.png', options_screen, pos_x, pos_y,
                            int(1.5 * size), 7 * size, "Не включать(включать)")

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
                        elif (self.first.x < mp[0] < self.first.x + self.first.width and
                              self.first.y < mp[1] < self.first.y + self.first.height):
                            click_sound.play()
                            self.change('Billy')
                        elif (self.second.x < mp[0] < self.second.x + self.second.width and
                              self.second.y < mp[1] < self.second.y + self.second.height):
                            click_sound.play()
                            self.change('Slipknot')
                        elif (self.third.x < mp[0] < self.third.x + self.third.width and
                              self.third.y < mp[1] < self.third.y + self.third.height):
                            click_sound.play()
                            self.change('Eminem')
            options_screen.blit(self.background_image, (0, 0))
            font = pygame.font.Font(None, 150)
            string_rendered = font.render('OPTIONS', 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.center = self.width // 2, 100
            options_screen.blit(string_rendered, intro_rect)
            self.back_to_menu.draw()
            self.less.draw()
            self.more.draw()
            self.first.draw()
            self.second.draw()
            self.third.draw()
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

        # обновление громкости в бд
        con = sqlite3.connect('For project.db')
        cur = con.cursor()
        cur.execute("""UPDATE Players
                            SET Loudness = ?
                            WHERE Nickname = 'Player'""", (snd_lev,))
        con.commit()
        con.close()

    def pic_sound(self, name, divide):
        self.image = pygame.transform.scale(load_image(name), (self.width // divide, self.width // 10))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        options_screen.blit(self.image, (self.rect.x, self.rect.y))
        self.snd_flag = True

    # смена песни
    def change(self, name):
        if name != self.song:
            pygame.mixer.music.stop()
            if name == 'Billy':
                self.song = 'Billy'
                song_result = 'Sound.wav'
                pygame.mixer.music.load("Sound.wav")
            elif name == 'Slipknot':
                self.song = 'Slipknot'
                song_result = 'Sound 2.wav'
                pygame.mixer.music.load("Sound 2.wav")
            elif name == 'Eminem':
                self.song = 'Eminem'
                song_result = 'Психободун.wav'
                pygame.mixer.music.load("Психободун.wav")
            pygame.mixer.music.play(-1, 0.0)

            con = sqlite3.connect('For project.db')
            cur = con.cursor()
            cur.execute("""UPDATE Players
                                    SET Song = ?
                                    WHERE Nickname = 'Player'""", (song_result,))
            con.commit()
            con.close()


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

        self.active_bonuses = 0

        self.jump_boost = False
        self.jump_image = load_image('jump_boost.png')

        self.boost = False
        self.boost_image = load_image('boost.png')

        self.tank = False
        self.tank_image = load_image('tank.png')

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
                         (0, surface.get_height() // 10 * 7 + 186, surface.get_width(), surface.get_height()))
        game_screen.blit(score_string, score_rect)
        game_screen.blit(coin_string, coin_rect)
        game_screen.blit(coin_image, (surface.get_width() // 20, surface.get_height() // 20 * 2))
        if self.active_bonuses == 1:
            if self.boost:
                game_screen.blit(self.boost_image, (surface.get_width() // 20, surface.get_height() // 20 * 3.5))
            if self.jump_boost:
                game_screen.blit(self.jump_image, (surface.get_width() // 20, surface.get_height() // 20 * 3.5))
            if self.tank:
                game_screen.blit(self.tank_image, (surface.get_width() // 20, surface.get_height() // 20 * 3.5))
        else:
            if self.boost:
                game_screen.blit(self.boost_image, (surface.get_width() // 20, surface.get_height() // 20 * 3.5))
            if self.jump_boost:
                game_screen.blit(self.jump_image, (surface.get_width() // 20 + 80, surface.get_height() // 20 * 3.5))
            if self.tank:
                game_screen.blit(self.tank_image, (surface.get_width() // 20 + 160, surface.get_height() // 20 * 3.5))
        # передвижение препятствий
        # отрисовка героя
        all_sprites.draw(game_screen)
        hero.move()
        hero.update()
        # обновление камеры
        camera.update(hero)
        draw_objects(all_objects)
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
        self.menu_button = Button('menu_btn.png', 'menu_btn_act.png', menu_screen, fi_pos, se_pos,
                                  70, 300, 'Главное меню')

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
                        elif (self.menu_button.x < mp[0] < self.menu_button.x + self.menu_button.width and
                              self.menu_button.y < mp[1] < self.menu_button.y + self.menu_button.height):
                            click_sound.play()
                            menu_running = False
                            game.over = False
                            menu_screen.fill((255, 255, 255))
                            menu.start()
                if event.type == pygame.KEYDOWN:
                    if event.key == 27:
                        return
            font = pygame.font.Font(None, 150)
            string_rendered = font.render('Пауза', 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x, intro_rect.y = self.width // 10 * 4, 100
            menu_screen.blit(string_rendered, intro_rect)
            self.continue_button.draw()
            self.restart_button.draw()
            self.exit_button.draw()
            self.menu_button.draw()
            pygame.display.flip()
            clock.tick(FPS)


class Game_Over_menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        x = self.width // 10 * 4
        increment = self.height // 10
        y = self.height // 10 * 4
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
                            self.salary()
                            self.record()
                            terminate()
                        # по кнопке "Заново"
                        elif (self.restart_button.x < mp[0] < self.restart_button.x + self.restart_button.width and
                              self.restart_button.y < mp[1] < self.restart_button.y + self.restart_button.height):
                            click_sound.play()
                            self.salary()
                            self.record()
                            menu_running = False
                            restart(x, y)
                            game.start()
                        # по кнопке "Выход в меню"
                        elif (self.to_menu.x < mp[0] < self.to_menu.x + self.to_menu.width and
                              self.to_menu.y < mp[1] < self.to_menu.y + self.to_menu.height):
                            click_sound.play()
                            self.salary()
                            self.record()
                            menu_running = False
                            game.over = False
                            menu_screen.fill((255, 255, 255))
                            menu.start()
            font = pygame.font.Font(None, 150)
            string_rendered = font.render('Игра окончена', 1, pygame.Color('red'))
            font2 = pygame.font.Font(None, 80)
            # Строка с результатом (по очкам)
            score_string = font2.render(f'Результат: {str(int(game.score))}', 1, pygame.Color('red'))
            coin_string = font2.render(
                f'Монет собрано: {str(int(game.coins))} + монеты за очки: {str(int(game.score // 100))}', 1,
                pygame.Color('red'))
            intro_rect = string_rendered.get_rect()
            intro_rect.center = self.width // 2, 100
            score_rect = score_string.get_rect()
            score_rect.center = self.width // 2, 220
            coin_rect = coin_string.get_rect()
            coin_rect.center = self.width // 2, 340
            menu_screen.blit(string_rendered, intro_rect)
            menu_screen.blit(score_string, score_rect)
            menu_screen.blit(coin_string, coin_rect)
            self.to_menu.draw()
            self.restart_button.draw()
            self.exit_button.draw()
            pygame.display.flip()
            clock.tick(FPS)

    def salary(self):
        # добавление денег к существущей сумме(пока не для чего - только в планах)
        con = sqlite3.connect('For project.db')
        cur = con.cursor()
        coins = cur.execute("""SELECT Coins FROM Players
                                WHERE Nickname = 'Player'""").fetchall()
        coins = coins[0][0]
        coins += game.coins
        cur.execute("""UPDATE Players
                        SET Coins = ?
                        WHERE Nickname = 'Player'""", (coins,))
        con.commit()
        con.close()

    def record(self):
        # записывание наибольшего количества очков в таблицу
        con = sqlite3.connect('For project.db')
        cur = con.cursor()
        points = cur.execute("""SELECT Record FROM Players
                                WHERE Nickname = 'Player'""").fetchall()
        points = points[0][0]
        if points < int(game.score):
            points = int(game.score)
            cur.execute("""UPDATE Players
                            SET Record = ?
                            WHERE Nickname = 'Player'""", (points,))
            con.commit()
        con.close()


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
        self.jump_h = 23
        self.jumpc = self.jump_h
        self.rect.y = surface.get_height() // 10 * 7 - 20
        self.const = height - (height // 15) * 5 + 10
        self.speed = 1
        self.tank = False
        self.last_update = pygame.time.get_ticks()
        self.frames = self.run_frames
        self.flag = 'run'
        self.new_time = 0
        self.bns = ''
        self.fon_speed = 13

    def move(self):
        if self.tank:
            for i in all_objects:
                if not pygame.sprite.collide_mask(self, i):
                    self.rect.x += self.speed
                    game.score += 0.1
                else:
                    self.rect.x += self.speed
                    game.score += 0.1
        else:
            for i in all_objects:
                if not pygame.sprite.collide_mask(self, i):
                    self.rect.x += self.speed
                    game.score += 0.1
                else:
                    i.rect.x = 2000
                    i.function()
                    self.bns = i

        game.dx1 -= self.fon_speed
        game.dx2 -= self.fon_speed

        if game.dx1 < -1920:
            game.dx1 = 1920

        if game.dx2 < -1920:
            game.dx2 = 1920

        # проверка на наличие и длительность бонуса
        if self.bns != '' and type(self.bns) == Bonus:
            if self.bns.flag[0] is True:
                self.new_time = pygame.time.get_ticks()
                if self.new_time - self.bns.last_update > 5000:
                    name = self.bns.flag[1]
                    self.bns.flag = [False, name]
                    self.bns.anti(name)

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

    # обновление кадров
    def update(self):
        now = pygame.time.get_ticks()
        # частота обновления анимации героя
        if now - self.last_update > 80:
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
            return True
        else:
            return False

    def function(self):
        game.over = True

    def move(self, rad):
        self.rect.x = rad


# класс бонусов
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
        self.flag = [False, 'kek']
        self.rect.bottom = surface.get_height() // 10 * 7 + 186

    def move_object(self):
        if self.rect.x > -200:
            self.rect.x -= self.speed
            return True
        else:
            return False

    def function(self):
        if self.func == 'ускорение':
            for i in all_objects:
                i.speed += 3
            hero.fon_speed += 3
            name = 'speed'
            game.active_bonuses += 1
            game.boost = True
        elif self.func == 'танк':
            hero.tank = True
            name = 'Tank'
            game.active_bonuses += 1
            game.tank = True
        elif self.func == 'высокие прыжки':
            if not game.jump_flag:
                hero.jump_h = 26
                name = 'high_jumps'
                game.active_bonuses += 1
                game.jump_boost = True
            else:
                name = 'high_jumps'
                game.jump_boost = True
        elif self.func == 'деньги':
            game.coins += 3
            name = 'coins'
        self.flag = [True, name]
        self.last_update = pygame.time.get_ticks()

    # метод отката бонуса
    def anti(self, name):
        if name == 'speed':
            for i in all_objects:
                i.speed -= 3
            hero.fon_speed -= 3
            game.active_bonuses -= 1
            game.boost = False
        elif name == 'Tank':
            hero.tank = False
            game.active_bonuses -= 1
            game.tank = False
        elif name == 'high_jumps':
            hero.jump_h = 23
            game.active_bonuses -= 1
            game.jump_boost = False
        hero.bns = ''

    def move(self, rad):
        self.rect.x = rad


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
