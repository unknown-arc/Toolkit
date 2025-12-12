from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
import sys
import os
from pathlib import Path
import os


def icon_path(asset_name):
    # base_dir = Path(__file__).resolve().parents[3] / "assets" / "header_icons"
    base_dir = Path(__file__).resolve().parent.parent.parent / "assets" / "quicklab_icons"
    full_path = base_dir / asset_name 
    print(f"Base directory for assets: {base_dir}")
    # print(f"Checking path existence: {full_path}")
    if not full_path.exists():
        print(f"ERROR: File not found at {full_path}")
    # else:
        # print(f"SUCCESS: File exists at {full_path}")
    return str(full_path)


class IconButton(QPushButton):

    def __init__(self, name, default_icon_path, hover_icon_path, bg_color = "transparent", size=QSize(48, 48), parent=None):
        super().__init__(parent)

        # self.icon_name = name
        self.default_icon = QIcon(str(default_icon_path))
        self.hover_icon = QIcon(str(hover_icon_path))
        
        # Button size and icon size
        self.setFixedSize(size)
        icon_dim = min(size.width(), size.height()) - 24  
        self.setIconSize(QSize(icon_dim, icon_dim))
        self.setFlat(True)
        self.setIcon(self.default_icon)
        self.setToolTip(name)

        # --- FIX: Use the passed bg_color here ---
        style_sheet = f"""
            IconButton {{
                /* Base state: Use the dynamic bg_color parameter */
                background-color: {bg_color}; 
                border: none;
                border-radius: {size.width() // 2}px; /* Makes it a perfect circle */
                
                /* Smooth transition for size and color */
                transition: background-color 0.2s, transform 0.2s; 
            }}
            
            IconButton:hover {{
                /* Hover background: Use a slightly transparent white for hover */
                background-color: rgba(255, 255, 255, 0.7); 
                
                /* Hover effect: slightly bigger (1.1x scale) */
                transform: scale(1.1); 
            }}
            
            /* Keep the icon centered and ensure it doesn't move */
            IconButton::icon {{
                padding: 0px; 

            ToolTip {{
                background-color: black;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }}    
            }}

        """
        self.setStyleSheet(style_sheet)

    def enterEvent(self, event):
        self.setIcon(self.hover_icon)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.default_icon)
        super().leaveEvent(event)


class MikeButton(IconButton):
    def __init__(self, parent=None):
        super().__init__("Mike", icon_path("mike_icon.svg"), icon_path("mike_hover_icon.svg"), parent=parent)

class AddFileButton(IconButton):
    def __init__(self, parent=None):
        super().__init__("Add File", icon_path("addfile_icon.svg"), icon_path("addfile_hover_icon.svg"), parent=parent)   

class SendMessageButton(IconButton):
    def __init__(self, parent=None):
        # Passes the blue color that is now correctly applied in the base class.
        super().__init__("Send Message", icon_path("send_icon.svg"), icon_path("send_hover_icon.svg"), parent=parent)

# bg_color="#1E90FF"        