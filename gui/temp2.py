import sys
from PySide6.QtWidgets import (
    QApplication, 
    QFrame, 
    QLabel,
    QWidget,
    QVBoxLayout,
    QToolButton,
    QSizePolicy,
    QHBoxLayout
)
from PySide6.QtGui import QColor, QPixmap, QIcon
from PySide6.QtCore import Qt, QSize

# --- DEPENDENCIES (NavButton) ---

class NavButton(QToolButton):
    """Styled button for modern sidebar navigation items (Icon + Text)."""
    def __init__(self, text, icon_color, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # Button should expand horizontally but have fixed height
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(45)

        # Placeholder for icon
        pixmap = QPixmap(24, 24)
        pixmap.fill(QColor(icon_color))
        self.setIcon(QIcon(pixmap))
        self.setIconSize(QSize(20, 20))

        # Styling for a modern sidebar look
        self.setStyleSheet("""
            QToolButton {
                text-align: left;
                padding: 10px 15px;
                border: none;
                color: #333333;
                font-size: 11pt;
                font-weight: 500;
                border-radius: 8px; /* Slightly rounded */
            }
            QToolButton:hover {
                background-color: #C0C0C0; /* Lighter hover */
            }
            QToolButton:checked {
                background-color: #A0A0A0; /* Active/selected state */
                color: white;
            }
        """)
        # Allow selection behavior
        self.setCheckable(True)

# --- TARGET COMPONENT (LeftPanel) ---

class LeftPanel(QFrame):
    """
    Styled left navigation panel with modern navigation buttons.
    This panel uses NavButton components and is structured 
    to accommodate three main blocks of functionality.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        # We don't need QPalette setup here if we use stylesheet
        
        # Apply border radius and ensure background color via stylesheet
        self.setStyleSheet(
             "QFrame {"
             "border-radius: 15px;" 
             "background-color: #D9D9D9;" # Background for the panel itself
             "color: #333333;"
             "padding: 10px;" # Inner padding
             "}"
        )
        # Ensure minimum size for the full panel view
        self.setMinimumWidth(250)
        self.setMaximumWidth(300)

        layout = QVBoxLayout(self)
        layout.setSpacing(5) # Smaller spacing between items
        layout.setContentsMargins(10, 10, 10, 10) # Margins inside the panel frame
        
        # 1. Navigation Title/Placeholder (App Name or Logo Placeholder)
        app_logo_label = QLabel("APP NAME", alignment=Qt.AlignTop | Qt.AlignHCenter)
        app_logo_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #555555; margin-bottom: 20px;")
        layout.addWidget(app_logo_label)
        
        # 2. Navigation Block 1 (Main Menu)
        layout.addWidget(QLabel("MAIN MENU", styleSheet="font-size: 9pt; font-weight: bold; color: #777777; margin-top: 10px; margin-bottom: 5px; margin-left: 10px;"))
        self.dashboard_btn = NavButton("Dashboard", "#00A0FF")
        self.dashboard_btn.setChecked(True) # Set dashboard as active
        layout.addWidget(self.dashboard_btn)

        # 3. Navigation Block 2 (User's request placeholder)
        self.projects_btn = NavButton("Projects", "#00CC66")
        layout.addWidget(self.projects_btn)
        
        # 4. Navigation Block 3 (User's request placeholder)
        self.reports_btn = NavButton("Reports", "#FFA000")
        layout.addWidget(self.reports_btn)

        # Optional: Another block (e.g., Settings/Help)
        layout.addWidget(QLabel("SUPPORT", styleSheet="font-size: 9pt; font-weight: bold; color: #777777; margin-top: 15px; margin-bottom: 5px; margin-left: 10px;"))
        self.settings_btn_nav = NavButton("Settings & Help", "#FF0000")
        layout.addWidget(self.settings_btn_nav)
        
        # Stretch to push content to the top
        layout.addStretch(1)


# --- Demonstration Code ---

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Create a simple container window to show the panel
    container = QWidget()
    container.setWindowTitle("Left Panel Isolation View")
    container.setStyleSheet("background-color: #F0F0F0; padding: 20px;")
    
    main_layout = QHBoxLayout(container)
    
    left_panel = LeftPanel()
    main_layout.addWidget(left_panel)
    
    # Add stretch to push the panel to the left, like it would be in a larger app
    main_layout.addStretch(1)
    
    container.resize(400, 600)
    container.show()
    
    sys.exit(app.exec())
