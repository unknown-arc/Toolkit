from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from pathlib import Path


def icon_path(asset_name):
    base_dir = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "rightpanel_icons"
    full_path = base_dir / asset_name
    # print(f"Checking path existence: {full_path}")
    if not full_path.exists():
        print(f"ERROR: File not found at {full_path}")
    # else:
        # print(f"SUCCESS: File exists at {full_path}")
    return str(full_path)


class IconButton(QPushButton):
    def __init__(self, name, default_icon_path, hover_icon_path, size=QSize(48, 48), parent=None):
        super().__init__(parent)

        self.default_icon = QIcon(str(default_icon_path))
        self.hover_icon = QIcon(str(hover_icon_path))
        
        self.setFixedSize(size)
        icon_dim = min(size.width(), size.height()) - 24  
        self.setIconSize(QSize(icon_dim, icon_dim))
        self.setFlat(True)
        self.setIcon(self.default_icon)
        self.setToolTip(name)

        style_sheet = f"""
            IconButton {{
                /* Base state: transparent background, circular shape */
                background-color: transparent; 
                border: none;
                border-radius: {size.width() // 2}px; /* Makes it a perfect circle */
                
                /* Smooth transition for size and color */
                transition: background-color 0.2s, transform 0.2s; 
            }}
            
            IconButton:hover {{
                /* Hover background: white (or light gray) */
                background-color: rgba(255, 255, 255, 0.7); /* Slightly transparent white */
                
                /* Hover effect: slightly bigger (1.1x scale) */
                transform: scale(1.1); 
            }}
            
            /* Keep the icon centered and ensure it doesn't move */
            IconButton::icon {{
                padding: 0px; 
            }}

            QToolTip {{
                color: #000000; 
                background-color: #ffffff;
                border-radius: 32px; 
                padding: 4px 8px; 
                font-family: Arial, sans-serif;
                font-weight: bold;
            }}
        """
        self.setStyleSheet(style_sheet)

    def enterEvent(self, event): 
        self.setIcon(self.hover_icon)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.default_icon)
        super().leaveEvent(event)

# class Minimize(IconButton):
#     def __init__(self, parent=None):
#         super().__init__("Minimize", icon_path("QuichAppEdit.svg"), icon_path("QuichAppEdit_hover.svg"), parent=parent)

class QuickAppEdit(IconButton):
    def __init__(self, parent=None):
        super().__init__("Edit Quick Apps", icon_path("QuickAppEdit.svg"), icon_path("QuickAppEdit_hover.svg"), parent=parent)



