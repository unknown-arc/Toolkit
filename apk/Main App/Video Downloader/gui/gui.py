from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from PySide6.QtCore import Qt
from .ui_pg1 import Page1
from .ui_pg2 import Page2
from .ui_pg3 import Page3

class VideoDownloaderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Downloader")
        self.setMinimumSize(500, 450)
        self.setStyleSheet("background-color: #f5f5f5;")  # example background

        # --- Stacked Widget ---
        self.stack = QStackedWidget(self)

        # --- Pages ---
        self.page1 = Page1()
        self.page2 = Page2()
        self.page3 = Page3()

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.stack.addWidget(self.page3)

        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

    def show_page(self, index):
        """Switch page by index (0,1,2)"""
        self.stack.setCurrentIndex(index)
