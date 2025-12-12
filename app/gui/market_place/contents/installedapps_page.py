from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QFrame,
    QScrollArea, QSizePolicy
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QSize, Qt
from pathlib import Path
import sys
import os

# --- ICON PATH WITH WHITE SVG FALLBACK ---
def icon_path(asset_name):
    base_dir = Path(__file__).resolve().parent.parent.parent / "assets" / "marketplace_icons"
    full_path = base_dir / asset_name 
    
    placeholder_name = "white_placeholder.svg"
    placeholder_path = Path.cwd() / placeholder_name
    
    if full_path.exists():
        return str(full_path)
    else:
        # Create a simple white SVG circle file if the real icon is missing
        if not placeholder_path.exists():
             try:
                 svg_content = """<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="24" cy="24" r="24" fill="white"/>
                                  </svg>"""
                 with open(placeholder_path, 'w') as f:
                     f.write(svg_content)
             except Exception as e:
                 print(f"ERROR: Could not create placeholder file: {e}")
                 return "" 
                 
        return str(placeholder_path)


class AppTile(QFrame):
    """A widget representing a single installed application in the list."""
    def __init__(self, app_name, version, icon_path_str, parent=None):
        super().__init__(parent)
        self.app_name = app_name
        
        # Style for the item frame
        self.setStyleSheet("""
            AppTile {
                background-color: #ffffff; /* White background for the tile */
                border: 1px solid #dddddd;
                border-radius: 8px;
                margin-bottom: 5px;
            }
            AppTile:hover {
                background-color: #f0f0f0; 
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                font-weight: bold;
            }
        """)
        self.setFixedHeight(80) 
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 5, 15, 5)

        # --- 1. Icon (Will be white if real icon fails) ---
        icon_label = QLabel()
        icon = QIcon(icon_path_str)
        icon_label.setPixmap(icon.pixmap(QSize(48, 48)))
        icon_label.setFixedSize(48, 48)
        main_layout.addWidget(icon_label)
        
        # --- 2. Name and Version Info (Vertical Stack) ---
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        name_label = QLabel(f"**{app_name}**")
        name_label.setFont(QFont("Segoe UI", 12))
        name_label.setTextFormat(Qt.TextFormat.RichText)
        
        version_label = QLabel(f"Version: {version}")
        version_label.setFont(QFont("Segoe UI", 9))
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(version_label)
        
        main_layout.addLayout(info_layout)
        main_layout.addStretch(1) 

        # --- 3. Action Buttons ---
        
        # Button 1: Launch/Open (Using the light blue color from previous steps)
        launch_btn = QPushButton("Launch")
        launch_btn.setFixedSize(80, 30)
        launch_btn.setStyleSheet("""
            QPushButton {
                background-color: #4fc3f7; /* Light Blue */
                color: white; 
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #03a9f4;
            }
        """)
        launch_btn.clicked.connect(lambda: print(f"Launched {app_name}"))
        
        # Button 2: Uninstall (Subtle style)
        uninstall_btn = QPushButton("Uninstall")
        uninstall_btn.setFixedSize(80, 30)
        uninstall_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                color: #555555; 
                border: 1px solid #aaaaaa;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #dddddd;
            }
        """)
        uninstall_btn.clicked.connect(lambda: print(f"Uninstalled {app_name}"))
        
        main_layout.addWidget(launch_btn)
        main_layout.addWidget(uninstall_btn)


### 2. InstalledPage Widget (The Scrolling List)

class InstalledPage(QWidget):
    """The main view for installed applications, featuring a scrollable list."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Installed Applications")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # --- Header ---
        header = QLabel("<h2>Installed Applications (13)</h2>")
        header.setStyleSheet("color: #333333; margin-bottom: 10px;")
        header.setTextFormat(Qt.TextFormat.RichText)
        main_layout.addWidget(header)
        
        # --- Scrollable Area ---
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        self.list_layout = QVBoxLayout(content_widget)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop) 
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        self._load_apps() 

    def _load_apps(self):
        """Populates the list with dummy data."""
        apps_data = [
            ("Video Editor Pro", "3.1.2", "video_icon.svg"),
            ("Design Studio Lite", "10.0.5", "design_icon.svg"),
            ("Data Analyzer", "4.5.0", "data_icon.svg"),
            ("Gaming Hub", "1.9.3", "game_icon.svg"),
            # Intentional failures to show white fallback
            ("Missing App Icon", "1.0.0", "non_existent_icon.png"), 
            ("File Organizer", "2.0.1", "file_icon.svg"),
            ("Code Editor X", "12.0.0", "code_icon.svg"),
            ("Music Player Beta", "0.9.1", "music_icon.svg"),
            ("Virtual Desktop", "1.1.0", "desktop_icon.svg"),
            ("PDF Viewer", "5.2.2", "pdf_icon.svg"),
            ("Backup Utility", "3.0.0", "backup_icon.svg"),
            ("System Monitor", "1.0.4", "monitor_icon.svg"),
            ("Image Resizer", "6.1.1", "resize_icon.svg"),
            ("Chat Client", "7.3.0", "chat_icon.svg"),
        ]
        
        for name, version, icon_file in apps_data:
            icon_path_str = icon_path(icon_file) # Uses the shared icon_path function
            app_tile = AppTile(name, version, icon_path_str)
            self.list_layout.addWidget(app_tile)
        
        self.list_layout.addStretch(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # ⚠️ NOTE: This will create a 'white_placeholder.svg' file in your directory
    # if it doesn't already exist or if any app icons are missing.
    
    installed_page = InstalledPage()
    installed_page.show()
    
    sys.exit(app.exec())