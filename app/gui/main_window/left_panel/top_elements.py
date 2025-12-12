from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStyle
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
import sys
from pathlib import Path

from core.signal_manager import LeftPanel_eb, Quickaccess_eb


def icon_path(asset_name):
    base_dir = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "leftpanel_icons"
    # base_dir = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "header_icons"
    full_path = base_dir / asset_name
    if not full_path.exists():
        print(f"ERROR: File not found at {full_path}")
    return str(full_path)

class IconTextButton(QPushButton):
    def __init__(self, name, default_icon_path, hover_icon_path, height=32, parent=None):
        super().__init__(parent)

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
            }}
            
            #IconTextButton:hover {{
                /* Hover background: light gray (standard navigation hover color) */
                background-color: #ffffff; 
                front-weight: bold;
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

class NewLab(IconTextButton):
    def __init__(self, parent=None):
        super().__init__("New Lab", icon_path("newlab.svg"), icon_path("newlab_hover.svg"), parent=parent)

class IncognitoLab(IconTextButton):
    def __init__(self, parent=None):
        super().__init__("Incorognito Lab", icon_path("incognitolab_icon.svg"), icon_path("incognitolab_hover_icon.svg"), parent=parent)

class CloseAllLab(IconTextButton):
    def __init__(self, parent=None):
        super().__init__("Close All Lab", icon_path("closeall_icon.svg"), icon_path("closeall_hover_icon.svg"), parent=parent)


class MarketPlace(IconTextButton):
    def __init__(self, parent=None):
        super().__init__("Add New App", icon_path("market.svg"), icon_path("market_hover.svg"), parent=parent)


# --- Main Application Window for Demonstration ---
class TopElementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Icon and Text Button Demo")
        self.setGeometry(200, 200, 350, 400)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Helper to get standard QIcons for a runnable example
        style = QApplication.style()

        
        # Step 1: Create buttons
        self.new_lab = NewLab()
        self.incognito_lab = IncognitoLab()
        self.closeall_lab = CloseAllLab()
        self.marketplace = MarketPlace()

#         # Step 2: Connect signals
        self.new_lab.clicked.connect(lambda: LeftPanel_eb.new_lab.emit())
        self.incognito_lab.clicked.connect(lambda: LeftPanel_eb.incognito_lab.emit("quicklab"))
        self.closeall_lab.clicked.connect(lambda: LeftPanel_eb.close_all_labs.emit())
        self.marketplace.clicked.connect(lambda: Quickaccess_eb.open_quickaccess_dialog.emit())

#         # Step 3: Add buttons to layout
        layout.addWidget(self.new_lab)
        layout.addWidget(self.incognito_lab)
        layout.addWidget(self.closeall_lab)
        layout.addWidget(self.marketplace)
        
        layout.addStretch()
   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TopElementWindow()
    window.show()
    sys.exit(app.exec())