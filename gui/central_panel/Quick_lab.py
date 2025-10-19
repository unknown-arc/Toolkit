from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QScrollArea
)
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt

class QuickLabWidget(QFrame):
    """Chat-like QuickLab widget with 10:9 aspect ratio and bottom message input bar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 500)
        self.setStyleSheet("""
            QFrame {
                border-radius: 20px;
                background-color: #FFFFFF;
            }
        """)

        # Main vertical layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        # Scroll area for messages
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        # Bottom rounded bar container
        self.input_bar = QFrame()
        self.input_bar.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 25px;
            }
        """)
        self.input_bar.setFixedHeight(50)

        self.input_layout = QHBoxLayout(self.input_bar)
        self.input_layout.setContentsMargins(10, 5, 10, 5)
        self.input_layout.setSpacing(10)

        # Rounded input box (inside the bar)
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                border: none;
                background-color: transparent;
                padding-left: 10px;
                font-size: 16px;
            }
        """)

        # Circular black send button
        self.send_button = QPushButton("➤")
        self.send_button.setFixedSize(40, 40)
        self.send_button.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color: #000000;
                color: #FFFFFF;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #222222;
            }
        """)

        self.send_button.clicked.connect(self.send_message)

        # Add input and button to the bar
        self.input_layout.addWidget(self.message_input)
        self.input_layout.addWidget(self.send_button)

        # Add the input bar at bottom
        self.main_layout.addWidget(self.input_bar)

    def send_message(self):
        """Add message to scroll area with light white shade."""
        text = self.message_input.text().strip()
        if not text:
            return

        message_label = QLabel(text)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("""
            QLabel {
                background-color: #EEEEEE;  /* light white shade */
                border-radius: 15px;
                padding: 8px;
                margin: 2px;
            }
        """)
        message_label.setFont(QFont("Segoe UI", 12))
        message_label.setAlignment(Qt.AlignLeft)

        self.scroll_layout.addWidget(message_label)
        self.message_input.clear()

        # Auto scroll to bottom
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )
