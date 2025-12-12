from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QApplication, QMainWindow, QVBoxLayout
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtCore import QSize, Qt, QEvent
import sys
import os
from pathlib import Path

def icon_path(asset_name):
    # base_dir = Path(__file__).resolve().parents[3] / "assets" / "header_icons"
    base_dir = Path(__file__).resolve().parent.parent.parent / "assets" 
    full_path = base_dir / asset_name 
    if not full_path.exists():
        print(f"ERROR: File not found at {full_path}")
    return str(full_path)

 
# Generic QPushButton with hover icon
class IconButton(QPushButton):
    def __init__(self, name, default_icon_path, hover_icon_path, size=QSize(64, 64), parent=None):
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


class BackButton(IconButton):
    def __init__(self, parent=None):
        super().__init__("Back", icon_path("back_button_icon.svg"), icon_path("back_button_icon_hover.svg"), parent=parent)

class NextButton(IconButton):
    def __init__(self, parent=None):
        super().__init__("Next", icon_path("next_button_icon.svg"), icon_path("next_button_icon_hover.svg"), parent=parent)


class TextButton(QPushButton):
    def __init__(self, name, effect_type="blank", effect_text="", parent=None):
        super().__init__(name, parent)

        self.default_text = name
        self.effect_text = effect_text
        self.effect_type = effect_type

        # Only for effect type 3 (text change)
        if effect_type == "hover-text":
            self.hover_text = f"{name} {effect_text}"
        else:
            self.hover_text = name

        self.setFixedSize(180, 40)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        # Apply correct style based on effect type
        self.apply_style()

        # Enable hover detection only for types 2 and 3
        if effect_type in ("hover-fill", "hover-text"):
            self.setMouseTracking(True)
            self.installEventFilter(self)

    # -------------------------------------------------
    # STYLE SETUP
    # -------------------------------------------------
    def apply_style(self):

        # TYPE 1 → simple border, no hover effect
        if self.effect_type == "blank":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    color: #000000;
                    border: 2px solid #000000;
                    border-radius: 10px;
                    font-size: 14px;
                    font-weight: 700;
                }
            """)
        
        # TYPE 2 → hover turns solid black
        elif self.effect_type == "hover-fill":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    color: #000000;
                    border: 2px solid #000000;
                    border-radius: 10px;
                    font-size: 14px;
                    font-weight: 700;
                    transition: all 0.3s ease;
                }
                QPushButton:hover {
                    background-color: #000000;
                    color: #ffffff;
                }
            """)

        # TYPE 3 → hover changes text also
        elif self.effect_type == "hover-text":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    color: #000000;
                    border: 2px solid #000000;
                    border-radius: 10px;
                    font-size: 14px;
                    font-weight: 700;
                    transition: all 0.3s ease;
                }
                QPushButton:hover {
                    background-color: #000000;
                    color: #ffffff;
                }
            """)

    # -------------------------------------------------
    # HOVER TEXT CHANGE (Only for type 3)
    # -------------------------------------------------
    def eventFilter(self, source, event):

        if self.effect_type == "hover-text":
            if event.type() == QEvent.Enter:
                self.setText(self.hover_text)

            elif event.type() == QEvent.Leave:
                self.setText(self.default_text)

        return super().eventFilter(source, event)


class ContinueButton(TextButton):
    def __init__(self, parent=None):
        super().__init__("Continue", 
        effect_type="hover-text", 
        effect_text="→", 
        parent=parent)

class FinishSetupButton(TextButton):
    def __init__(self, parent=None):
        super().__init__("Finish Setup", 
        effect_type="blank", 
        parent=parent)

class LaunchAppButton(TextButton):    
    def __init__(self, parent=None):
        super().__init__("Launch App", 
        effect_type="hover-fill", 
        parent=parent)        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a central widget
        central = QWidget()
        layout = QVBoxLayout(central)

        # Buttons
        txtbtn1 = ContinueButton()
        txtbtn2 = FinishSetupButton()
        txtbtn3 = LaunchAppButton()
        iconbtn1 = BackButton()
        iconbtn2 = NextButton()

        layout.addWidget(txtbtn1)
        layout.addWidget(txtbtn2)
        layout.addWidget(txtbtn3)
        layout.addWidget(iconbtn1)
        layout.addWidget(iconbtn2)

        # Attach layout to MainWindow
        self.setCentralWidget(central)

        self.setWindowTitle("Button Test")
        self.resize(400, 400)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
