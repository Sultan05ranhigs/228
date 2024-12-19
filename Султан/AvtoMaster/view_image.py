from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel


class ImageViewer(QDialog):
    """Окно для просмотра увеличенного изображения"""
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Просмотр изображения")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        # Отображение изображения
        image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap.scaled(750, 550, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(image_label)
        self.setLayout(layout)

        # Установить стиль для окна
        self.setStyleSheet("""
        QDialog {
            background-color: #121212; /* Темный фон */
            color: #FFFFFF;
        }
        QLabel {
            border: 1px solid #FFFFFF; /* Белая рамка */
        }
        """)