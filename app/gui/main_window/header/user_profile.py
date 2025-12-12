import os
import sys
from PySide6.QtWidgets import (
    QApplication, 
    QPushButton, 
    QMainWindow, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout, # Added for better header simulation
    QLabel
)
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QColor
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QIcon
from pathlib import Path


'''
def profile_picture_loc(profile_id):
    base_dir = Path(__file__).resolve().parent.parent.parent / "user_data" 
    file_path = base_dir / f"Profile {profile_id}" 
    full_path = base_dir / f"Profile {profile_id}" / "profile_picture.png"
    # print(f"Checking path existence: {full_path}")

    if not file_path.exists():
        print(f"ERROR: Profile directory not found at {file_path}")
        return "path_error"

    elif not full_path.exists():
        print(f"ERROR: File not found at {full_path}")
        return "file_error"
    
    # else:
        # print(f"SUCCESS: File exists at {full_path}")
    return str(full_path)

class UserProfile(QPushButton):

    UserProfilePicture = profile_picture_loc("1")

    def __init__(self, preferred_size: int = 64):
        
        super().__init__()
        self._preferred_size = preferred_size 
        self._load_and_prepare_image()
        
        # Add a simple stylesheet to remove the default button border/background
        self.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 0;
            }
        """)

    def _load_and_prepare_image(self):

        image_loaded = False

        if self.UserProfilePicture not in ["path_error", "file_error"]:
            pixmap = QPixmap(self.UserProfilePicture)
            if not pixmap.isNull():
                image_loaded = True
                # Resize the pixmap to preferred size while keeping aspect ratio
                self._original_pixmap = pixmap.scaled(
                    self._preferred_size, 
                    self._preferred_size, 
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                    Qt.TransformationMode.SmoothTransformation
                )
        
        if not image_loaded:            
            user_profile_icon = Path(__file__).resolve().parent.parent.parent / "assets" / "header_icons" / "user_default_profile_icon.svg"
            self._original_pixmap = QPixmap(str(user_profile_icon)).scaled(
                self._preferred_size, 
                self._preferred_size, 
                Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                Qt.TransformationMode.SmoothTransformation
            )
'''

class ProfileIcon(QPushButton):
    def __init__(self, size=QSize(64, 64), parent=None):
        super().__init__(parent)

        user_profile_icon = Path(__file__).resolve().parents[3] / "assets" / "header_icons" / "user_profile_icon.svg"
        user_profile_icon_hover = Path(__file__).resolve().parents[3] / "assets" / "header_icons" / "user_profile_icon_hover.svg"

        self.default_icon = QIcon(str(user_profile_icon))
        self.hover_icon = QIcon(str(user_profile_icon_hover))
        
        # Button size and icon size
        self.setFixedSize(size)
        icon_dim = min(size.width(), size.height()) - 24  
        self.setIconSize(QSize(icon_dim, icon_dim))
        self.setFlat(True)
        self.setIcon(self.default_icon)
        self.setToolTip("User Profile")

        
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
                Hover background: white (or light gray) */
                background-color: rgba(255, 255, 255, 0.7); /* Slightly transparent white */
                
                Hover effect: slightly bigger (1.1x scale) */
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


            
    