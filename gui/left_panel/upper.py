#!/usr/bin/env python3
"""
Simple 300x200 widget with 'Hello' text in black.
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt


class HelloWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Hello Widget")
        self.resize(260, 200)  # Fixed size as requested

        # Layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Label
        label = QLabel("Not Done yet")
        label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)

        # Colors
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        palette.setColor(QPalette.WindowText, QColor("black"))
        self.setPalette(palette)

        label.setStyleSheet("color: black;")

        layout.addWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = HelloWidget()
    widget.show()
    sys.exit(app.exec())
