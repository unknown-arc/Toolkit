from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QButtonGroup,
    QSizePolicy, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor, QPixmap
import os
import sys


class OccupationSelection(QWidget):
    """Vertical professional occupation selection with icon-text layout."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Question label
        question_label = QLabel("Please select your current occupation:")
        question_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        question_label.setStyleSheet("background: transparent;")  # <-- force transparency
        main_layout.addWidget(question_label, alignment=Qt.AlignLeft)


        # Vertical options layout
        options_layout = QVBoxLayout()
        options_layout.setSpacing(12)

        option_data = [
            ("Student", "icons/student.png"),
            ("Teacher", "icons/teacher.png"),
            ("Working Professional", "icons/briefcase.png"),
            ("Other", "icons/other.png")
        ]

        self.option_buttons = []
        self.option_group = QButtonGroup(self)
        self.option_group.setExclusive(True)

        self.selected_color = "#B3D9FF"  # light blue

        for name, icon_path in option_data:
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setFixedHeight(50)
            btn.setStyleSheet(self._base_style())

            # Horizontal layout: icon + text
            layout = QHBoxLayout(btn)
            layout.setContentsMargins(12, 6, 12, 6)
            layout.setSpacing(10)
            layout.setAlignment(Qt.AlignLeft)

            # Icon
            icon_label = QLabel()
            icon_label.setAlignment(Qt.AlignCenter)
            # Match icon size with text height (~16-18px)
            icon_size = 20
            icon_label.setFixedSize(icon_size, icon_size)
            if os.path.exists(icon_path):
                pixmap = QPixmap(icon_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_label.setPixmap(pixmap)
            else:
                icon_label.setStyleSheet("background-color: #FFFFFF; border-radius: 4px;")
            layout.addWidget(icon_label)

            # Text
            text_label = QLabel(name)
            text_label.setFont(QFont("Segoe UI", 12))
            text_label.setStyleSheet("background: transparent;")
            layout.addWidget(text_label)

            # Stretch to fill button width
            layout.addStretch()

            btn.icon_label = icon_label
            btn.text_label = text_label

            # Click handler
            btn.clicked.connect(lambda checked, b=btn: self._update_styles(b))

            # Hover effects
            btn.enterEvent = lambda e, b=btn: self._hover_enter(b)
            btn.leaveEvent = lambda e, b=btn: self._hover_leave(b)

            self.option_group.addButton(btn)
            self.option_buttons.append(btn)
            options_layout.addWidget(btn)

        main_layout.addLayout(options_layout)
        main_layout.addStretch()

    def _base_style(self):
        return """
            QPushButton {
                border-radius: 8px;
                border: 2px solid #C9C9C9;
                background-color: #FFFFFF;
                text-align: left;
            }
            QPushButton:hover {
                border: 2px solid #0078D7;
            }
        """

    def _update_styles(self, selected_btn):
        """Update selected style: light blue background, bold blue text."""
        for btn in self.option_buttons:
            if btn == selected_btn and btn.isChecked():
                btn.setStyleSheet(f"""
                    QPushButton {{
                        border-radius: 8px;
                        border: 2px solid #0078D7;
                        background-color: {self.selected_color};
                    }}
                """)
                btn.text_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
                btn.text_label.setStyleSheet("color: #0078D7; background: transparent;")
                btn.icon_label.setFixedSize(24, 24)  # slightly bigger
            else:
                btn.setStyleSheet(self._base_style())
                btn.text_label.setFont(QFont("Segoe UI", 12))
                btn.text_label.setStyleSheet("color: black; background: transparent;")
                btn.icon_label.setFixedSize(20, 20)

    def _hover_enter(self, btn):
        """Slightly enlarge icon on hover if not selected."""
        if not btn.isChecked():
            btn.icon_label.setFixedSize(22, 22)
            btn.text_label.setFont(QFont("Segoe UI", 12, QFont.Bold))

    def _hover_leave(self, btn):
        """Reset icon size after hover leaves if not selected."""
        if not btn.isChecked():
            btn.icon_label.setFixedSize(20, 20)
            btn.text_label.setFont(QFont("Segoe UI", 12))

    def get_selected_option(self):
        for btn in self.option_buttons:
            if btn.isChecked():
                return btn.text_label.text()
        return None


# --- Preview ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OccupationSelectionProfessional()
    w.setStyleSheet("background: #F3F3F3;")
    w.resize(300, 300)
    w.show()
    sys.exit(app.exec())
