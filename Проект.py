# импорт необходимых модулей
import pygame

# класс меню перед игрой
class Menu():
    def __init__(self, width, height):
        self.top = height // 10
        self.left = width // 10
        self.length = width // 5
        self.size = height // 5
        self.height = 3
        self.bns = ['Play', 'Options', 'Exit']
        self.extra()

    def get_button(self, mouse_pos):
        for elem in self.buttons:
            first = elem[0]
            second = elem[1]
            third = elem[2]
            forth = elem[3]
            if first <= mouse_pos[0] <= third and second <= mouse_pos[1] <= forth:
                num = self.buttons.index(elem)
                return num

    def on_click(self, button_coords):
        if button_coords is not None:
            val = self.bns[button_coords]
            print(val)

    def get_click(self, mouse_pos):
        btn = self.get_button(mouse_pos)
        self.on_click(btn)

    def extra(self):
        self.buttons = []
        second = self.top + self.size
        third = self.left + self.length
        forth = second + self.size
        num = 0
        for i in range(self.height):
            # список с координатами "кнопок"
            self.buttons.append((int(self.left * 3.5), second - self.size // 2,
                                 int(third * 3.5), forth - self.size // 2))
            if num == 0:
                txt = 'Play'
            elif num == 1:
                txt = 'Options'
            elif num == 2:
                txt = 'Exit'
            # рисование "кнопок"
            fontObj = pygame.font.Font(None, 100)
            textSurfaceObj = fontObj.render(txt, True, (255, 0, 0, 0))
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (self.left * 5, second)
            screen.blit(textSurfaceObj, textRectObj)

            second += self.size
            forth += self.size
            num += 1



# инициализация pygame
pygame.init()
pygame.display.set_caption('Без названия')
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
surface = pygame.display.get_surface()
x, y = surface.get_width(), surface.get_height()
screen.fill((0, 0, 0))
running = True
menu = Menu(x, y)

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # выход из игры на кнопку Esc(Escape)
            if event.key == 27:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                menu.get_click(event.pos)
    pygame.display.flip()
pygame.quit()