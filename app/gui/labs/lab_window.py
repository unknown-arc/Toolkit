from PySide6.QtWidgets import (
    QApplication, QFrame, QVBoxLayout, QWidget, QLabel, QStackedLayout, QSizePolicy
)
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt


from gui.labs.lab_hostbar import LabHostBar


class LabWindow(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(600, 500)
        self.setStyleSheet("""
            QFrame {
                border-radius: 20px;
                background-color: #F7F7F7;
            }
        """)

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        # Content area
        self.content_area = QFrame()
        self.content_area.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border-radius: 12px;
            }
        """)

        self.content_area_layout = QVBoxLayout(self.content_area)
        self.content_area_layout.setContentsMargins(15, 15, 15, 15)
        self.content_area_layout.setSpacing(10)

        # Lab bar (pure GUI widget)
        self.lab_bar = LabHostBar()
        self.lab_bar.setFixedHeight(50)
        self.content_area_layout.addWidget(self.lab_bar, 0, Qt.AlignTop)

        # Session container (empty) — logic file will add/remove widgets here
        self.session_container = QFrame()
        self.session_layout = QVBoxLayout(self.session_container)
        self.session_layout.setContentsMargins(0, 0, 0, 0)
        self.session_layout.setSpacing(0)
        self.content_area_layout.addWidget(self.session_container, 1)

        self.main_layout.addWidget(self.content_area, 1)




