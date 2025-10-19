import sys
import os
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

from header.profile import UserProfile
from header.setting import SettingsButton
from header.notification import NotificationButton
from header.maket_place import MarketplaceButton

class Header(QFrame):
    """
    The main application header component.
    It includes an application title and the responsive Circular User Profile Button.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set fixed height as requested (80px), and styling
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, QColor("#EDEDED")) # Light gray background
        # pal.setColor(QPalette.ColorRole.Window, QColor("#008000")) # Green background while working
        self.setPalette(pal)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Setup the main horizontal layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5) # Margin for breathing room
        
        #Right side: Profile Button
        # Preferred size 64px, which will be constrained by the 80px header height (minus margins).
        self.profile_button = UserProfile(preferred_size=64)
        self.profile_button.clicked.connect(self._handle_profile_click)

        
        layout.addWidget(self.profile_button, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addStretch(1)

        self.notification_button = NotificationButton(preferred_size=40)
        self.notification_button.clicked.connect(self._handle_notification_click)

        self.settings_button = SettingsButton(preferred_size=56)
        self.settings_button.clicked.connect(self._handle_settings_click)

        self.marketplace_button = MarketplaceButton(preferred_size=56)
        self.marketplace_button.clicked.connect(self._handle_marketplace_click)

        layout.addWidget(self.notification_button, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.settings_button, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.marketplace_button, alignment=Qt.AlignmentFlag.AlignVCenter)

    def _handle_profile_click(self):
        """Dummy handler for button click."""
        print("Profile button clicked!")

    def _handle_notification_click(self):
        """Dummy handler for button click."""
        print("Notification button clicked!")

    def _handle_settings_click(self):
        """Dummy handler for button click."""
        print("Settings button clicked!")

    def _handle_marketplace_click(self):
        """Dummy handler for button click."""
        print("Marketplace button clicked!")            


# --- Demonstration Code ---

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    
    # --- Setup for Demonstration ---
    
    # Create a dummy image file so the button doesn't default to black
    if not os.path.exists(UserProfile.DUMMY_IMAGE_PATH):
        try:
            success_pixmap = QPixmap(128, 128) 
            success_pixmap.fill(QColor("gray"))
            success_pixmap.save(UserProfile.DUMMY_IMAGE_PATH, "PNG")
            print(f"Dummy profile image created at: {UserProfile.DUMMY_IMAGE_PATH}")
        except Exception:
            print("Could not create dummy image. Profile button will show BLACK.")


    main_window = QMainWindow()
    header = Header()
    
    # A simple main layout to showcase the header
    # central_widget = QWidget()
    # main_layout = QVBoxLayout(central_widget)
    # main_layout.addWidget(header)
    # main_layout.addStretch(1) 
    
    # main_window.setCentralWidget(central_widget)
    # main_window.setWindowTitle("App Header Example")
    # main_window.resize(600, 400)
    # main_window.show()
    
    # --- Cleanup Function ---
    # def cleanup():
    #     """Cleans up the temporary dummy file."""
    #     if os.path.exists(UserProfile.DUMMY_IMAGE_PATH):
    #         os.remove(UserProfile.DUMMY_IMAGE_PATH)

    # app.aboutToQuit.connect(cleanup)
    
    # sys.exit(app.exec())
