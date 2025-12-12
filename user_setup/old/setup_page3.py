from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QApplication, QSizePolicy, QPushButton, QLabel, QButtonGroup, QSizePolicy, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor

import sys

class ThemeAndColorSlection(QWidget):
    """Widget for Theme and Color selection inside Page 3 card."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        font = QFont("Segoe UI", 13)

        # --- Theme Selection ---
        theme_label = QLabel("Choose App Theme")
        theme_label.setFont(font)
        layout.addWidget(theme_label, alignment=Qt.AlignLeft)

        theme_row = QHBoxLayout()
        theme_row.setSpacing(20)
        self.light_btn = QPushButton("Light")
        self.dark_btn = QPushButton("Dark")

        for btn in [self.light_btn, self.dark_btn]:
            btn.setCheckable(True)
            btn.setFixedSize(120, 60)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #dcdcdc;
                    border-radius: 12px;
                    background-color: #ffffff;
                    font-size: 14px;
                }
                QPushButton:checked {
                    border: 3px solid #0078D7;
                }
            """)
        self.light_btn.setChecked(True)

        theme_group = QButtonGroup(self)
        theme_group.addButton(self.light_btn)
        theme_group.addButton(self.dark_btn)

        theme_row.addWidget(self.light_btn)
        theme_row.addWidget(self.dark_btn)
        layout.addLayout(theme_row)

        # --- Color Selection ---
        color_label = QLabel("Choose App Color")
        color_label.setFont(font)
        layout.addWidget(color_label, alignment=Qt.AlignLeft)

        color_row = QHBoxLayout()
        color_row.setSpacing(15)
        self.color_buttons = []
        colors = ["#007bff", "#28a745", "#dc3545", "#fd7e14"]
        for color in colors:
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setFixedSize(36, 36)
            btn.setStyleSheet(f"""
                QPushButton {{
                    border-radius: 18px;
                    background-color: {color};
                    border: 2px solid #ffffff;
                }}
                QPushButton:checked {{
                    border: 3px solid {color};
                }}
            """)
            color_row.addWidget(btn)
            self.color_buttons.append(btn)

        color_group = QButtonGroup(self)
        for btn in self.color_buttons:
            color_group.addButton(btn)

        layout.addLayout(color_row)

    def get_theme_color(self):
        """Return selected theme and color as a dictionary."""
        theme = "Light" if self.light_btn.isChecked() else "Dark"
        selected_color = None
        for btn in self.color_buttons:
            if btn.isChecked():
                selected_color = btn.styleSheet().split("background-color:")[1].split(";")[0].strip()
                break
        return {"theme": theme, "color": selected_color}


# # --- Preview ---
# if __name__ == "__main__":
#     import sys
#     from PySide6.QtWidgets import QApplication

#     app = QApplication(sys.argv)
#     window = AppThemeAndColor()
#     window.show()
#     sys.exit(app.exec())
