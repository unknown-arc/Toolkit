from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
import sys
import os
from pathlib import Path

# Function to get full asset path
# def icon_path(asset_name):
#     base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#     print(f"Base directory for assets: {base_dir}")
#     print (os.path.join(base_dir, "assets", asset_name))
#     return os.path.join(base_dir, "assets", asset_name)

def icon_path(asset_name):
    # base_dir = Path(__file__).resolve().parents[3] / "assets" / "header_icons"
    base_dir = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "header_icons"
    full_path = base_dir / asset_name 
    # print(f"Checking path existence: {full_path}")
    if not full_path.exists():
        print(f"ERROR: File not found at {full_path}")
    # else:
        # print(f"SUCCESS: File exists at {full_path}")
    return str(full_path)

# def icon_path(asset_name):
#     base_dir = os.path.dirname(__file__)
#     print(f"Base directory for assets: {base_dir}")
#     return os.path.join(base_dir, asset_name)
 
 
# Generic QPushButton with hover icon
class IconButton(QPushButton):
    def __init__(self, name, default_icon_path, hover_icon_path, size=QSize(48, 48), parent=None):
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


class UserSetting(IconButton):
    def __init__(self, parent=None):
        super().__init__("Setting", icon_path("setting.svg"), icon_path("setting_hover.svg"), parent=parent)

class GetHelp(IconButton):
    def __init__(self, parent=None):
        super().__init__("GetHelp", icon_path("help.svg"), icon_path("help_hover.svg"), parent=parent)

class Notification(IconButton):
    def __init__(self, parent=None):
        super().__init__("Notification", icon_path("notification.svg"), icon_path("notification_hover.svg"), parent=parent)

class MarketPlace(IconButton):
    def __init__(self, parent=None):
        super().__init__("MarketPlace", icon_path("market.svg"), icon_path("market_hover.svg"), parent=parent)



# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Buttons with Hover Icons")

#         layout = QHBoxLayout(self)

#         # Step 1: Create buttons
#         self.user_setting = UserSetting()
#         self.get_help = GetHelp()
#         self.notification = Notification()
#         self.marketplace = MarketPlace()

#         # Step 2: Connect signals
#         self.user_setting.clicked.connect(lambda: print("UserSetting clicked"))
#         self.get_help.clicked.connect(lambda: print("GetHelp clicked"))
#         self.notification.clicked.connect(lambda: print("Notification clicked"))
#         self.marketplace.clicked.connect(lambda: print("MarketPlace clicked"))

#         # Step 3: Add buttons to layout
#         layout.addWidget(self.user_setting)
#         layout.addWidget(self.get_help)
#         layout.addWidget(self.notification)
#         layout.addWidget(self.marketplace)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
