from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor

class CustomDialog(QDialog):
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
        self.container.setFixedSize(1000, 500)

        # Main layout
        layout = QVBoxLayout(self.container)

        # Top bar with close button
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        close_button = QPushButton("✖")
        close_button.setFixedSize(32, 32)
        close_button.clicked.connect(self.accept)
        top_bar.addWidget(close_button)

        # Label/content
        label = QLabel("This is a custom dialog")
        label.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        layout.addLayout(top_bar)
        layout.addWidget(label)
        layout.setContentsMargins(20, 10, 20, 20)

        # Style
        self.setStyleSheet("""
            QWidget#container {
                background-color: white;
                border-radius: 15px;
                border: 1px solid grey;
            }
            QLabel {
                font-size: 18px;
                padding: 10px;
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
        painter.fillRect(self.rect(), QColor(0, 0, 0, 150))  # Dim entire background
        super().paintEvent(event)

if __name__ == "__main__":  
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    dlg = CustomDialog()
    dlg.exec()