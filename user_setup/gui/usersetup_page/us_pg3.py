from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QButtonGroup, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor


class AppearanceSelection(QWidget):
    """Professional Theme & Color selection widget for Page 3 card."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(25)

        font_label = QFont("Segoe UI", 13)

        # ---------------- Theme Selection ----------------
        theme_label = QLabel("Choose App Theme")
        theme_label.setFont(font_label)
        theme_label.setStyleSheet("background: transparent; font-weight: bold;")
        main_layout.addWidget(theme_label, alignment=Qt.AlignLeft)

        theme_row = QHBoxLayout()
        theme_row.setSpacing(20)

        self.light_btn = QPushButton("Light")
        self.dark_btn = QPushButton("Dark")

        for btn in [self.light_btn, self.dark_btn]:
            btn.setCheckable(True)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setFixedSize(140, 60)
            btn.setStyleSheet(self._theme_base_style())
        self.light_btn.setChecked(True)

        self.theme_group = QButtonGroup(self)
        self.theme_group.setExclusive(True)
        self.theme_group.addButton(self.light_btn)
        self.theme_group.addButton(self.dark_btn)

        # Click handlers
        self.light_btn.clicked.connect(lambda: self._update_theme_style(self.light_btn))
        self.dark_btn.clicked.connect(lambda: self._update_theme_style(self.dark_btn))

        theme_row.addWidget(self.light_btn)
        theme_row.addWidget(self.dark_btn)
        main_layout.addLayout(theme_row)

        # ---------------- Color Selection ----------------
        color_label = QLabel("Choose App Color")
        color_label.setFont(font_label)
        color_label.setStyleSheet("background: transparent; font-weight: bold;")
        main_layout.addWidget(color_label, alignment=Qt.AlignLeft)

        color_row = QHBoxLayout()
        color_row.setSpacing(15)
        self.color_buttons = []
        colors = ["#007bff", "#28a745", "#dc3545", "#fd7e14"]

        for color in colors:
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setFixedSize(36, 36)
            btn.color = color
            btn.setStyleSheet(f"""
                QPushButton {{
                    border-radius: 18px;
                    background-color: {color};
                    border: 2px solid #FFFFFF;
                }}
                QPushButton:checked {{
                    border: 2px solid #000000;
                }}
            """)
            btn.clicked.connect(lambda checked, b=btn: self._update_color_selection(b))
            color_row.addWidget(btn)
            self.color_buttons.append(btn)

        self.color_group = QButtonGroup(self)
        self.color_group.setExclusive(True)
        for btn in self.color_buttons:
            self.color_group.addButton(btn)

        main_layout.addLayout(color_row)
        main_layout.addStretch()

        # Initialize styles
        self._update_theme_style(self.light_btn)

    # ---------------- Theme Button Styling ----------------
    def _theme_base_style(self):
        return """
            QPushButton {
                border-radius: 12px;
                border: 2px solid #dcdcdc;
                background-color: #ffffff;
                font-size: 14px;
                font-weight: normal;
            }
            QPushButton:hover {
                border: 2px solid #0078D7;
            }
        """

    def _update_theme_style(self, selected_btn):
        for btn in [self.light_btn, self.dark_btn]:
            if btn == selected_btn and btn.isChecked():
                btn.setStyleSheet("""
                    QPushButton {
                        border-radius: 12px;
                        border: 2px solid #0078D7;
                        background-color: #B3D9FF;
                        font-size: 14px;
                        font-weight: bold;
                    }
                """)
            else:
                btn.setStyleSheet(self._theme_base_style())

    # ---------------- Color Selection ----------------
    def _update_color_selection(self, selected_btn):
        for btn in self.color_buttons:
            if btn == selected_btn and btn.isChecked():
                btn.setStyleSheet(f"""
                    QPushButton {{
                        border-radius: 18px;
                        background-color: {btn.color};
                        border: 2px solid #000000;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        border-radius: 18px;
                        background-color: {btn.color};
                        border: 2px solid #FFFFFF;
                    }}
                """)

    def get_theme_color(self):
        theme = "Light" if self.light_btn.isChecked() else "Dark"
        selected_color = None
        for btn in self.color_buttons:
            if btn.isChecked():
                selected_color = btn.color
                break
        return {"theme": theme, "color": selected_color}


# ---------------- Preview ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThemeAndColorSelectionProfessional()
    window.setStyleSheet("background: #F3F3F3;")
    window.resize(400, 250)
    window.show()
    sys.exit(app.exec())
