# settings_left.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout, QButtonGroup
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor

from core.signal_manager import Header_eb

class SettingsLeftPanel(QWidget):

    section_selected = Signal(str)


    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # --- Top bar (Back + Title)
        top_bar = QHBoxLayout()
        self.back_btn = QPushButton("←")
        self.back_btn.setFixedSize(32, 32)
        self.back_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                font-size: 18px;
                color: #333;
            }
            QPushButton:hover {
                color: #0078D7;
            }
        """)

        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        top_bar.addWidget(self.back_btn)
        top_bar.addWidget(title)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        # --- Section Buttons ---
        self.buttons = {}
        sections = ["General", "Privacy", "Notifications", "Account"]

        btn_group = QButtonGroup(self)
        btn_group.setExclusive(True)

        for sec in sections:
            btn = QPushButton(sec)
            btn.setCheckable(True)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    border-radius: 10px;
                    padding: 10px;
                    text-align: left;
                    background-color: transparent;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #f2f2f2;
                }
                QPushButton:checked {
                    background-color: #e6f0ff;
                    color: #0078D7;
                    font-weight: bold;
                }
            """)
            btn_group.addButton(btn)
            layout.addWidget(btn)
            self.buttons[sec] = btn
            btn.clicked.connect(lambda _, s=sec: self.section_selected.emit(s))


        # ===Connect Signals===
        self.back_btn.clicked.connect(Header_eb.back_to_main_page.emit)

        # Default selection
        self.buttons["General"].setChecked(True)
        layout.addStretch()
