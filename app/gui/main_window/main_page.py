from __future__ import annotations
import platform
import sys
import ctypes
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPalette
from pathlib import Path

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).resolve().parents[2]
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

from gui.main_window.header.header import Header
from gui.main_window.left_panel.LeftPanel import LeftPanel  
from gui.main_window.central_panel.center_panel import CenterPanel
from gui.main_window.right_panel.RightPanel import RightPanel


class MainWindowPage(QWidget): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Toolkit")
        # self.setStyleSheet("background-color: #f4d0cc;")
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_w = screen_geometry.width()
        screen_h = screen_geometry.height()
        min_w = max(700, int(screen_w * 0.35))
        min_h = max(600, int(screen_h * 0.60))
        self.setMinimumSize(min_w, min_h)

        # 3.1. Main Layout: Vertical (Header + Body)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header (Fixed by main_layout)
        self.header = Header(self)
        # self.header.open_settings.connect(self.open_page)
        main_layout.addWidget(self.header)

        # 3.2. Body Layout: Horizontal (Left | Center | Right)
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # Left Panel Setup
        self.left_panel = LeftPanel(self)
        self.left_container = QWidget() # Store container for resize control
        left_layout = QVBoxLayout(self.left_container)  # Margins on the container's layout for spacing (10px padding on all sides of the panel)
        left_layout.setContentsMargins(0, 0, 0, 0) 
        left_layout.setSpacing(0)
        left_layout.addWidget(self.left_panel)
        body_layout.addWidget(self.left_container, 0) 

        # Center Panel Setup
        self.center_container = CenterPanel(self)
        body_layout.addWidget(self.center_container, 1)

        # Right Panel Setup
        self.right_panel = RightPanel(self)
        self.right_container = QWidget() # Store container for resize control
        right_layout = QVBoxLayout(self.right_container)        # Margins on the container's layout for spacing
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        right_layout.addWidget(self.right_panel)
        body_layout.addWidget(self.right_container, 0) 

        # Final setup
        main_layout.addLayout(body_layout, 1) # Body layout takes up remaining vertical space
        self.setLayout(main_layout)



    def resizeEvent(self, event):
        """Centralized event handler to apply dynamic, calculated sizes."""
        new_width = event.size().width()
        new_height = event.size().height()
        
        # 1. Header Height (Based on window height/screen height)
        header_height = max(50, int(new_height * 0.1))
        self.header.setFixedHeight(header_height)

        # 2. Left Panel Width (Based on window width)
        left_target_w = max(300, int(new_width * 0.175))
        self.left_container.setFixedWidth(left_target_w)
        self.left_panel.setFixedWidth(left_target_w )

        # 3. Right Panel Width (Based on window width)
        right_target_w = max(60, int(new_width * 0.04)) 
        self.right_container.setFixedWidth(right_target_w)
        self.right_panel.setFixedWidth(right_target_w)
        
        super().resizeEvent(event)

def main(argv=None) -> int:
    app = QApplication(sys.argv)
    win = MainWindowPage()
    win.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
