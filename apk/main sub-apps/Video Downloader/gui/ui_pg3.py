from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton
from PySide6.QtCore import Qt

class Page3(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.progress_label = QLabel("Downloading...")
        self.progress_label.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar()

        self.back_button = QPushButton("Download Another Video")
        self.back_button.hide()  # only show after download completes

        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.back_button)
