import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt

from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
import sys
import os
from pathlib import Path

def icon_path(asset_name):
    base_dir = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "leftpanel_icons"
    full_path = base_dir / asset_name
    if not full_path.exists():
        print(f"ERROR: File not found at {full_path}")
    return str(full_path)

class IconAndTitle(QPushButton):
    def __init__(self, height=32, parent=None):
        super().__init__(parent)

        name = "Activity"
        default_icon_path = icon_path("activity_icon.svg")
        hover_icon_path = icon_path("activity_icon.svg")

        self.default_icon = QIcon(str(default_icon_path))
        self.hover_icon = QIcon(str(hover_icon_path))
        
        # 1. Set the text (the app name)
        self.setText(name)
        self.setIcon(self.default_icon)

        # 2. Sizing adjustment for text: Fixed height, minimum width for content
        self.setFixedHeight(height)
        self.setMinimumWidth(150) 
        
        # Icon size: Standard size for a 48px height button (e.g., 32x32)
        icon_dim = height - 12
        self.setIconSize(QSize(icon_dim, icon_dim))
        
        # Set object name for specific QSS targeting
        self.setObjectName("IconTextButton") 
        
        # 3. Styling for rectangular button with hover effect
        style_sheet = f"""
            #IconTextButton {{
                /* Base state: transparent background, dark text, rounded corners */
                color: #2D3748; /* Dark gray text */
                background-color: transparent; 
                border: none;
                border-radius: 16 px; /* Rounded rectangular shape */
                text-align: left; /* Aligns text and icon to the left */
                padding: 0px 10px; /* Padding for visual space */
                text-weight: bold;
            }}
            
            #IconTextButton:hover {{
                /* Hover background: light gray (standard navigation hover color) */
                background-color: #ffffff; 
            }}
            
            #IconTextButton:pressed {{
                /* Pressed style: slightly darker for visual feedback */
                background-color: #CBD5E0;
            }}
        """
        self.setStyleSheet(style_sheet)

    def enterEvent(self, event):
        """Changes the icon to the hover icon when the mouse enters."""
        self.setIcon(self.hover_icon)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Changes the icon back to the default icon when the mouse leaves."""
        self.setIcon(self.default_icon)
        super().leaveEvent(event)


class ActivityWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Activity Widget")
        self.setMinimumSize(260, 300)

        # Layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)  # Align content to top-center
        layout.setContentsMargins(0, 0, 0, 0)  # Padding around edges

        
        title_label = IconAndTitle()

        layout.addWidget(title_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ActivityWidget()
    widget.show()
    sys.exit(app.exec())
