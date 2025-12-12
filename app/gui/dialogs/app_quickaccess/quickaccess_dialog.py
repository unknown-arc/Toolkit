# quick_access_dialog.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor

from .content.quickaccess_bar import QuickAccessAppBar as PartOneWidget
from .content.otherapps_bar import OtherApps as PartTwoWidget


class QuickAccessDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Transparent parent background for dimming effect
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Full-screen dialog for backdrop
        if parent:
            self.setGeometry(parent.geometry())
        else:
            self.resize(1200, 800)

        # Create content container
        self.container = QWidget(self)
        self.container.setObjectName("container")
        self.container.setFixedSize(1000, 600)

        # Main layout
        layout = QVBoxLayout(self.container)

        # Top bar with close button
        top_bar = QHBoxLayout()
        title = QLabel("Quick Access")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        close_button = QPushButton("✖")
        close_button.setFixedSize(32, 32)
        close_button.clicked.connect(self.accept)

        top_bar.addWidget(title)
        top_bar.addStretch()
        top_bar.addWidget(close_button)

        # ----- Insert Part 1 -----
        self.part_one = PartOneWidget()
        self.part_one.setFixedHeight(140)

        # ----- Insert Part 2 -----
        self.part_two = PartTwoWidget()

        # Add widgets to layout
        layout.addLayout(top_bar)
        layout.addWidget(self.part_one)
        layout.addWidget(self.part_two)

        layout.setContentsMargins(20, 10, 20, 20)
        layout.setSpacing(20)

        # Style
        self.setStyleSheet("""
            QWidget#container {
                background-color: white;
                border-radius: 15px;
                border: 1px solid grey;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                color: red;
            }
        """)

        # Center dialog
        self.center_container()

    def center_container(self):
        parent_size = self.size()
        container_size = self.container.size()
        self.container.move(
            (parent_size.width() - container_size.width()) // 2,
            (parent_size.height() - container_size.height()) // 2
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 150))  # Dim background


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = QuickAccessDialog()
    dialog.exec()