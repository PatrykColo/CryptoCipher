import os

import PySide6
from PySide6.QtCore import QDir
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QFileDialog, QHBoxLayout, \
    QComboBox, QFormLayout, QLineEdit, QListWidgetItem, QListWidget, QCheckBox

from controller.controller import encrypt, decrypt, encrypt_any_file, encrypt_bmp_file, \
    decrypt_any_file, decrypt_bmp_file


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.selected_file = None
        self.setWindowTitle("CryptoCypher1.0")
        self.setMinimumSize(900, 600)
        self.selected_path = QDir.homePath()
        self.output_folder = None
        self.modify_byte = False



        central = QWidget(self)
        self.setCentralWidget(central)

        file_container = QWidget()
        file_container.setObjectName("file_container")
        file_container.setMaximumWidth(400)

        # 1) Wybór pliku:
        #self.file_label = QLabel("Nie wybrano pliku.")
        self.file_btn = QPushButton("Wybierz pliki")
        self.file_btn.setObjectName("file_button")
        self.file_btn.clicked.connect(self.open_file_dialog)

        self.file_list_widget = QListWidget()
        self.file_list_widget.itemClicked.connect(self.on_file_selected)

        file_layout = QVBoxLayout(file_container)
        file_layout.setAlignment(PySide6.QtCore.Qt.AlignTop | PySide6.QtCore.Qt.AlignLeft)
        file_layout.addWidget(self.file_btn)
        file_layout.addWidget(self.file_list_widget)


        # 2) Konfiguracja szyfrowania:

        self.selected_file_label = QLabel("Nazwa pliku...")
        self.selected_file_label.setObjectName("selected_file_label")
        self.selected_file_label.setAlignment(PySide6.QtCore.Qt.AlignCenter)
        self.selected_file_label.setContentsMargins(0, 10, 0, 10)

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

        self.config_container = QWidget()
        self.config_container.setObjectName("configuration_container")
        self.config_container.setMaximumWidth(500)



        config_layout = QVBoxLayout(self.config_container)
        config_layout.setAlignment(PySide6.QtCore.Qt.AlignTop)



        #config_layout.addLayout(file_layout)

        form = QFormLayout()
        form.setVerticalSpacing(12)
        form.setHorizontalSpacing(20)

        form.addRow("TRYB:", self.mode_combo)
        form.addRow("ALGORYTM:", self.alg_combo)
        form.addRow("HASŁO:", self.password_edit)



        self.output_dict_label = QLabel(self.selected_path)

        label = QLabel("KATALOG WYJŚCIOWY:")

        self.folder_button = QPushButton()
        self.folder_button.setObjectName("folder_button")
        self.folder_button.setIcon(QIcon("icons/folder.png"))
        self.folder_button.setIconSize(QSize(24, 24))
        self.folder_button.setFixedSize(32, 32)
        self.folder_button.setStyleSheet("border: none;")
        self.folder_button.clicked.connect(self.output_dict_dialog)

        output_layout = QHBoxLayout()
        output_layout.addWidget(label)
        output_layout.addWidget(self.output_dict_label)
        output_layout.addWidget(self.folder_button)

        output_container = QWidget()
        output_container.setObjectName("output_container")
        output_container.setLayout(output_layout)


        testing_section_label = QLabel("Demonstracja modyfikacji szyfrogramu")
        testing_section_label.setContentsMargins(0, 20, 0, 10)

        layout = QHBoxLayout(self)
        layout.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.checkbox = QCheckBox()
        self.checkbox.setObjectName("modify_checkbox")
        self.checkbox.setChecked(False)
        self.checkbox.toggled.connect(lambda checked: setattr(self, 'modify_byte', checked))
        self.label = QLabel("Automatycznie zmodyfikuj losowo wybrany bajt szyfrogramu")

        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)


        #form.addRow("IV:", self.iv_edit)

        #form.addRow(self.encrypt_btn)
        #form.addRow(self.decrypt_btn)

        config_layout.addWidget(self.selected_file_label)
        config_layout.addLayout(form)
        config_layout.addWidget(output_container)
        config_layout.addWidget(self.encrypt_btn)
        config_layout.addWidget(self.decrypt_btn)
        config_layout.addWidget(self.info_box)
        config_layout.addWidget(testing_section_label)
        config_layout.addLayout(layout)


        # 3) Główny układ
        main_layout = QHBoxLayout(central)

        main_layout.addWidget(file_container)
        #main_layout.addLayout(file_layout)
        #main_layout.addLayout(config_layout)
        main_layout.addWidget(self.config_container)
        self.hide_config_container()
        #self.setStyleSheet(load_stylesheet())


    # def choose_file(self):
    #     file_path, _ = QFileDialog.getOpenFileName(
    #         self,
    #         "Wybierz plik",
    #         # os.path.expanduser("~"),  # katalog domowy jako startowy
    #         os.path.abspath("memory/"),
    #         "Wszystkie pliki (*);;Pliki tekstowe (*.txt)"
    #     )
    #
    #     if file_path:
    #         self.selected_file = file_path
    #         self.file_label.setText(f"Wybrano: {os.path.basename(file_path)}")
    #         # print(self.mode_combo.currentText())
    #         # print(self.alg_combo.currentText())
    #         # self.process_file(file_path) #TODO

    def open_file_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Wybierz pliki", os.path.abspath("memory/"))
        if files:
            self.file_list_widget.clear()
            for file_path in files:
                file_name = os.path.basename(file_path)
                item = QListWidgetItem(file_name)
                item.setData(256, file_path)
                self.file_list_widget.addItem(item)

    def on_file_selected(self, item):
        self.show_config_container()
        self.selected_file_label.setText(item.text().upper())
        self.selected_path = item.data(256) #przechowujemy path wybranego pliku

    def output_dict_dialog(self):
        home = QDir.homePath()
        folder = QFileDialog.getExistingDirectory(None, "Wybierz katalog do zapisu", home, options=QFileDialog.ShowDirsOnly)

        if folder:
            self.output_folder = folder
            self.output_dict_label.setText(folder)

    def show_config_container(self):
        self.config_container.setStyleSheet("")
        self.mode_combo.setVisible(True)
        self.alg_combo.setVisible(True)
        self.folder_button.show()
        self.checkbox.setVisible(True)
        self.config_container.setEnabled(True)

    def hide_config_container(self):
        self.config_container.setStyleSheet("background-color: transparent; color: transparent; border: none;")
        self.mode_combo.setVisible(False)
        self.alg_combo.setVisible(False)
        self.folder_button.hide()
        self.checkbox.setVisible(False)
        self.config_container.setEnabled(False)


    def encrypt_file(self):
        f = self.selected_path
        extention = get_file_extension(f)
        alg = self.alg_combo.currentText()
        mode = self.mode_combo.currentText()
        name = os.path.basename(f)[:-4]
        password = self.password_edit.text()
        if password == "":
            self.info_box = "Nie podano hasła"
            return
        output_path = f"{self.output_folder}/{name}_{alg}_{mode}{extention}"
        if extention == '.bmp':
            encrypt_bmp_file(f, output_path, alg, mode, password)
        else:
            encrypt_any_file(f, output_path, alg, mode, password)
        self.info_box = "Szyfrowanie zakończone"

    def decrypt_file(self):
        f = self.selected_path
        extention = get_file_extension(f)
        alg = self.alg_combo.currentText()
        mode = self.mode_combo.currentText()
        name = os.path.basename(f)[:-4]
        password = self.password_edit.text()
        if password == "":
            self.info_box = "Nie podano hasła"
            return
        output_path = f"{self.output_folder}/{name}_{alg}_{mode}{extention}"
        if extention == '.bmp':
            decrypt_bmp_file(f, output_path, alg, mode, password)
        else:
            decrypt_any_file(f, output_path, alg, mode, password)
        self.info_box = "Szyfrowanie zakończone"

def get_file_extension(path: str):
    return os.path.splitext(path)[1]
