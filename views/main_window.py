import os

import PySide6
from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QFileDialog, QHBoxLayout, \
    QComboBox, QFormLayout, QLineEdit

from controller.controller import encrypt, decrypt, encrypt_any_file, encrypt_bmp_file, \
    decrypt_any_file, decrypt_bmp_file


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.selected_file = None
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
        self.encrypt_btn.clicked.connect(self.encrypt_file)

        self.decrypt_btn = QPushButton("Decrypt")
        self.decrypt_btn.clicked.connect(self.decrypt_file)

        self.gen_key_and_iv = QPushButton("Generate Key and IV")

        self.info_box = QLabel("Operacja zakończona sukcesem!")

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



        config_layout.addLayout(form)
        config_layout.addWidget(self.info_box)
        # 3) Główny układ
        main_layout = QHBoxLayout(central)
        main_layout.addLayout(file_layout)
        main_layout.addWidget(config_container)

        #self.setStyleSheet(load_stylesheet())


    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz plik",
            # os.path.expanduser("~"),  # katalog domowy jako startowy
            os.path.abspath("memory/"),
            "Wszystkie pliki (*);;Pliki tekstowe (*.txt)"
        )

        if file_path:
            self.selected_file = file_path
            self.file_label.setText(f"Wybrano: {os.path.basename(file_path)}")
            # print(self.mode_combo.currentText())
            # print(self.alg_combo.currentText())
            # self.process_file(file_path) #TODO

    def encrypt_file(self):
        f = self.selected_file
        if f is None:
            print("null")
            # self.info_box = "chujnia" #TODO IMPLEMENT CONTAINER WITH INFO WHEN FILE NOT CHOSEN
        # TODO: it's midnight i don't wanna deal with this now
        extention = os.path.splitext(f)
        if extention == '.bmp':
            pass
        else:
            pass

        #encrypt(self.selected_file, self.alg_combo.currentText(), self.mode_combo.currentText(), self.password_edit.text())


    def decrypt_file(self):
        f = self.selected_file
        if f is None:
            print("ups something wrong pls fix me ")
            #self.info_box = "-_-"
        extention = os.path.splitext(f)
        # TODO: or with this
        if extention == '.bmp':
            pass
        else:
            pass
        # decrypt(self.selected_file, self.alg_combo.currentText(), self.mode_combo.currentText(), self.password_edit.text())