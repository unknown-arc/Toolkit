from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QFont

class HeaderFrame(QWidget):
    def __init__(self):
        super().__init__()

        self.min_height = 60     # final height after scroll
        self.max_height = 260    # starting expanded height

        self.setMinimumHeight(self.max_height)
        self.setMaximumHeight(self.max_height)

        self.title_label = QLabel("Marketplace")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            HeaderFrame {
                background-color: #3498DB; /* Light blue background */
            }
        """)

        

        # BIG starting font
        self.max_font = 72
        self.min_font = 18
        self.title_label.setFont(QFont("Segoe UI", self.max_font, QFont.Bold))

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        self._height = self.max_height

    # smooth animation value
    def getHeight(self):
        return self._height

    def setHeight(self, value):
        self._height = value
        self.setFixedHeight(value)

        # Dynamic font scaling based on height %
        ratio = (value - self.min_height) / (self.max_height - self.min_height)
        new_font_size = self.min_font + (self.max_font - self.min_font) * ratio

        self.title_label.setFont(QFont("Segoe UI", int(new_font_size), QFont.Bold))

    height_anim = Property(int, getHeight, setHeight)

    # external function
    def animateTo(self, target_height):
        anim = QPropertyAnimation(self, b"height_anim")
        anim.setDuration(300)
        anim.setEndValue(target_height)
        anim.setEasingCurve(QEasingCurve.InOutCubic)
        anim.start()
        self.anim = anim
