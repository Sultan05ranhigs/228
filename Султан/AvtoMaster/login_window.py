from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox, QMessageBox, QGridLayout, QLabel
from PyQt6.QtCore import Qt
import utils
from styles import style

class LoginWindow(QMainWindow):
    def __init__(self, db, controller):
        super().__init__()
        self.db = db
        self.controller = controller
        self.setWindowTitle("Вход")
        self.setGeometry(200, 200, 300, 200)
        utils.center_window(self)

        layout = QVBoxLayout()
        form_widget = QWidget()
        
        title = QLabel("Аутентификация и Регистрация")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout = QGridLayout()
        form_layout.setSpacing(10)
        form_layout.addWidget(title, 0, 0, 1, 2)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Логин")
        form_layout.addWidget(self.username_input, 1, 0)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.password_input, 2, 0)
    
        self.role_select = QComboBox(self)
        self.role_select.addItems(["user", "admin"])
        form_layout.addWidget(self.role_select, 3, 0)

        self.login_button = QPushButton("Войти", self)
        self.login_button.clicked.connect(self.login)
        form_layout.addWidget(self.login_button, 4, 0)

        self.register_button = QPushButton("Регистрация", self)
        self.register_button.clicked.connect(self.register)
        form_layout.addWidget(self.register_button, 5, 0)

        form_widget.setLayout(form_layout)
        layout.addWidget(form_widget, alignment=Qt.AlignmentFlag.AlignCenter)        

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.apply_stylesheet()

    def apply_stylesheet(self):
        self.setStyleSheet(style.base_style)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        
        user = self.db.authenticate_user(username, password)
        if user:
            self.controller.show_main_window(user)  # Переход к MainWindow
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_select.currentText()

        if not username or not password or not role:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        
        if self.db.register_user(username, password, role):
            QMessageBox.information(self, "Успех", "Регистрация успешна")
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким логином уже существует")
