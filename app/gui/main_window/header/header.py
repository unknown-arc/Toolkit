import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QFrame, 
    QHBoxLayout, 
    QLabel,
    QWidget,
    QVBoxLayout
)
from PySide6.QtGui import QColor, QPalette, QPixmap
from PySide6.QtCore import Qt

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).resolve().parents[3]
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

from gui.main_window.header.user_profile import ProfileIcon as UserProfile
from gui.main_window.header.header_element import UserSetting, GetHelp, Notification, MarketPlace
from core.signal_manager import Header_eb

class Header(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)       
        
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, QColor("#EDEDED")) # Light gray background
        # pal.setColor(QPalette.ColorRole.Window, QColor("#008000")) # Green background while working
        self.setPalette(pal)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Setup the main horizontal layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5) # Margin for breathing room
        layout.setSpacing(0)
        
        # Step 1: Create buttons          
        self.profile_button = UserProfile()
        self.user_setting = UserSetting()
        self.get_help = GetHelp()
        self.notification = Notification()
        self.marketplace = MarketPlace()

        # Step 2: Connect signals
        self.profile_button.clicked.connect(Header_eb.open_userprofile_dialog.emit)
        self.user_setting.clicked.connect(Header_eb.open_settings_page.emit)
        self.get_help.clicked.connect(Header_eb.open_gethelp_dialog.emit)
        self.notification.clicked.connect(lambda: Header_eb.open_notification_popup.emit(self.notification))
        self.marketplace.clicked.connect(Header_eb.open_marketplace_page.emit)

        # Step 3: Add buttons to layout
        layout.addSpacing(20)
        layout.addWidget(self.profile_button, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addStretch(1)
        layout.addWidget(self.notification)
        layout.addWidget(self.get_help)
        layout.addWidget(self.user_setting)
        layout.addWidget(self.marketplace)
        layout.addSpacing(20)


# --- Demonstration Code ---

if __name__ == '__main__':
    app = QApplication(sys.argv)
    header = Header()
    header.resize(800, 60)
    header.show()
    sys.exit(app.exec())