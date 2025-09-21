import sys
import os
import threading

from core import  Downloader, DownloadWorker, url_validator, fetch_info
from gui import VideoDownloaderGUI
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QObject, Signal

'''
class Download:

    # url = input("Enter video URL: ")

    def __init__(self):
        self.url = input("Enter video URL: ")
        self.validate = url_validator(self.url)
        if self.validate.validate_url():
            print("✅ Valid URL")
            self.fetcher = fetch_info()
            video_info = self.fetcher.fetch_basic_info(self.url)
            if video_info:
                print(f"Title: {video_info['title']}")
                print(f"Thumbnail URL: {video_info['thumbnail_url']}")
                print("Available Formats:")
                for fmt in video_info['formats']:
                    print(f" - Format ID: {fmt['format_id']}, Resolution: {fmt.get('resolution', 'N/A')}, Note: {fmt.get('format_note', '')}")
            else:
                print("❌ Failed to fetch video information.")
        else:
            print("❌ Invalid URL") 

    def _start_download(self, format_id):
        def progress_hook(d):
            if d['status'] == 'downloading':
                print(f"⬇ {d['_percent_str']} at {d['_speed_str']}")
            elif d['status'] == 'finished':
                print(f"✅ Download complete: {d['filename']}")

        # Run download in background thread
        threading.Thread(
            target=self.downloader.basic_download,
            args=(self.url, format_id),
            kwargs={'progress_callback': progress_hook},
            daemon=True
        ).start()
        print("Download started in background! You can continue using the app...")
        

if __name__ == "__main__":
    Download()

'''

class Controller:
    def __init__(self):
        # Core logic instances
        self.validator = url_validator()  # URL validation
        self.fetcher = fetch_info()       # Fetch video info
        self.downloader = Downloader()    # Download handler

        # GUI setup
        self.app = QApplication(sys.argv)
        self.gui = VideoDownloaderGUI()

        # Connect GUI signals
        self.gui.page1.fetch_requested.connect(self.handle_fetch)
        self.gui.page2.download_requested.connect(self.handle_download)
        self.gui.page2.location_selected.connect(self.handle_location_selected)

        self.current_url = ""

    # --------------------
    # Fetch video info
    # --------------------
    def handle_fetch(self, url):
        if not self.validator.validate_url(url):
            QMessageBox.warning(self.gui, "Error", "Invalid URL")
            return

        # Run fetch in a thread to prevent GUI freezing
        def fetch_task():
            try:
                info = self.fetcher.fetch_basic_info(url)
                if info:
                    self.current_url = url
                    # Update GUI in main thread
                    self.app.postEvent(self.gui, lambda: self.update_page2(info))
                else:
                    self.app.postEvent(
                        self.gui, 
                        lambda: QMessageBox.warning(self.gui, "Error", "Failed to fetch video info")
                    )
            except Exception as e:
                self.app.postEvent(
                    self.gui, 
                    lambda: QMessageBox.warning(self.gui, "Error", f"Fetch error: {e}")
                )

        threading.Thread(target=fetch_task, daemon=True).start()

    def update_page2(self, info):
        page2 = self.gui.page2
        page2.filename_input.setText(info.get("title", "video"))
        page2.quality_combo.clear()

        for f in info.get("formats", []):
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                label = f"{f.get('height', 'N/A')}p - {f.get('ext')}"
                page2.quality_combo.addItem(label, f['format_id'])

        self.gui.show_page(1)  # Switch to Page2

    # --------------------
    # Download video
    # --------------------
    def handle_download(self, url, format_id, filename):
        if not self.downloader.output_path:
            QMessageBox.warning(self.gui, "Error", "Select download location first")
            return

        # Start download in a separate thread using DownloadWorker
        self.download_worker = DownloadWorker(
            self.downloader, self.current_url, format_id, filename
        )
        self.download_worker.progress.connect(self.on_download_progress)
        self.download_worker.finished.connect(self.on_download_finished)

        threading.Thread(target=self.download_worker.run, daemon=True).start()
        self.gui.show_page(2)  # Show progress page

    def on_download_progress(self, percent):
        page3 = self.gui.page3
        page3.progress_bar.setValue(percent)
        page3.progress_label.setText(f"Downloading... {percent}%")

    def on_download_finished(self):
        page3 = self.gui.page3
        page3.progress_bar.setValue(100)
        page3.progress_label.setText("Download Finished!")
        page3.back_button.show()

    # --------------------
    # Select folder
    # --------------------
    def handle_location_selected(self, path):
        self.downloader.output_path = path

    # --------------------
    # Run app
    # --------------------
    def run(self):
        self.gui.show_page(0)  # Start on Page1
        self.gui.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    Controller().run()
