from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPalette


class RightPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor("#EDEDED"))
        self.setPalette(pal)
        self.setFrameStyle(QFrame.NoFrame)
        self.setLineWidth(0)
        self.setStyleSheet("color: white;")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(alignment=Qt.AlignTop | Qt.AlignHCenter))