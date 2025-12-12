from PySide6.QtWidgets import ( 
    QApplication, QWidget, QHBoxLayout, 
    QPushButton, QApplication, QMainWindow, 
    QVBoxLayout, QSizePolicy)
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtCore import QSize, Qt, QEvent
import sys
import os
from pathlib import Path


def icon_path(asset_name):
    base_dir = Path(__file__).resolve().parent.parent.parent / "assets"
    full_path = base_dir / asset_name
    if not full_path.exists():
        print(f"ERROR: File not found at {full_path}")
    return str(full_path)


class IconLoginButton(QPushButton):
    def __init__(self, name, icon_path, size=QSize(64, 64), parent=None):
        super().__init__(parent)

        self.icon = QIcon(str(icon_path))
        self.bg_color = "transparent"
        self.default_size = size

        # Button size and icon size
        self.setFixedSize(size)
        icon_dim = min(size.width(), size.height()) - 24
        self.setIconSize(QSize(icon_dim, icon_dim))
        self.setIcon(self.icon)
        self.setToolTip(name)
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)

        self.setContentsMargins(0,0,0,0)
        

        self.update_style()  

    def update_style(self):
        size = self.size()
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.bg_color};
                border: none;
                border-radius: {size.width() // 2}px;
                
            }}
            QToolTip {{
                color: #000000; 
                background-color: #ffffff;
                border-radius: 32px; 
                padding: 4px 8px; 
                font-family: Arial, sans-serif;
                font-weight: bold;
            }}
        """)

    # Hover events
    def enterEvent(self, event):
        self.bg_color = "white"  # background turns white on hover
        self.update_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.bg_color = "transparent"  # revert to transparent
        self.update_style()
        super().leaveEvent(event)


class GoogleIcon(IconLoginButton):
    def __init__(self, name= "Google", icon_path = icon_path("google-logo.svg"), size=QSize(64, 64), parent=None):
        super().__init__(name, icon_path, size, parent) 

class AppleIcon(IconLoginButton):
    def __init__(self, name= "Apple", icon_path = icon_path("apple-logo.svg"), size=QSize(64, 64), parent=None):
        super().__init__(name, icon_path, size, parent)

class GitHubIcon(IconLoginButton):
    def __init__(self, name= "GitHub", icon_path = icon_path("github-logo.svg"), size=QSize(64, 64), parent=None):
        super().__init__(name, icon_path, size, parent)

class OutlookIcon(IconLoginButton):
    def __init__(self, name= "Outlook", icon_path = icon_path("outlook-logo.svg"), size=QSize(64, 64), parent=None):
        super().__init__(name, icon_path, size, parent)


class TextLoginButton(QPushButton):
    def __init__(self, text, bg_color="#000000", height=40, parent=None):
        super().__init__(text, parent)

        # Store properties
        self.default_text = text
        self.bg_color = bg_color

        # Set fixed size
        self.setFixedHeight(height)
        self.setMinimumWidth(200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Set cursor
        self.setCursor(QCursor(Qt.PointingHandCursor))

        # Apply style
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.bg_color};
                color: #ffffff;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 700;
            }}
        """)

class SignupButton(TextLoginButton):
    def __init__(self, text="Sign-up", bg_color="#0066ff", parent=None):        
        super().__init__(text, bg_color=bg_color, parent=parent)

class GuestLogin(TextLoginButton):
    def __init__(self, text="Guest", bg_color="#000000", parent=None):        
        super().__init__(text, bg_color=bg_color, parent=parent)

class LoginButton(TextLoginButton):      
    def __init__(self, text="Login", bg_color="#000000", parent=None):        
        super().__init__(text, bg_color=bg_color, parent=parent)  
   

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()        
        self.setFixedSize(400, 300)
        self.setWindowTitle("Login Buttons Example")

        main_layout = QVBoxLayout()  # Main vertical layout

        # Horizontal layout for social icons
        icon_layout = QHBoxLayout()
        icon_layout.setSpacing(0)  # space between icons
        icon_layout.setContentsMargins(0, 0, 0, 0)

        google_icon = GoogleIcon()
        apple_icon = AppleIcon()
        github_icon = GitHubIcon()
        outlook_icon = OutlookIcon()

        icon_layout.addWidget(google_icon)
        icon_layout.addWidget(apple_icon)
        icon_layout.addWidget(github_icon)
        icon_layout.addWidget(outlook_icon)

        main_layout.addLayout(icon_layout)
        main_layout.setSpacing(15)

        # Vertical stack for login buttons
        signup_login = SignupButton()
        guest_login = GuestLogin()
        login_button = LoginButton()

        main_layout.addWidget(signup_login)
        main_layout.addWidget(guest_login)
        main_layout.addWidget(login_button)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.show()





if __name__ == "__main__":    
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())        
