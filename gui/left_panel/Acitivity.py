#!/usr/bin/env python3
"""
PySide6 widget with minimum size 260x300
Displays 'Activity' text at the top in black.
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt


class ActivityWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Activity Widget")
        self.setMinimumSize(260, 300)

        # Layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # Align content to top-center
        layout.setContentsMargins(10, 15, 10, 10)  # Padding around edges

        # Title label
        title_label = QLabel("Activity")
        title_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: black;")

        # Background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)

        # Add widgets to layout
        layout.addWidget(title_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ActivityWidget()
    widget.show()
    sys.exit(app.exec())
