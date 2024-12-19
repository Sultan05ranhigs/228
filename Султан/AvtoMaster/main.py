from PyQt6.QtWidgets import QApplication
from database import Database
from login_window import LoginWindow


from PyQt6.QtWidgets import QApplication
from login_window import LoginWindow
from main_window import MainWindow

class AppController:
    """Класс для управления окнами приложения"""
    def __init__(self, db):
        self.db = db
        self.app = QApplication([])

        self.login_window = LoginWindow(self.db, self)
        self.main_window = None

    def show_login_window(self):
        """Отобразить окно авторизации"""
        if self.main_window:
            self.main_window.close()
        self.login_window = LoginWindow(self.db, self)
        self.login_window.show()

    def show_main_window(self, user):
        """Отобразить главное окно"""
        self.login_window.close()
        self.main_window = MainWindow(self.db, user, self)
        self.main_window.show()

    def run(self):
        """Запуск приложения"""
        self.login_window.show()
        self.app.exec()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    db = Database()
    app_controller = AppController(db)
    app_controller.run()
