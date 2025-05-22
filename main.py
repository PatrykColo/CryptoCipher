import sys
from PySide6.QtWidgets import QApplication
from views.main_window import MainWindow


def load_stylesheet():
    with open("assets/style.qss", "r") as f:
        return f.read()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.setStyleSheet(load_stylesheet())
    window.show()
    sys.exit(app.exec())
