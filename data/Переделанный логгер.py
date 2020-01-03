import sys, sqlite3, time, socket, os
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QVBoxLayout, QMessageBox
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QPushButton, QSizePolicy, QHBoxLayout
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from random import choice, randint


class Registration(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('Свин.jpg'))
        self.i, okIsPressed = QInputDialog.getItem(self, "Семья свинов",
                                                   "Подтвердите, что вы не робот! Как зовут дочь отца Свинки Пеппы!",
                                                   ("Джордж", "Мама Свин", "Свинка Пеппа", "Папа Свин"), 0, False)
        if okIsPressed is True and self.i == 'Свинка Пеппа':
            self.initUI()
        elif okIsPressed is True and self.i != 'Свинка Пеппа':
            self.setWindowTitle('Wasted')
            self.setWindowIcon(QIcon('Крест.jpg'))
            self.loser = QPixmap('Потрачено.jpg')
            self.image = QLabel(self)
            self.move(0, 0)
            self.image.resize(self.loser.width(), self.loser.height())
            self.image.setPixmap(self.loser)
            self.show()

    def initUI(self):
        # начальный пользовательский интерфейс
        self.setGeometry(0, 0, 240, 240)
        self.move(200, 200)

        self.setWindowTitle('Регистрация')
        self.setWindowIcon(QIcon('Иконка.png'))
        self.setWindowOpacity(1)
        self.setFixedSize(250, 250)

        self.first_label = QLabel(self)
        self.first_label.setText('Придумайте, пожалуйста, новый логин!')
        self.first_label.resize(self.first_label.sizeHint())
        self.first_label.move(20, 10)

        self.reg = QPushButton('Зарегистрироваться', self)
        self.reg.resize(self.reg.sizeHint())
        self.reg.move(65, 110)
        self.reg.setStyleSheet('QPushButton {background-color: yellow}')
        self.reg.clicked.connect(self.registration)

        self.name = QLineEdit(self)
        self.name.resize(self.first_label.sizeHint())
        self.name.move(20, 30)

        self.se_label = QLabel(self)
        self.se_label.setText('Придумайте оригинальный пароль!')
        self.se_label.resize(self.se_label.sizeHint())
        self.se_label.move(20, 50)

        self.pas_field = QLineEdit(self)
        self.pas_field.resize(self.first_label.sizeHint())
        self.pas_field.move(20, 70)

        self.exists = QLabel(self)
        self.exists.setText('Уже есть аккаунт?')
        self.exists.move(140, 200)

        self.login = QPushButton('Войти', self)
        self.login.resize(95, 20)
        self.login.setStyleSheet('QPushButton {background-color: pink}')
        self.login.move(140, 215)
        self.login.clicked.connect(self.log_in)

        self.show()

    def registration(self):
        self.add = self.name.text()
        self.pas = self.pas_field.text()
        if self.add != '' and self.pas != '' and len(self.add) < 16:
            # подключение к базе данных Users
            con = sqlite3.connect('Пользователи.db')
            cur = con.cursor()
            check_result = cur.execute("""SELECT User FROM Users""").fetchall()
            check_result = list(map(lambda x: str(x).lstrip("('").rstrip("')',"), check_result))
            # проверяем, существует ли уже игрок с данным именем
            if self.add in check_result:
                self.error = QMessageBox.critical(self, 'Ошибка', 'Такое имя уже существует!', QMessageBox.Ok)
            else:
                # внесение нового пользователся
                result = cur.execute("""INSERT INTO Users(User, Password) VALUES(?, ?)
                                    """, (self.add, self.pas))
                con.commit()
                con.close()
                self.close()
                self.success('Регистрация завершена!')
        # выводим ошибки при заполнении полей
        elif len(self.add) > 16:
            self.error = QMessageBox.critical(self, 'Ошибка', 'Длина имени превышает 16 символов!', QMessageBox.Ok)
        elif self.add != '' and self.pas == '':
            self.error = QMessageBox.critical(self, 'Ошибка', 'Вы не указали пароль!', QMessageBox.Ok)
        elif self.add == '' and self.pas != '':
            self.error = QMessageBox.critical(self, 'Ошибка', 'Вы не указали логин!', QMessageBox.Ok)
        else:
            self.error = QMessageBox.critical(self, 'Ошибка', 'Вы не ввели ни имя, ни пароль!', QMessageBox.Ok)

    def log_in(self):
        # закрываем окно регистрации и переходим к окну входа
        self.close()
        jo.show()

    def success(self, nadpis):
        # выводим пользователю окно "Успех!" в случае входа или регистрации
        self.notice = QMessageBox.about(self, 'Успех!', nadpis)
        # меняем имя игрока в уже заготовленном окне теста
        Exercise.change(self)
        # показываем окно теста
        ex.show()

    def return_name(self):
        return self.add


