from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Signal, Qt
from core import url_validator as UrlValidator  # ✅ import the function

class Page1(QWidget):
    fetch_requested = Signal(str)  # Signal to send URL to main.py

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Enter Video URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://...")

        fetch_button = QPushButton("Next")
        fetch_button.clicked.connect(self._on_next)

        layout.addWidget(label)
        layout.addWidget(self.url_input)
        layout.addWidget(fetch_button)

    def _on_next(self):
        url = self.url_input.text().strip()
        self.fetch_requested.emit(url)
        # if UrlValidator.validate_url(url):   # ✅ uses static method
        #     self.url_submitted.emit(url)     # send URL to main.py
        # else:
        #     self.label.setText("❌ Invalid URL, try again")