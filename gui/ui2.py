import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QGridLayout, QPushButton, QLabel, 
                               QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette

class ToolButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFixedSize(120, 120)
        self.setStyleSheet("""
            QPushButton {
                background: rgba(80, 80, 80, 120);  /* Semi-transparent */
                border: 2px solid rgba(120, 120, 120, 80);
                border-radius: 15px;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(100, 100, 100, 150);
            }
            QPushButton:pressed {
                background: rgba(60, 60, 60, 180);
            }
        """)

class SidePanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 300)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Enable transparency
        self.setStyleSheet("""
            QFrame {
                background: rgba(60, 60, 60, 120);  /* Semi-transparent */
                border: 2px solid rgba(100, 100, 100, 60);
                border-radius: 20px;
            }
        """)

class ToolkitMainWindow(QMainWindow):
    def __init__(self, background_path=None):
        super().__init__()
        self.setWindowTitle("TOOLKIT")
        self.setFixedSize(1200, 800)
        self.background_path = background_path

        # Set background image or gradient
        self.setup_background()

        # Central widget
        central_widget = QWidget()
        central_widget.setAttribute(Qt.WA_TranslucentBackground)  # Critical for transparency
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(30)

        # Left side panel
        left_panel = SidePanel()
        main_layout.addWidget(left_panel)

        # Center layout
        center_layout = QVBoxLayout()
        center_layout.setSpacing(30)

        # Title label
        title_label = QLabel("TOOLKIT")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                background: rgba(80, 80, 80, 120);  /* Semi-transparent */
                border: 2px solid rgba(120, 120, 120, 80);
                border-radius: 25px;
                color: white;
                font-size: 28px;
                font-weight: bold;
                padding: 20px 40px;
                letter-spacing: 3px;
            }
        """)
        center_layout.addWidget(title_label)

        # Tool grid
        grid_widget = QWidget()
        grid_widget.setFixedSize(380, 380)
        grid_widget.setAttribute(Qt.WA_TranslucentBackground)
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        tool_names = [
            "FILE", "EDIT", "VIEW",
            "TOOLS", "BUILD", "DEBUG",
            "HELP", "SETTINGS", "EXIT"
        ]

        for i in range(3):
            for j in range(3):
                btn = ToolButton(tool_names[i*3 + j])
                btn.clicked.connect(lambda checked, name=tool_names[i*3 + j]: self.tool_clicked(name))
                grid_layout.addWidget(btn, i, j)

        center_layout.addWidget(grid_widget, 0, Qt.AlignCenter)

        main_layout.addLayout(center_layout)

        # Right side panel
        right_panel = SidePanel()
        main_layout.addWidget(right_panel)

    def setup_background(self):
        if self.background_path and os.path.exists(self.background_path):
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-image: url("{self.background_path}");
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                    background-origin: content;
                }}
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background: qradialgradient(cx:0.5, cy:0.3, radius:1.2,
                        stop:0 rgba(120, 120, 120, 255),
                        stop:0.5 rgba(60, 60, 60, 255),
                        stop:1 rgba(0, 0, 0, 255));
                }
            """)

    def tool_clicked(self, tool_name):
        print(f"Tool clicked: {tool_name}")
        if tool_name == "EXIT":
            self.close()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Dark palette for other UI elements
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, Qt.black)
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(dark_palette)

    # Change this to your actual image path
    background_path = r"Z:\Project\Toolkit\Background.png"

    window = ToolkitMainWindow(background_path)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
