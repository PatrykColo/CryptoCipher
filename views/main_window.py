import os

import PySide6
from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QFileDialog, QHBoxLayout, \
    QComboBox, QFormLayout, QLineEdit


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
        file_layout = QVBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_btn)

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



        config_container = QWidget()
        config_container.setObjectName("configuration_container")
        config_container.setMaximumWidth(400)

        config_layout = QVBoxLayout(config_container)
        config_layout.setAlignment(PySide6.QtCore.Qt.AlignTop)

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

        config_layout.addLayout(form)

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