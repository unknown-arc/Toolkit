from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QFileDialog
from PySide6.QtCore import Signal, Qt

class Page2(QWidget):
    download_requested = Signal(str, str, str)  # url, format_id, filename
    location_selected = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.filename_input = QLineEdit()
        self.quality_combo = QComboBox()

        self.location_label = QLabel("Save to: Not selected")
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self._on_browse)

        loc_layout = QHBoxLayout()
        loc_layout.addWidget(self.location_label)
        loc_layout.addWidget(browse_button)

        download_button = QPushButton("Download")
        download_button.clicked.connect(self._on_download)

        layout.addWidget(QLabel("Filename:"))
        layout.addWidget(self.filename_input)
        layout.addWidget(QLabel("Quality:"))
        layout.addWidget(self.quality_combo)
        layout.addLayout(loc_layout)
        layout.addWidget(download_button)

    def _on_browse(self):
        path = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if path:
            self.location_label.setText(f"Save to: {path}")
            self.location_selected.emit(path)

    def _on_download(self):
        filename = self.filename_input.text()
        format_id = self.quality_combo.currentData()
        url = ""  # will be set from main.py controller
        self.download_requested.emit(url, format_id, filename)
