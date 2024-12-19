base_style = """
QMainWindow {
    background-color: #f5f5f5;
    font: 12px "Arial", sans-serif;
}

QWidget {
    background-color: #ffffff;
    font-size: 14px;
}

QPushButton {
    background-color: #ff9900;
    color: black;
    border-radius: 5px;
    padding: 5px;
    font-weight: bold;
    font-size: 14px;
}

QPushButton#delete_button {
    background-color: red;
    color: white;
}

QPushButton#edit_button {
    background-color: #005a9e;
    color: white;
}

QPushButton:hover {
    background-color: #ffcc66;
}

QPushButton:pressed {
    background-color: #ff9900;
}

QLineEdit, QTableWidget {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 5px;
}

QTableWidget::item {
    padding: 10px;
}
"""