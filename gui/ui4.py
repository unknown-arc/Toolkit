import sys
import os
import ctypes
from ctypes import wintypes
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QPushButton, QLabel, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QPixmap, QPainter

# from downloader_gui import Downloader  # Assuming Downloader is defined in downloader_logi.py

# from downloader_gui import DownloaderGUI

# def open_video_downloader(self):
#     self.downloader_window = DownloaderGUI()
#     self.downloader_window.show()

# === Win32 Frosted Glass Structures ===
class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [
        ("AccentState", ctypes.c_int),
        ("AccentFlags", ctypes.c_int),
        ("GradientColor", ctypes.c_int),
        ("AnimationId", ctypes.c_int)
    ]

class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ("Attribute", ctypes.c_int),
        ("Data", ctypes.c_void_p),
        ("SizeOfData", ctypes.c_size_t)
    ]

def enable_glass(hwnd, gradient_color=0x90000000):  
    """
    Apply acrylic blur.
    gradient_color = 0xAABBGGRR (ARGB)
    AA = Alpha (opacity), higher = more solid.
    Example: 0x90FFFFFF = 144 alpha, white blur tint.
    """
    accent = ACCENT_POLICY()
    accent.AccentState = 3  # ACCENT_ENABLE_BLURBEHIND
    accent.GradientColor = gradient_color
    data = WINDOWCOMPOSITIONATTRIBDATA()
    data.Attribute = 19  # WCA_ACCENT_POLICY
    data.SizeOfData = ctypes.sizeof(accent)
    data.Data = ctypes.addressof(accent)
    ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.byref(data))

# === Frosted Glass Panel ===
class FrostedPanel(QFrame):
    def __init__(self, width=200, height=300, radius=20, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(width, height)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.radius = radius
        self.setStyleSheet(f"""
            QFrame {{
                background: rgba(40, 40, 40, 40); /* transparent base for blur */
                border: 2px solid rgba(150, 150, 150, 60);
                border-radius: {radius}px;
            }}
        """)

    def showEvent(self, event):
        if sys.platform.startswith("win"):
            hwnd = self.winId().__int__()
            enable_glass(hwnd, gradient_color=0x90FFFFFF)  # strong blur

# === Frosted Glass Button ===
class FrostedButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFixedSize(120, 120)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QPushButton {
                background: rgba(40, 40, 40, 40);
                border: 2px solid rgba(150, 150, 150, 60);
                border-radius: 15px;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(80, 80, 80, 80);
            }
            QPushButton:pressed {
                background: rgba(20, 20, 20, 120);
            }
        """)

    def showEvent(self, event):
        if sys.platform.startswith("win"):
            hwnd = self.winId().__int__()
            enable_glass(hwnd, gradient_color=0x10FFFFFF)  # medium blur

# === Frosted Glass Title Panel ===
class FrostedTitle(QLabel):
    def __init__(self, text="TOOLKIT", parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(80)
        self.setAlignment(Qt.AlignCenter)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QLabel {
                background: rgba(40, 40, 40, 40);
                border: 2px solid rgba(150, 150, 150, 60);
                border-radius: 25px;
                color: white;
                font-size: 28px;
                font-weight: bold;
                letter-spacing: 3px;
                padding: 20px 40px;
            }
        """)

    def showEvent(self, event):
        if sys.platform.startswith("win"):
            hwnd = self.winId().__int__()
            enable_glass(hwnd, gradient_color=0x90FFFFFF)  # same as panels

# === Main Window ===
class ToolkitMainWindow(QMainWindow):
    def __init__(self, background_path=None):
        super().__init__()
        self.setWindowTitle("TOOLKIT")
        self.resize(1200, 800)  # resizable
        self.background_pixmap = QPixmap(background_path) if background_path and os.path.exists(background_path) else None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(30)

        # Left frosted panel
        left_panel = FrostedPanel()
        main_layout.addWidget(left_panel)

        # Center layout
        center_layout = QVBoxLayout()
        center_layout.setSpacing(30)

        # Title with frosted effect
        title_label = FrostedTitle()
        center_layout.addWidget(title_label)

        # Frosted button grid
        grid_widget = QWidget()
        grid_widget.setFixedSize(380, 380)
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        tool_names = [
            "Video Downloader", "EDIT", "VIEW",
            "TOOLS", "BUILD", "DEBUG",
            "HELP", "SETTINGS", "EXIT"
        ]

        for i in range(3):
            for j in range(3):
                btn = FrostedButton(tool_names[i*3 + j])
                btn.clicked.connect(lambda checked, name=tool_names[i*3 + j]: self.tool_clicked(name))
                grid_layout.addWidget(btn, i, j)

        center_layout.addWidget(grid_widget, 0, Qt.AlignCenter)
        main_layout.addLayout(center_layout)

        # Right frosted panel
        right_panel = FrostedPanel()
        main_layout.addWidget(right_panel)

    def paintEvent(self, event):
        """Draw background image if available."""
        if self.background_pixmap:
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), self.background_pixmap)

    def tool_clicked(self, tool_name):
        print(f"Tool clicked: {tool_name}")
        if tool_name == "Video Downloader":
            self.open_video_downloader()
        elif tool_name == "EXIT":
            self.close()        

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, Qt.black)
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(dark_palette)

    background_path = r"Z:\Project\Toolkit\assests\Background.png"
    window = ToolkitMainWindow(background_path)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
