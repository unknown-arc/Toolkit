# gui.py
from PySide6.QtWidgets import (
    QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QProgressBar, QFileDialog, QMessageBox
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap
import requests

class VideoDownloaderGUI(QWidget):
    # Signals to communicate with main.py
    fetch_requested = Signal(str)
    download_requested = Signal(str, str, str)
    location_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Downloader")
        self.setMinimumSize(500, 450)

        self.download_path = ""
        self.thumbnail_pixmap = None

        # Stack widget to hold pages
        self.stack = QStackedWidget(self)
        self.page1 = self._create_url_page()
        self.page2 = self._create_options_page()
        self.page3 = self._create_progress_page()

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.stack.addWidget(self.page3)

        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

    # --- Page 1: Enter URL ---
    def _create_url_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Enter Video URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://...")

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self._on_next_page1)

        layout.addWidget(label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.next_button)
        return page

    def _on_next_page1(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL")
            return
        # Emit signal to main.py to validate and fetch info
        self.fetch_requested.emit(url)

    # --- Page 2: Options / Info ---
    def _create_options_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        self.thumbnail_label = QLabel()
        self.thumbnail_label.setAlignment(Qt.AlignCenter)

        self.filename_input = QLineEdit()
        self.quality_combo = QComboBox()

        loc_layout = QHBoxLayout()
        self.location_label = QLabel("Save to: Not selected")
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self._on_browse)
        loc_layout.addWidget(self.location_label)
        loc_layout.addWidget(browse_button)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self._on_download)

        layout.addWidget(self.thumbnail_label)
        layout.addWidget(QLabel("Filename:"))
        layout.addWidget(self.filename_input)
        layout.addWidget(QLabel("Quality:"))
        layout.addWidget(self.quality_combo)
        layout.addLayout(loc_layout)
        layout.addWidget(self.download_button)
        return page

    def _on_browse(self):
        path = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if path:
            self.download_path = path
            self.location_label.setText(f"Save to: {path}")
            self.location_selected.emit(path)

    def _on_download(self):
        url = self.url_input.text()
        filename = self.filename_input.text()
        format_id = self.quality_combo.currentData()
        if not self.download_path:
            QMessageBox.warning(self, "Error", "Select download location first")
            return
        self.download_requested.emit(url, format_id, filename)
        # Switch to progress page
        self.stack.setCurrentWidget(self.page3)

    # --- Page 3: Progress ---
    def _create_progress_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        self.progress_thumbnail_label = QLabel()
        self.progress_thumbnail_label.setAlignment(Qt.AlignCenter)
        self.progress_filename_label = QLabel("Filename: ")
        self.progress_location_label = QLabel("Location: ")
        self.progress_bar = QProgressBar()
        self.progress_status_label = QLabel("Starting download...")
        self.progress_status_label.setAlignment(Qt.AlignCenter)
        self.back_button = QPushButton("Download Another Video")
        self.back_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.page1))
        self.back_button.hide()

        layout.addWidget(self.progress_thumbnail_label)
        layout.addWidget(self.progress_filename_label)
        layout.addWidget(self.progress_location_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_status_label)
        layout.addWidget(self.back_button)
        return page

    # --- Helper methods called from main.py ---
    def update_video_info(self, info: dict):
        self.filename_input.setText(info.get("title", "video"))
        self.quality_combo.clear()
        for f in info.get("formats", []):
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                label = f"{f.get('height', 'N/A')}p - {f.get('ext')}"
                self.quality_combo.addItem(label, f['format_id'])
        if info.get("thumbnail"):
            try:
                response = requests.get(info["thumbnail"])
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.thumbnail_label.setPixmap(pixmap.scaledToWidth(320, Qt.SmoothTransformation))
            except:
                pass

    def update_progress(self, percent, status=""):
        self.progress_bar.setValue(percent)
        self.progress_status_label.setText(status)
