from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QProgressBar, QMessageBox, QComboBox
)
from PySide6.QtCore import QThread, Signal
from Downloader import list_formats, download_video

class DownloadThread(QThread):
    progress = Signal(str)

    def __init__(self, url, format_id, subtitles):
        super().__init__()
        self.url = url
        self.format_id = format_id
        self.subtitles = subtitles

    def run(self):
        def hook(d):
            if d['status'] == 'downloading':
                self.progress.emit(f"{d['_percent_str']} at {d['_speed_str']}")
            elif d['status'] == 'finished':
                self.progress.emit("✅ Download complete!")

        download_video(self.url, self.format_id, subtitles=self.subtitles, progress_callback=hook)

class DownloaderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader (yt-dlp)")
        self.setGeometry(200, 200, 500, 500)

        self.formats = []
        self.subs = {}

        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter video URL")
        layout.addWidget(self.url_input)

        self.list_button = QPushButton("Fetch Formats")
        self.list_button.clicked.connect(self.fetch_formats)
        layout.addWidget(self.list_button)

        self.category_label = QLabel("Select Category:")
        layout.addWidget(self.category_label)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["Select", "Video Only", "Audio Only", "Audio + Video"])
        self.category_combo.currentIndexChanged.connect(self.filter_formats)
        layout.addWidget(self.category_combo)

        self.formats_text = QTextEdit()
        self.formats_text.setReadOnly(True)
        layout.addWidget(self.formats_text)

        self.format_box = QLineEdit()
        self.format_box.setPlaceholderText("Enter format ID")
        layout.addWidget(self.format_box)

        self.subtitle_box = QLineEdit()
        self.subtitle_box.setPlaceholderText("Subtitle language (optional)")
        layout.addWidget(self.subtitle_box)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("")
        layout.addWidget(self.progress_label)

        self.setLayout(layout)

    def fetch_formats(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL.")
            return

        self.formats, self.subs = list_formats(url)
        self.formats_text.setText("✅ Formats fetched. Please select a category.")

    def filter_formats(self):
        if not self.formats:
            return

        category = self.category_combo.currentText()
        self.formats_text.clear()

        filtered = []
        for f in self.formats:
            vcodec = f.get('vcodec', 'none')
            acodec = f.get('acodec', 'none')

            if category == "Video Only" and vcodec != "none" and acodec == "none":
                filtered.append(f)
            elif category == "Audio Only" and vcodec == "none" and acodec != "none":
                filtered.append(f)
            elif category == "Audio + Video" and vcodec != "none" and acodec != "none":
                filtered.append(f)

        if filtered:
            for f in filtered:
                self.formats_text.append(
                    f"{f['format_id']:>6} | {f.get('ext',''):<5} | "
                    f"{f.get('resolution',''):<10} | "
                    f"{f.get('filesize','N/A')}"
                )
        else:
            self.formats_text.setText("No formats found for this category.")

    def start_download(self):
        url = self.url_input.text().strip()
        format_id = self.format_box.text().strip()
        subtitles = self.subtitle_box.text().strip() or None

        if not url or not format_id:
            QMessageBox.warning(self, "Error", "Please enter both URL and format ID.")
            return

        self.download_thread = DownloadThread(url, format_id, subtitles)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.start()

    def update_progress(self, text):
        self.progress_label.setText(text)

if __name__ == "__main__":
    app = QApplication([])
    window = DownloaderGUI()
    window.show()
    app.exec()
