#!/usr/bin/env python3
"""
Minimal Digital Clock - PySide6
Always 24-hour format, white background, black text.
"""

import sys
from PySide6.QtCore import Qt, QTimer, QTime, QDate
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QFont, QColor, QPalette


class DigitalClock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Digital Clock - PySide6")
        self.setMinimumSize(260, 150)

        # Layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Time label
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont("Consolas", 40, QFont.Bold))

        # Date label
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setFont(QFont("Segoe UI", 14))

        layout.addWidget(self.time_label)
        layout.addWidget(self.date_label)

        # Colors
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        palette.setColor(QPalette.WindowText, QColor("black"))
        self.setPalette(palette)

        self.time_label.setStyleSheet("color: black;")
        self.date_label.setStyleSheet("color: black;")

        # Timer to update every second
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        self.update_time()

    def update_time(self):
        now = QTime.currentTime()
        time_text = now.toString("HH:mm:ss")  # 24-hour format
        date_text = QDate.currentDate().toString("dddd, MMMM d, yyyy")

        self.time_label.setText(time_text)
        self.date_label.setText(date_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec())