class Join(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # начальный пользовательский интерфейс
        # установка гифки
        self.gif = QMovie('Вход гифка.gif')
        self.setGeometry(240, 240, 340, 340)
        self.im = QLabel()
        self.im.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.im.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout()
        self.layout.addStretch(1)
        self.layout.addWidget(self.im)
        verticalSpacer = QSpacerItem(300, 450, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(verticalSpacer)
        self.setLayout(self.layout)
        self.gif.setCacheMode(QMovie.CacheAll)
        self.gif.setSpeed(100)
        self.im.setMovie(self.gif)
        self.gif.start()

        self.setWindowTitle('Вход')
        self.setWindowIcon(QIcon('Вход.png'))
        self.setFixedSize(450, 200)

        self.nik_label = QLabel('Введите существующий логин!', self)
        self.nik_label.resize(self.nik_label.sizeHint())
        self.nik_label.move(20, 90)

        self.nik = QLineEdit(self)
        self.nik.resize(self.nik_label.sizeHint())
        self.nik.move(20, 110)

        self.password_label = QLabel('Введите подходящий пароль!', self)
        self.password_label.resize(self.password_label.sizeHint())
        self.password_label.move(20, 130)

        self.password_line = QLineEdit(self)
        self.password_line.resize(self.password_label.sizeHint())
        self.password_line.move(20, 150)

        self.enter_button = QPushButton('Войти', self)
        self.enter_button.move(45, 170)
        self.enter_button.setStyleSheet('QPushButton {background-color: sandybrown}')
        self.enter_button.clicked.connect(self.enter)

        self.ip = socket.gethostbyname(socket.gethostname())
        self.time_label = QLabel(self.ip, self)
        self.time_label.resize(self.time_label.sizeHint())
        self.time_label.move(370, 180)

    def enter(self):
        self.add = self.nik.text()
        self.pas = self.password_line.text()
        if self.add != '' and self.pas != '':
            # подключаемся к базе данных Users
            con = sqlite3.connect('Пользователи.db')
            cur = con.cursor()
            check_result = cur.execute("""SELECT User FROM Users""").fetchall()
            check_result = list(map(lambda x: str(x).lstrip("('").rstrip("')',"), check_result))
            check_pas = cur.execute("""SELECT Password FROM Users""").fetchall()
            check_pas = list(map(lambda x: str(x).lstrip("('").rstrip("')',"), check_pas))
            # проверяем, существует ли введённый пользователь
            if self.add in check_result and self.pas in check_pas:
                con.close()
                self.close()
                Registration.success(self, 'Вход выполнен!')
            else:
                self.error = QMessageBox.critical(self, 'Ошибка', 'Такого аккаунта нет!', QMessageBox.Ok)
        # выводим ошибки при заполнении полей
        elif self.add != '' and self.pas == '':
            self.error = QMessageBox.critical(self, 'Ошибка', 'Вы не указали пароль!', QMessageBox.Ok)
        elif self.add == '' and self.pas != '':
            self.error = QMessageBox.critical(self, 'Ошибка', 'Вы не указали логин!', QMessageBox.Ok)
        else:
            self.error = QMessageBox.critical(self, 'Ошибка', 'Вы не ввели ни имя, ни пароль!', QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    reg = Registration()
    jo = Join()
    reg.show()
    sys.exit(app.exec_())