import os

import PySide6
from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QFileDialog, QHBoxLayout, \
    QComboBox, QFormLayout, QLineEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CryptoCypher1.0")
        self.setMinimumSize(700, 600)


        # Centralny widget (serce GUI)
        # central_widget = QWidget()
        # self.setCentralWidget(central_widget)
        #
        # self.modeSelection = QComboBox()
        # self.modeSelection.addItems(["ECB", "CBC", "CTR"])
        #
        # self.select_file_label = QLabel("Nie wybrano pliku.")
        # self.select_file_btn = QPushButton("Wybierz plik")
        # self.select_file_btn.setObjectName("selectFileBtn")
        #
        # self.select_file_btn.clicked.connect(self.choose_file)
        #
        # key_label = QLabel("HASŁO:")
        # mode_selection_label = QLabel("TRYB:")
        #
        # configuration_container = QWidget()
        # configuration_container.setObjectName("configuration_container")
        #
        #
        # mainLayout = QHBoxLayout()
        # configuration_layout = QVBoxLayout(configuration_container)
        # configuration_layout.setContentsMargins(25, 1, 25, 50)
        #
        # keyConfiguration = QHBoxLayout()
        # modeConfiguration = QHBoxLayout()
        #
        #
        #
        #
        # selection_layout = QVBoxLayout()
        #
        # selection_layout.addWidget(self.select_file_label)
        # selection_layout.addWidget(self.select_file_btn)
        #
        # configuration_layout.setAlignment(PySide6.QtCore.Qt.AlignTop)
        # configuration_layout.addWidget(mode_selection_label)
        # configuration_layout.addWidget(self.modeSelection)
        #
        # mainLayout.addLayout(selection_layout)
        # mainLayout.addLayout(configuration_layout)
        # central_widget.setLayout(mainLayout)


        central = QWidget(self)
        self.setCentralWidget(central)

        # 1) File picker
        self.file_label = QLabel("Nie wybrano pliku.")
        self.file_btn = QPushButton("Wybierz plik")
        self.file_btn.setObjectName("file_button")
        self.file_btn.clicked.connect(self.choose_file)
        file_layout = QVBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_btn)

        # 2) Configuration (mode + password)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["ECB", "CBC", "CTR"])
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        config_container = QWidget()
        config_container.setObjectName("configuration_container")
        config_container.setMaximumWidth(400)

        config_layout = QVBoxLayout(config_container)
        config_layout.setAlignment(PySide6.QtCore.Qt.AlignTop)

        form = QFormLayout()
        form.setVerticalSpacing(12)
        form.setHorizontalSpacing(20)

        form.addRow("TRYB:", self.mode_combo)
        form.addRow("HASŁO:", self.password_edit)
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