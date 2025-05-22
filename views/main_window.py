import os

import PySide6
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QFileDialog, QHBoxLayout, \
    QComboBox, QFormLayout, QLineEdit, QScrollArea, QToolButton, QSizePolicy, QFrame

from PySide6.QtCore import Qt, QPropertyAnimation, QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CryptoCypher1.0")
        self.setMinimumSize(700, 600)


        central = QWidget(self)
        self.setCentralWidget(central)

        # 1) Wybór pliku:
        self.file_label = QLabel("Nie wybrano pliku.")
        self.file_btn = QPushButton("Wybierz plik")
        self.file_btn.setObjectName("file_button")
        self.file_btn.clicked.connect(self.choose_file)


        # 2) Konfiguracja szyfrowania:
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["ECB", "CBC", "CTR"])

        self.alg_combo = QComboBox()
        self.alg_combo.addItems(["AES", "DES"])

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.iv_edit = QLineEdit()

        self.encrypt_btn = QPushButton("Encrypt")
        self.decrypt_btn = QPushButton("Decrypt")
        self.gen_key_and_iv = QPushButton("Generate Key and IV")

        self.success_txt = QLabel("Operacja zakończona sukcesem!")

        config_container = QWidget()
        config_container.setObjectName("configuration_container")
        config_container.setMaximumWidth(400)



        config_layout = QVBoxLayout(config_container)
        config_layout.setAlignment(PySide6.QtCore.Qt.AlignTop)

        file_layout = QVBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_btn)

        config_layout.addLayout(file_layout)

        form = QFormLayout()
        form.setVerticalSpacing(12)
        form.setHorizontalSpacing(20)

        form.addRow("TRYB:", self.mode_combo)
        form.addRow("ALGORYTM:", self.alg_combo)
        form.addRow("HASŁO:", self.password_edit)
        form.addRow("IV:", self.iv_edit)

        form.addRow(self.encrypt_btn)
        form.addRow(self.decrypt_btn)
        form.addRow(self.gen_key_and_iv)

        collapsible = CollapsibleBox("Testowe ustawienia błędu")
        collapsible.add_widget(QLabel("djfnskd"))


        config_layout.addLayout(form)
        config_layout.addWidget(self.success_txt)
        config_layout.addWidget(collapsible)
        # 3) Główny układ
        main_layout = QHBoxLayout(central)
        main_layout.addLayout(file_layout)
        main_layout.addWidget(config_container)

        #self.setStyleSheet(load_stylesheet())


    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz plik",
            os.path.expanduser("~"),  # katalog domowy jako startowy
            "Pliki tekstowe (*.txt);;Wszystkie pliki (*)"
        )

        if file_path:
            self.select_file_label.setText(f"Wybrano: {os.path.basename(file_path)}")
            self.process_file(file_path) #TODO


class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)

        self.toggle_button = QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { font-weight: bold; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.clicked.connect(self.on_toggle)

        self.content_area = QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.content_area.setFrameShape(QFrame.Shape.NoFrame)
        self.content_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.content_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.toggle_animation = QPropertyAnimation(self.content_area, b"maximumHeight")
        self.toggle_animation.setDuration(200)
        self.toggle_animation.setStartValue(0)
        self.toggle_animation.setEndValue(0)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.content_area)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.content_layout = QVBoxLayout()
        self.content_layout.setAlignment(Qt.AlignTop)
        self.content_widget = QWidget()
        self.content_widget.setLayout(self.content_layout)
        self.content_area.setWidget(self.content_widget)
        self.content_area.setWidgetResizable(True)

    def on_toggle(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow)

        total_height = self.content_widget.sizeHint().height()
        self.toggle_animation.setDirection(
            QPropertyAnimation.Direction.Forward if checked else QPropertyAnimation.Direction.Backward
        )
        self.toggle_animation.setEndValue(total_height)
        self.toggle_animation.start()

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)