import os
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QMessageBox, QTableWidget, QTableWidgetItem,
    QInputDialog, QLabel, QFileDialog, QHeaderView, QLineEdit, QDialog
    )
from PyQt6.QtCore import Qt, QSize, QFile, QTextStream
from view_image import ImageViewer
from styles import style
import utils


class MainWindow(QMainWindow):
    def __init__(self, db, user, controller):
        super().__init__()
        self.setGeometry(200, 200, 800, 600)
        utils.center_window(self)
        self.db = db
        self.user_id, self.role = user
        self.controller = controller
        
        self.setWindowTitle("Султан Service")
        layout = QVBoxLayout()
        container = QHBoxLayout()

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Поиск...")
        self.search_field.textChanged.connect(self.filter_table)
        container.addWidget(self.search_field)

        logout_button = QPushButton("Выйти")
        logout_button.clicked.connect(self.logout)
        logout_button.setObjectName("delete_button")
        container.addWidget(logout_button)

        layout.addLayout(container)


        if self.role == "admin":
            self.init_admin_ui(layout)
        else:
            self.init_user_ui(layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.apply_stylesheet()

    def apply_stylesheet(self):
        self.setStyleSheet(style.base_style)

    def init_admin_ui(self, layout):
        """Интерфейс для администратора"""
        self.parts_table = QTableWidget(self)
        self.refresh_parts()
        self.parts_table.setSortingEnabled(True)
        layout.addWidget(self.parts_table)
        buttons_layout = QHBoxLayout()

        add_button = QPushButton("Добавить запчасть", self)
        add_button.clicked.connect(self.add_part)
        add_button.setIcon(QIcon("icons/add.png"))
        buttons_layout.addWidget(add_button)

        edit_button = QPushButton("Изменить запчасть", self)
        edit_button.clicked.connect(self.edit_part)
        edit_button.setIcon(QIcon("icons/edit.png"))
        edit_button.setObjectName("edit_button")
        buttons_layout.addWidget(edit_button)

        delete_button = QPushButton("Удалить запчасть", self)
        delete_button.clicked.connect(self.delete_part)
        delete_button.setIcon(QIcon("icons/delete.png"))
        delete_button.setObjectName("delete_button")
        buttons_layout.addWidget(delete_button)

        export_button = QPushButton("Экспортировать в CSV", self)
        export_button.clicked.connect(self.export_to_csv)
        buttons_layout.addWidget(export_button)

        layout.addLayout(buttons_layout)

    def export_to_csv(self):
        """Экспорт данных запчастей в CSV файл"""
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )

        if not file_name:
            return  # User canceled the dialog

        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                cursor = self.db.conn.cursor()
                cursor.execute("SELECT name, price, purchase_date FROM parts")
                parts = cursor.fetchall()

                file.write("Название,Цена,Дата покупки\n")

                for part in parts:
                    name, price, purchase_date = part
                    file.write(f"{name},{price:.2f},{purchase_date}\n")

            QMessageBox.information(self, "Успех", "Данные успешно экспортированы в CSV файл.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать данные: {str(e)}")

    def init_user_ui(self, layout):
        """Интерфейс для пользователя"""
        self.parts_table = QTableWidget(self)
        self.refresh_parts()
        layout.addWidget(self.parts_table)
        buttons_layout = QHBoxLayout()

        buy_button = QPushButton("Купить", self)
        buy_button.clicked.connect(self.buy_part)
        buttons_layout.addWidget(buy_button)

        history_button = QPushButton("История покупок", self)
        history_button.clicked.connect(self.view_history)
        buttons_layout.addWidget(history_button)

        layout.addLayout(buttons_layout)

    def filter_table(self):
        """Фильтрация таблицы по строкам, кроме столбца с изображениями"""
        search_text = self.search_field.text().lower()

        for row in range(self.parts_table.rowCount()):
            row_visible = False
            for column in range(self.parts_table.columnCount()):
                if column == 3:  # Пропускаем столбец с изображениями
                    continue
                item = self.parts_table.item(row, column)
                if item and search_text in item.text().lower():
                    row_visible = True
                    break

            self.parts_table.setRowHidden(row, not row_visible)

    def refresh_parts(self):
        """Обновление таблицы запчастей"""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, name, price, image, purchase_date FROM parts")
        parts = cursor.fetchall()

        self.parts_table.setRowCount(len(parts))
        self.parts_table.setColumnCount(5)
        self.parts_table.setHorizontalHeaderLabels(["ID", "Название", "Цена", "Опубликовано", "Изображение"])
        self.parts_table.header = self.parts_table.horizontalHeader()
        self.parts_table.header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.parts_table.header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.parts_table.header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.parts_table.header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.parts_table.header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        self.parts_table.verticalHeader().setVisible(False)

        for row, (part_id, name, price, image, purchase_date) in enumerate(parts):
            print(part_id, name, price, image, purchase_date)
            self.parts_table.setRowHeight(row, 80)
            name_item = QTableWidgetItem(name)
            part_id_item = QTableWidgetItem(str(part_id))
            price_item = QTableWidgetItem(f"{price:.2f}")
            date_item = QTableWidgetItem(purchase_date)

            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            part_id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            part_id_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            name_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            price_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            date_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            self.parts_table.setItem(row, 0, part_id_item)
            self.parts_table.setItem(row, 1, name_item)
            self.parts_table.setItem(row, 2, price_item)
            self.parts_table.setItem(row, 3, date_item)

            if image and os.path.exists(image):
                label = QLabel()
                pixmap = QPixmap(image)
                if not pixmap.isNull():
                    label.setPixmap(pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio))
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    label.setStyleSheet("border: 1px solid lightgray; padding: 3px;")
                    label.mousePressEvent = lambda event, img=image: self.open_image_viewer(img)
                    self.parts_table.setCellWidget(row, 4, label)
            else:
                self.parts_table.setItem(row, 4, QTableWidgetItem("Изображение недоступно"))


    def open_image_viewer(self, image_path):
        """Открытие диалогового окна с изображением"""
        viewer = ImageViewer(image_path)
        viewer.exec()

    def add_part(self):
        """Добавление запчасти"""
        name, ok1 = QInputDialog.getText(self, "Добавить запчасть", "Название:")
        if not ok1 or not name:
            return

        price, ok2 = QInputDialog.getDouble(self, "Добавить запчасть", "Цена:")
        if not ok2:
            return

        image_path, _ = QFileDialog.getOpenFileName(self, "Выбрать изображение", "", "Изображения (*.png *.jpg *.jpeg)")
        if not image_path:
            image_path = None

        with self.db.conn:
            self.db.conn.execute(
                "INSERT INTO parts (name, price, image) VALUES (?, ?, ?)",
                (name, price, image_path)
            )
        QMessageBox.information(self, "Успех", "Запчасть добавлена")
        self.refresh_parts()

    def edit_part(self):
        """Изменение запчасти."""
        selected = self.parts_table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запчасть для изменения.")
            return

        part_id = self.parts_table.item(selected, 0).text()
        name, ok = QInputDialog.getText(self, "Изменить запчасть", "Новое название:")
        if not ok or not name.strip():
            return

        price, ok = QInputDialog.getDouble(self, "Изменить запчасть", "Новая цена:", 0, 0, 100000, 2)
        if not ok:
            return

        image_path, _ = QFileDialog.getOpenFileName(self, "Выбрать изображение", "", "Изображения (*.png *.jpg *.jpeg)")
        if image_path:
            with self.db.conn:
                self.db.conn.execute("UPDATE parts SET image = ? WHERE id = ?", (image_path, part_id))

        with self.db.conn:
            self.db.conn.execute("UPDATE parts SET name = ?, price = ? WHERE id = ?", (name, price, part_id))
        QMessageBox.information(self, "Успех", "Запчасть изменена.")
        self.refresh_parts()

    def delete_part(self):
        """Удаление запчасти"""
        selected = self.parts_table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запчасть для удаления")
            return

        part_id = self.parts_table.item(selected, 0).text()
        with self.db.conn:
            self.db.conn.execute("DELETE FROM parts WHERE id = ?", (part_id,))
        self.refresh_parts()

    def buy_part(self):
        """Покупка запчасти"""
        selected = self.parts_table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запчасть для покупки")
            return

        part_id = self.parts_table.item(selected, 0).text()
        with self.db.conn:
            self.db.conn.execute("INSERT INTO purchases (user_id, part_id) VALUES (?, ?)", (self.user_id, part_id))
        QMessageBox.information(self, "Успех", "Покупка выполнена")

    def view_history(self):
        """Просмотр истории покупок"""
        self.view_history_dialog = PurchaseHistoryDialog(self.db.get_purchase_history(self.user_id), parent=self)
        self.view_history_dialog.exec()

    def logout(self):
        """Выход из аккаунта"""
        reply = QMessageBox.question(
            self, "Выход", "Вы уверены, что хотите выйти?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.show_login_window()


class PurchaseHistoryDialog(QDialog):
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("История покупок")
        self.resize(600, 400)

        layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        search_label = QLabel("Поиск:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите текст для поиска")
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Название", "Цена (руб.)", "Дата"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Только для просмотра
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.table)

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.history = history
        self.populate_table(history)

    def populate_table(self, history):
        """Заполняем таблицу данными"""
        self.table.setRowCount(len(history))
        for row, (name, price, _, date) in enumerate(history):
            name_item = QTableWidgetItem(name)
            price_item = QTableWidgetItem(f"{price:.2f}")
            date_item = QTableWidgetItem(date)

            # Выравнивание текста
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, price_item)
            self.table.setItem(row, 2, date_item)

    def filter_table(self):
        """Фильтрация строк в таблице на основе текста поиска"""
        filter_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            is_visible = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if filter_text in item.text().lower():
                    is_visible = True
                    break
            self.table.setRowHidden(row, not is_visible)


    def view_history(self):
        """Просмотр истории покупок"""
        history = self.db.get_purchase_history(self.user_id)
        if not history:
            QMessageBox.information(self, "История", "История покупок пуста")
            return

        # Отображаем диалог с историей покупок
        dialog = PurchaseHistoryDialog(history, parent=self)
        dialog.exec()
    