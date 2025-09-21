# downloader_gui.py
"""
PySide6 GUI for Downloader (uses downloader_logic.py).
"""

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QProgressBar, QTextEdit, QComboBox, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal

from downloader_logi import Downloader, safe_filename


# Worker thread for background download
class DownloadWorker(QThread):
    progress = Signal(int)
    status = Signal(str)
    finished_one = Signal(str)
    error = Signal(str)

    def __init__(self, url, outtmpl, format_id, advanced, subtitles, category, extras):
        super().__init__()
        self.url = url
        self.outtmpl = outtmpl
        self.format_id = format_id
        self.advanced = advanced
        self.subtitles = subtitles
        self.category = category
        self.extras = extras
        self.downloader = Downloader(output_path=os.path.dirname(outtmpl) or ".")

    def run(self):
        try:
            self.status.emit("Starting...")

            def hook(d):
                if d.get("status") == "downloading":
                    percent_str = d.get("_percent_str", "0%").replace("%", "")
                    try:
                        percent = int(float(percent_str))
                    except Exception:
                        percent = 0
                    self.progress.emit(percent)
                    self.status.emit(f"⬇ {d.get('_percent_str','')} at {d.get('_speed_str','')}")
                elif d.get("status") == "finished":
                    self.progress.emit(100)
                    self.status.emit("✅ Finished")
                    self.finished_one.emit(d.get("filename", "Done"))

            opts = self.downloader.build_opts(
                self.format_id,
                self.outtmpl,
                self.advanced,
                self.subtitles,
                self.category,
                self.extras,
            )
            self.downloader.download_with_hook(self.url, opts, hook)

        except Exception as e:
            self.error.emit(str(e))


# GUI
class DownloaderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader (yt-dlp)")
        self.setMinimumSize(500, 400)

        self.downloader = Downloader()
        self.worker = None

        # Widgets
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter video URL")

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Default", "Advanced"])

        self.category_combo = QComboBox()
        self.category_combo.addItems(["Audio Only", "Video Only", "Audio + Video"])

        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["best", "worst"])

        self.subs_input = QLineEdit()
        self.subs_input.setPlaceholderText("Subtitle language code (e.g. en)")
        self.subs_input.setEnabled(False)

        self.thumb_check = QCheckBox("Download Thumbnail")
        self.json_check = QCheckBox("Save Metadata JSON")

        self.start_btn = QPushButton("Download")
        self.progress = QProgressBar()
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Video URL:"))
        layout.addWidget(self.url_input)
        layout.addWidget(QLabel("Mode:"))
        layout.addWidget(self.mode_combo)
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(self.category_combo)
        layout.addWidget(QLabel("Quality:"))
        layout.addWidget(self.quality_combo)
        layout.addWidget(self.subs_input)
        layout.addWidget(self.thumb_check)
        layout.addWidget(self.json_check)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.progress)
        layout.addWidget(QLabel("Log:"))
        layout.addWidget(self.log)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connections
        self.mode_combo.currentTextChanged.connect(self.toggle_advanced)
        self.start_btn.clicked.connect(self.start_download)

    def toggle_advanced(self, text):
        advanced = text == "Advanced"
        self.subs_input.setEnabled(advanced)
        self.thumb_check.setEnabled(advanced)
        self.json_check.setEnabled(advanced)

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL")
            return

        category = self.category_combo.currentText()
        quality = self.quality_combo.currentText()
        advanced = self.mode_combo.currentText() == "Advanced"
        subtitles = self.subs_input.text().strip() or None
        extras = {
            "writethumbnail": self.thumb_check.isChecked(),
            "writeinfojson": self.json_check.isChecked(),
            "noplaylist": not advanced,
        }

        format_id = self.downloader.auto_select_format(category, quality)
        outtmpl = f"downloads/{safe_filename('%(title)s')}.%(ext)s"

        self.worker = DownloadWorker(url, outtmpl, format_id, advanced, subtitles, category, extras)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.status.connect(self.log.append)
        self.worker.finished_one.connect(lambda f: self.log.append(f"✅ Saved: {f}"))
        self.worker.error.connect(lambda e: QMessageBox.critical(self, "Error", e))
        self.worker.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = DownloaderGUI()
    gui.show()
    sys.exit(app.exec())
