from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QHBoxLayout, QFrame
)
from PySide6.QtCore import Qt


class MessageFrame(QWidget):
    def __init__(self, message_widget: QWidget, parent=None):
        super().__init__(parent)

        # Styles
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
            }
            QFrame#message_bg {
                background-color: #ffffff;
            }
            QFrame#card {
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-radius: 16px;
                padding: 40px;
            }
        """)

        self.setWindowTitle("App")
        self.resize(900, 600)

        # --------------- Main Layout (Root) ---------------
        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        # ---------- message AREA ----------
        message = QFrame()
        message.setObjectName("message_bg")

        message_layout = QVBoxLayout(message)
        message_layout.setContentsMargins(20, 20, 20, 20)
        message_layout.setAlignment(Qt.AlignCenter)

        # Card Container
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(20)

        message_widget.setMaximumWidth(420)
        card_layout.addWidget(message_widget, alignment=Qt.AlignCenter)

        message_layout.addWidget(card, alignment=Qt.AlignCenter)
        root_layout.addWidget(message, stretch=1)
